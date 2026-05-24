from django.contrib import admin
from .models import Question, QuestionSource


class QuestionSourceInline(admin.TabularInline):
    model = QuestionSource
    extra = 0
    readonly_fields = ('document', 'relevant_chunk')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'created_at')
    search_fields = ('question_text', 'answer_text')
    readonly_fields = ('answer_text', 'created_at')
    inlines = [QuestionSourceInline]
