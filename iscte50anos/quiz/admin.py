from django.contrib import admin

# Register your models here.
from quiz.models import Question, Quiz, Answer, QuizQuestion, QuizImage

admin.site.site_header = '50 Anos Iscte'

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]

class QuestionInline(admin.TabularInline):
    model = QuizQuestion

class QuizAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
    ]


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizImage)

# TEST
admin.site.register(Quiz, QuizAdmin)
