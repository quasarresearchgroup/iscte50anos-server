from django.contrib import admin

# Register your models here.
from quiz.models import Question, Quiz, Choice, QuizQuestion, QuizImage, Trial

admin.site.site_header = '50 Anos Iscte'

class ChoiceInline(admin.TabularInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
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
admin.site.register(Trial)

print("-------Admin quiz-------------")
quiz = Quiz.objects.get(user__username="admin")

print(quiz.questions.all())

print("--------------------")