from quiz.models import Quiz

quiz = Quiz.objects.get(user__username="admin")
print(quiz)