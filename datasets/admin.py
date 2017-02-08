from django.contrib import admin
from .models import Approved, Pending, Rejected, Deleted, NotEval, NotEvalAdmin
# Register your models here.


admin.site.register(Approved)
admin.site.register(Pending)
admin.site.register(Rejected)
admin.site.register(Deleted)
admin.site.register(NotEval, NotEvalAdmin)
