import json

from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django.utils.module_loading import import_string
from channels.sessions import channel_session
from channels import Group

from . import messages
from . import conf
from .chatbot import ChatterBot


@channel_session
def on_connect(message):
    payload = message.content['text']
    message.channel_session['user'] = payload['username']
    message.reply_channel.send(messages.system(_('Welcome to the chat!')))
    Group('chat_%(username)s' % payload).send(messages.system(_('User %(username)s joined chat') % payload))
    Group('chat_%(username)s' % payload).add(message.reply_channel)


@channel_session
def on_disconnect(message):
    Group('chat').discard(message.reply_channel)
    Group('chat').send(messages.system(
        _('User %(user)s left chat') % message.channel_session))


@channel_session
def on_message(message):
    payload = message.content['text']
    user = message.channel_session['user']
    text = payload['text']
    text_type = payload['message_type']
    if text_type == 'message':
        message = messages.info(text, user)
        Group('chat_%s' % user).send(message)
        response = ChatterBot().get_response(text, None)
        Group('chat_%s' % user).send(messages.system(response['text']))
    else:
        ChatterBot().train(text)
        Group('chat_%s' % user).send(messages.system(text, message_type="training"))


@channel_session
def on_command(message):
    payload = message.content['text']
    user = message.channel_session['user']
    command, *args = payload['text'].strip().split()

    if command == '/me' and len(args) >= 1:
        text = ' '.join(args)
        message = messages.info('{} {}'.format(user, text))
        Group('chat').send(message)

    else:
        msg = messages.system(
            _(
                'Error: no such command %(command)s '
                'with arguments "%(args)s"'
            ) % {'command': command, 'args': ' '.join(args)})
        message.reply_channel.send(msg)


def get_engine():
    return import_string(conf.CHAT_ENGINE)
