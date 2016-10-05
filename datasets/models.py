from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
# Create your models here.


class Spam(models.Model):
    message = models.TextField()

    def __str__(self):
        return "Spam " + str(self.id)


class NotSpam(models.Model):
    message = models.TextField()

    def __str__(self):
        return "NotSpam " + str(self.id)


class NotEval(models.Model):
    message = models.TextField()
    spam = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None
    )

    def __str__(self):
        return "NotEval " + str(self.id)


class NotEvalAdmin(admin.ModelAdmin):
    def short_message(obj):
        return obj.message[:40]

    def user_name(obj):
        return obj.user.username

    short_message.short_description = 'Message'
    list_display = (short_message, user_name, 'spam')


def create_user_token(sender, instance, created, **kwargs):
    if created:
        t = Token(user=instance)
        t.save()

post_save.connect(create_user_token, sender=User)
