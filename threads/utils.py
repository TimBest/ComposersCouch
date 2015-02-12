# -*- coding:utf-8 -*-
import datetime
import re

from django.conf import settings
from django.core.cache import cache
from django.template import Context
from django.template.loader import get_template

from . import settings as tm_settings


# favour django-mailer but fall back to django.core.mail
if tm_settings.MESSAGES_USE_SENDGRID:
    import sendgrid_parse_api

from django.core.mail import send_mail

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.datetime.now


def fill_count_cache(user):
    from .models import inbox_count_for
    cache.set(tm_settings.INBOX_COUNT_CACHE % user.pk,
              inbox_count_for(user), tm_settings.INBOX_COUNT_CACHE_TIME)


def open_message_thread(recipients, subject, template,
                        sender, context={}, send=True, message=None):
    body = ''
    if template:
        t = get_template(template)
        body = t.render(Context(context))
    else:
        body = message

    from forms import ComposeForm  # temporary here to remove circular dependence
    compose_form = ComposeForm(data={
        "recipient": recipients,
        "subject": subject,
        "body": body
    })
    if compose_form.is_valid():
        (thread, new_message) = compose_form.save(sender=sender, send=send)

    return (thread, new_message)

def create_thread(participants, sender, subject, body):
    from .models import Message, Thread, Participant
    # ensure the participants are unique
    participants = list(set(participants))
    message = Message.objects.create(
                body=body,
                sender=sender,
                parent_msg=None,
                sent_at=now(),
    )
    thread = Thread.objects.create(
        subject=subject,
        latest_msg=message,
        creator=sender,
    )
    thread.all_msgs.add(message)
    thread.save()
    for user in participants:
        if user != sender:
            participant = Participant.objects.create(thread=thread, user=user)
        else:
            participant = Participant.objects.create(
                            thread=thread,
                            user=user,
                            read_at=now(),
                            replied_at=now(),
            )
    return thread


def reply_to_thread(thread, sender, body):
    from .models import Message, Participant
    new_message = Message.objects.create(body=body, sender=sender)
    new_message.parent_msg = thread.latest_msg
    thread.latest_msg = new_message
    thread.all_msgs.add(new_message)
    thread.replied = True
    thread.save()
    new_message.save()

    recipients = []
    for participant in thread.participants.all():
        participant.deleted_at = None
        participant.save()
        if sender != participant.user:  # dont send emails to the sender!
            recipients.append(participant.user)

    sender_part = Participant.objects.get(thread=thread, user=sender)
    sender_part.replied_at = sender_part.read_at = now()
    sender_part.save()

    invalidate_count_cache(Message, new_message)

    return (thread, new_message)


def get_lines(body):
    body = body.replace('\r', ' ')
    lines = [x.strip() for x in body.splitlines(True)]
    return lines

def email(subject_template, message_template, recipient_list, object, action, site):
    """Compose and send an email."""
    ctx_dict = {'site': site, 'object': object, 'action': action}
    subject = render_to_string(subject_template, ctx_dict)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    message = render_to_string(message_template, ctx_dict)
    # during the development phase, consider using the setting: EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)

def strip_mail(body):

    custom_line_no = None

    lines = get_lines(body)

    has_signature = False
    for l in lines:
        if l.strip().startswith('>'):
            has_signature = True

    # strip signature -- only if there is a signature. otherwise all is stripped
    if has_signature:
        for l in reversed(lines):
            lines.remove(l)
            if l.strip().startswith('>'):
                break

    # strip quotes
    for i, l in enumerate(lines):
        if l.lstrip().startswith('>'):
            if not custom_line_no:
                custom_line_no = i - 1
                popme = custom_line_no
                while not lines[popme]:
                    lines.pop(popme)
                    popme -= 1
                if re.search(r'^.*?([0-1][0-9]|[2][0-3]):([0-5][0-9]).*?$', lines[popme]) or re.search(r'[\w-]+@([\w-]+\.)+[\w-]+', lines[popme]):
                    lines.pop(popme)
                break

    stripped_lines = [s for s in lines if not s.lstrip().startswith('>')]

    # strip last empty string in the list if it exists
    if not stripped_lines[-1]:
        stripped_lines.pop()

    # stripped message
    return ('\n').join(stripped_lines)


def invalidate_count_cache(sender, message, recipients=None, **kwargs):
    for thread in message.thread.select_related().all():
        for participant in thread.participants.exclude(user=message.sender):
            fill_count_cache(participant.user)
