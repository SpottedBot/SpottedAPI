from django.db import models
from .validators import SenderChoicesValidator
# Create your models here.


class Chat(models.Model):
    conversation_id = models.CharField(unique=True, max_length=32)
    created = models.DateTimeField(auto_now_add=True)
    origin = models.CharField(max_length=30)

    def append_message(self, text, sender):
        SenderChoicesValidator()(sender)
        Message.objects.create(
            chat=self,
            text=text,
            sender=sender
        )

    def log_generator(self):
        messages = self.message_log.all()
        for message in messages:
            yield message.display_text

    def get_full_log(self):
        full_log = f"{self.created.strftime('%d %b %H:%M')} Chat {self.conversation_id} ({self.origin}):\n"
        log = self.log_generator()
        for message in log:
            full_log += message + '\n'
        return full_log

    @property
    def full_log(self):
        return self.get_full_log()

    def __str__(self):
        return f"Chat {self.conversation_id} from {self.origin}"


class Message(models.Model):
    sender_choices = (('page', 'Page'), ('user', 'User'))

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='message_log',
        blank=True
    )
    text = models.TextField()
    sender = models.CharField(choices=sender_choices, max_length=10)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def index(self):
        return self.chat.message_log.filter(created__lt=self.created).count()

    @property
    def display_text(self):
        return f"{self.created.strftime('%d %b %H:%M')} {self.get_sender_display()} says:\n{self.text}"

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"Message {self.index} ({self.get_sender_display()}) from {str(self.chat)}"
