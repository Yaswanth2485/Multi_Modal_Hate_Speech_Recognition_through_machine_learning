from django.contrib import admin
from .models import registrationmodel




class registredusers(admin.ModelAdmin):
  list_display = ("name", "email", "mobile","status")  
admin.site.register(registrationmodel, registredusers)







