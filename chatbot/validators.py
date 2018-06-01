from django.core.exceptions import ValidationError


class SenderChoicesValidator(object):
    def __init__(self, error_class=ValidationError):
        self.error_class = error_class

    def __call__(self, sender):
        from .models import Message
        if not next(filter(lambda x: x[0] == sender, Message.sender_choices), False):
            message = f'{sender} is not a valid sender choice for Message'
            raise self.error_class(message)
