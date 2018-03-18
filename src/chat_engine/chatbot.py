# from django.conf import settings
import json
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings


class ChatterBot(object):
    """
    Subclass this mixin for access to the 'chatterbot' attribute.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT)

    def get_response(self, text, conversation_id=None):
        conversation = self.get_conversation(conversation_id)

        response = self.chatterbot.get_response(text, conversation.id)
        response_data = response.serialize()
        return response_data

    def prepare_train_text(self, text):
        # import pdb; pdb.set_trace()
        train = []
        try:
            train_array = json.loads(text)
            for key in train_array.keys():
                for item in train_array[key]:
                    train.append(key)
                    train.append(item)
        except Exception as e:
            train_array = [phrase for phrase in text.splitlines()]
            if len(train_array) > 1:
                if len(train_array) > 3 and train_array[1] == '' and train_array[2] == '':
                    for item in train_array[3:]:
                        train.append(train_array[0])
                        train.append(item)
                else:
                    train = train_array
            else:
                train = []
        return train


    def train(self, text):
        # train = [phrase for phrase in text.split(',')]
        train = self.prepare_train_text(text)
        self.chatterbot.train(train)

    def get_conversation(self, conversation_id=None):
        """
        Return the conversation for the session if one exists.
        Create a new conversation if one does not exist.
        """
        from chatterbot.ext.django_chatterbot.models import Conversation, Response

        class Obj(object):
            def __init__(self):
                self.id = None
                self.statements = []

        conversation = Obj()

        # conversation.id = request.session.get('conversation_id', 0)
        existing_conversation = False
        try:
            Conversation.objects.get(id=conversation.id)
            existing_conversation = True

        except Conversation.DoesNotExist:
            conversation_id = self.chatterbot.storage.create_conversation()
            # request.session['conversation_id'] = conversation_id
            conversation.id = conversation_id

        if existing_conversation:
            responses = Response.objects.filter(
                conversations__id=conversation.id
            )

            for response in responses:
                conversation.statements.append(response.statement.serialize())
                conversation.statements.append(response.response.serialize())

        return conversation
