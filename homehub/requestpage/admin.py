from django.contrib import admin
from .models import Request

class RequestAdmin(admin.ModelAdmin):  # add this
  list_display = ('request_type','request_desc','status','phone_number')

# Register your models here.
admin.site.register(Request, RequestAdmin)