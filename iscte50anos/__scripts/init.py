from quiz.models import Answer, Question

Question.objects.all().delete()
Answer.objects.all().delete()



for i in range(1, 6):

    question = Question.objects.create(text=f"Multiple Answer {i}", type="M")

    Answer.objects.create(text="Answer 1", is_correct=False, question=question)
    Answer.objects.create(text="Answer 2", is_correct=True, question=question)
    Answer.objects.create(text="Answer 3",  is_correct=True, question=question)
    Answer.objects.create(text="Answer 4",  is_correct=False, question=question)

for i in range(1, 6):
    question = Question.objects.create(text=f"Single Answer {i}", type="S")

    Answer.objects.create(text="Answer 1", is_correct=False, question=question)
    Answer.objects.create(text="Answer 2", is_correct=False, question=question)
    Answer.objects.create(text="Answer 3",  is_correct=True, question=question)
    Answer.objects.create(text="Answer 4",  is_correct=False, question=question)


