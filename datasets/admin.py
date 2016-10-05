from django.contrib import admin
from datasets.models import Spam, NotSpam, NotEval, NotEvalAdmin
# Register your models here.


admin.site.register(Spam)
admin.site.register(NotSpam)
admin.site.register(NotEval, NotEvalAdmin)
