import random
from quiz.models import Quiz, Question, TrialQuestion
from topics.models import TopicAccess, Topic

from users.models import Profile, Level

QUIZ_SIZE = 8


def update_level(user):

    profile = Profile.objects.get(user=user)
    num_accessed_topics = TopicAccess.objects.filter(user=user).count()

    next_level = Level.objects.get(num_topics=num_accessed_topics)
    if next_level.number != profile.level:
        profile.level = next_level.number
        profile.save()
        create_quiz(user)


def create_quiz_old(user, level):
    # If the user does not have a quiz for its current level

    if not Quiz.objects.filter(user=user, level=level).exists():
        # Get random questions for accessed topics, user
        topic_accesses = TopicAccess.objects.filter(user=user).select_related("topic")
        accessed_topics = [t.topic for t in topic_accesses]

        single_questions = list(Question.objects.filter(topics__in=accessed_topics, type="S"))
        multiple_questions = list(Question.objects.filter(topics__in=accessed_topics, type="M"))

        single_questions = random.sample(single_questions, level.num_single_questions)
        print(single_questions)
        multiple_questions = random.sample(multiple_questions, level.num_multiple_questions)
        print(multiple_questions)

        # Create quiz and assign the selected questions
        quiz = Quiz.objects.create(user=user, level=level)
        quiz.questions.set(single_questions + multiple_questions)
        quiz.save()


def create_quiz(user):
    next_quiz_number = Quiz.objects.filter(user=user).count()

    topic_accesses = TopicAccess.objects.filter(user=user).select_related("topic")
    accessed_topics = [t.topic for t in topic_accesses]

    # Create quiz for the  visited topics
    quiz = Quiz.objects.create(user=user, number=next_quiz_number)
    quiz.topics.set(accessed_topics)


def create_first_quiz(user):
    # Create first quiz with all topics
    quiz = Quiz.objects.create(user=user, number=0)
    quiz.topics.set(Topic.objects.all().exclude(title="Georeferenciação"))


def assign_trial_questions(user, trial, topics):

    # Get all questions not previously associated
    questions = list(Question.objects.filter(topics__in=topics)
                     .exclude(trial_questions__trial__quiz__user=user))

    # TODO get remaining questions
    if len(questions) < QUIZ_SIZE - 1:
        questions = list(Question.objects.filter(topics__in=topics))

    questions = random.sample(questions, QUIZ_SIZE-1)

    geo_questions = Question.objects.filter(topics__title="Georeferenciação")\
        .exclude(trial_questions__trial__quiz__user=user)
    geo_question = random.choice(geo_questions)
    questions.append(geo_question)

    trial_questions = []
    question_number = 1
    for question in questions:
        trial_question = TrialQuestion(trial=trial, question=question, number=question_number)
        trial_questions.append(trial_question)
        question_number += 1

    TrialQuestion.objects.bulk_create(trial_questions)


def calculate_user_score(user):
    total_score = 0
    for quiz in user.quizzes.all():
        if quiz.number == 0:
            continue
        total_score += quiz.score()
    return total_score
