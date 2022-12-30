from quiz.models import Question, QuizImage
from topics.models import Topic

questions = Question.objects.all()
images = QuizImage.objects.all()
csvData = ""

for question in questions:
    try:
        imageLink = question.image.link
    except:
        imageLink = ""
    line = f"\"{question.pk}\", \"{question.text}\" , \"{imageLink}\""
    csvData += line + "\n"
    print(line)


f = open("quiz_export.csv",mode= "w",encoding="utf-8")
f.write(csvData)
f.close()