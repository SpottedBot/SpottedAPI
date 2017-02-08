from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
# Create your models here.


class Pending(models.Model):
    message = models.TextField()
    is_safe = models.BooleanField(default=True)
    suggestion = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Pending " + str(self.id)


class Approved(models.Model):
    message = models.TextField()
    is_safe = models.BooleanField(default=True)
    suggestion = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    by_api = models.BooleanField(default=False)

    def __str__(self):
        return "Approved " + str(self.id)


class Rejected(models.Model):
    message = models.TextField()
    is_safe = models.BooleanField(default=True)
    suggestion = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    by_api = models.BooleanField(default=False)
    reason = models.CharField(max_length=100)

    def __str__(self):
        return "Rejected " + str(self.id)


class Deleted(models.Model):
    message = models.TextField()
    is_safe = models.BooleanField(default=True)
    suggestion = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    by_api = models.BooleanField(default=False)  # Is going to be true if the spotted was approved by the api
    reason = models.CharField(max_length=100)
    by = models.CharField(max_length=100)

    def __str__(self):
        return "Deleted " + str(self.id)


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
