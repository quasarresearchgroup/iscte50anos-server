from django.contrib import admin

# Register your models here.
from quiz.models import Question, Quiz, Choice, QuizImage, Trial, TrialQuestion

admin.site.site_header = '50 Anos Iscte'

class ChoiceInline(admin.TabularInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]
    list_filter = [
         "topics"
    ]
    search_fields = ['text', 'image__description']


class TrialQuestionInline(admin.TabularInline):
    model = TrialQuestion


class TrialAdmin(admin.ModelAdmin):
    inlines = [
        TrialQuestionInline,
    ]


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizImage)

# TEST
admin.site.register(Quiz)
admin.site.register(Trial, TrialAdmin)
admin.site.register(TrialQuestion)

'''
print("-------Admin quiz-------------")
quiz = Quiz.objects.get(user__username="admin")

print(quiz.questions.all())

print'("--------------------")
'''