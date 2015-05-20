from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_request_email(request,
                       subject_template='request/email_create_request_subject.txt',
                       message_template='request/email_create_request_message.txt',):
    """Compose and send an email."""

    recipient_list = []
    for participant in request.thread.participants.all():
        if participant.user.email and (request.thread.creator != participant.user):
                recipient_list.append(participant.user.email)
    if recipient_list:
        context = { 'request':request, 'domain':'composerscouch.com', 'protocol':'http' }
        subject = render_to_string(subject_template, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        message = render_to_string(message_template, context)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)
