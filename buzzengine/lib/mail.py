from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMultiAlternatives

from google.appengine.api import mail as aeemail
from google.appengine.runtime import apiproxy_errors


def _send_deferred(message, fail_silently=False):
    try:
        message.send()
    except (aeemail.Error, apiproxy_errors.Error):
        if not fail_silently:
            raise


class EmailBackend(BaseEmailBackend):
    can_defer = False

    def send_messages(self, email_messages):
        num_sent = 0
        for message in email_messages:
            if self._send(message):
                num_sent += 1
        return num_sent

    def _copy_message(self, message):
        """
        Creates and returns App Engine EmailMessage class from message.
        """
        gmsg = aeemail.EmailMessage(sender=message.from_email,
            to=message.to,
            subject=message.subject,
            body=message.body)
        if message.extra_headers.get('Reply-To', None):
            gmsg.reply_to = message.extra_headers['Reply-To']
        if message.cc:
            gmsg.cc = list(message.cc)
        if message.bcc:
            gmsg.bcc = list(message.bcc)
        if message.attachments:
            # Must be populated with (filename, filecontents) tuples.
            attachments = []
            for attachment in message.attachments:
                if hasattr(attachment, "get_filename") and hasattr(attachment, "get_payload"):
                    attachments.append((attachment.get_filename(),
                                        attachment.get_payload(decode=True)))
                else:
                    attachments.append((attachment[0], attachment[1]))
            gmsg.attachments = attachments
            # Look for HTML alternative content.
        if isinstance(message, EmailMultiAlternatives):
            for content, mimetype in message.alternatives:
                if mimetype == 'text/html':
                    gmsg.html = content
                    break
        return gmsg

    def _send(self, message):
        try:
            message = self._copy_message(message)
        except (ValueError, aeemail.InvalidEmailError), err:
            import logging
            logging.warn(err)
            if not self.fail_silently:
                raise
            return False
        if self.can_defer:
            self._defer_message(message)
            return True
        try:
            message.send()
        except (aeemail.Error, apiproxy_errors.Error):
            if not self.fail_silently:
                raise
            return False
        return True

    def _defer_message(self, message):
        from google.appengine.ext import deferred
        from django.conf import settings
        queue_name = getattr(settings, 'EMAIL_QUEUE_NAME', 'default')
        deferred.defer(_send_deferred,
            message,
            fail_silently=self.fail_silently,
            _queue=queue_name)


class AsyncEmailBackend(EmailBackend):
    can_defer = True