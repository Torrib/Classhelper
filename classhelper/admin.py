from django.contrib import admin
from models import Subject, Assessment, Tag, SubjectDocument

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'subject_name')

admin.site.register(Subject, SubjectAdmin)

class TagAdmin(admin.ModelAdmin):
    model = Tag

admin.site.register(Tag, TagAdmin)

class SubjectDocumentAdmin(admin.ModelAdmin):
    model = SubjectDocument

admin.site.register(SubjectDocument, SubjectDocumentAdmin)
