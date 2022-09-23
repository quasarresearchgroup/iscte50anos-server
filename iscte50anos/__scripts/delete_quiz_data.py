from quiz.models import Question, QuizImage
from topics.models import Topic

Question.objects.all().delete()
QuizImage.objects.all().delete()
Topic.objects.all().delete()
