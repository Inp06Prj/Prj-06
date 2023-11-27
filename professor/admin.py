from django.contrib import admin
from .models import Pro_User, Calendar
    # , ProfessorSchedule

admin.site.register(Pro_User)

# admin.site.register(ProfessorSchedule)
admin.site.register(Calendar)