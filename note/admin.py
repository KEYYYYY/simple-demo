from django.contrib import admin

from .models import Note, NoteBook

admin.site.register(Note)
admin.site.register(NoteBook)
