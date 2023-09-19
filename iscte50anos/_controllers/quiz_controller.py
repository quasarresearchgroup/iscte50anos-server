import random
from quiz.models import Quiz, Question, TrialQuestion
from topics.models import TopicAccess, Topic

from users.models import Profile, Level

QUIZ_SIZE = 5


# QUIZ_SIZE = 8

# TODO change for final version
def update_level(user):
    profile = Profile.objects.get(user=user)
    num_accessed_topics = TopicAccess.objects.filter(user=user).count()

    next_level = Level.objects.get(num_topics=num_accessed_topics)
    if next_level.number != profile.level:
        Profile.objects.filter(user=user).update(level=next_level.number)

        #create_quiz(user)
        create_quiz_single_topic(user, next_level)


def create_quiz_single_topic(user, level):
    last_topic_access = TopicAccess.objects.filter(user=user).select_related("topic").latest("when")
    topic = last_topic_access.topic

    # Create quiz for the visited topics
    quiz = Quiz.objects.create(user=user, number=level.number)
    quiz.topics.set([topic])


def create_quiz(user):
    topic_accesses = TopicAccess.objects.filter(user=user).select_related("topic")
    accessed_topics = [t.topic for t in topic_accesses]

    # Create quiz for the  visited topics
    quiz = Quiz.objects.create(user=user, number=len(topic_accesses))
    quiz.topics.set(accessed_topics)

# OLD FUNCTIONS


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


def create_first_quiz(user):
    # Create first quiz with all topics
    quiz = Quiz.objects.create(user=user, number=0)
    quiz.topics.set(Topic.objects.all().exclude(title="Georeferenciação"))


def assign_trial_questions_simple(user, trial, topics):
    # Get all questions not previously associated
    questions = list(Question.objects.filter(topics__in=topics).exclude(trial_questions__trial__quiz__user=user))

    if len(questions) < QUIZ_SIZE:
        middle_questions = list(Question.objects.filter(topics__in=topics))

    questions = questions + random.sample(middle_questions, QUIZ_SIZE)

    trial_questions = []
    question_number = 1
    for question in questions:
        trial_question = TrialQuestion(trial=trial, question=question, number=question_number)
        trial_questions.append(trial_question)
        question_number += 1

    TrialQuestion.objects.bulk_create(trial_questions)


def assign_trial_questions(user, trial, topics):
    # Get all questions not previously associated
    middle_questions = list(Question.objects.filter(topics__in=topics)
                            .exclude(trial_questions__trial__quiz__user=user, category="self_explanatory"))

    first_questions = list(Question.objects.filter(topics__in=topics, category="self_explanatory")
                           .exclude(trial_questions__trial__quiz__user=user))

    if len(middle_questions) < QUIZ_SIZE - 2:
        middle_questions = list(Question.objects.filter(topics__in=topics)
                                .exclude(category="self_explanatory"))
    if len(first_questions) == 0:
        first_questions = list(Question.objects.filter(category="self_explanatory"))

    questions = [random.choice(first_questions)]
    questions = questions + random.sample(middle_questions, QUIZ_SIZE - 2)

    geo_questions = Question.objects.filter(topics__title="Georeferenciação") \
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

def assign_trial_questions_final(user, trial, topics):
    # Get all questions not previously associated
    questions = list(Question.objects.filter(topics__in=topics)
                     .exclude(trial_questions__trial__quiz__user=user))

    # TODO get remaining questions
    if len(questions) < QUIZ_SIZE - 1:
        questions = list(Question.objects.filter(topics__in=topics))

    questions = random.sample(questions, QUIZ_SIZE - 1)

    geo_questions = Question.objects.filter(topics__title="Georeferenciação") \
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
