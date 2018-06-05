
from django.contrib import admin
from library.models import *
# Register your models here.
admin.site.register(Client)
admin.site.register(Library)
admin.site.register(Book)
admin.site.register(SeminarRoom)
admin.site.register(SeminarUse)
admin.site.register(Staff)
admin.site.register(BookChecked)
admin.site.register(BookRequest)
