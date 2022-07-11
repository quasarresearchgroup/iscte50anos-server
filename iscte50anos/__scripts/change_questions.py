from quiz.models import Question

Question.objects.all().update(type="S")
