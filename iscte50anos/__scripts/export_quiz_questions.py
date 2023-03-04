from quiz.models import Question, QuizImage, Choice
from topics.models import Topic

questions = Question.objects.all()
images = QuizImage.objects.all()
csvData = ""

for question in questions:
    try:
        imageLink = question.image.link
    except:
        imageLink = ""

    correct_choice = Choice.objects.filter(question=question.pk, is_correct=True)
    correct_choice_str = ""
    if len(correct_choice) > 1:
        for choice in correct_choice:
            correct_choice_str += f"{choice.text};"
    elif len(correct_choice) == 1:
        correct_choice_str = correct_choice[0].text
    
    question_topics=question.topics
    print(question_topics)

    #line:str = f"\"{question.pk}\";\"{question.text}\";\"{imageLink}\";\"{correct_choice_str}\";\"{question_topics}\""
    line:str = f"\"{question.pk}\";\"{question.text}\";\"{imageLink}\";\"{correct_choice_str}\""
    csvData += line + "\n"
    print(line)

with open("quiz_export.csv", mode="w", encoding="utf-8") as f:
    f.write("question.pk;question.text;imageLink;correct_choice_str\n")
    f.write(csvData)