import random
from quiz.models import Quiz, Question
from topics.models import TopicAccess

from users.models import Profile, Level


def update_level(user):
    profile = Profile.objects.get(user=user)
    num_accessed_topics = TopicAccess.objects.filter(user=user).count()

    next_level = Level.objects.get(min_topics__lte=num_accessed_topics, max_topics__gte=num_accessed_topics)
    if next_level.level != profile.level:
        profile.level = next_level.level
        profile.save()
        create_quiz(user, next_level)


# TODO How to use read topics?
def create_quiz(user, level):
    # If the user does not have a quiz for its current level

    # level = Level.objects.get(profile__user=user)
    if not Quiz.objects.filter(user=user, level=level).exists():
        # Get random questions for accessed topics, user
        topic_accesses = TopicAccess.objects.filter(user=user)
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


# Best out of the trials
# Depending on best trial, subtract percentage of total quiz score (first trial, no subtract. last, more subtract)
# TODO score with puzzle completion
def calculate_user_score_puzzle(user):
    pass


def calculate_user_score(user):
    total_score = 0
    for quiz in user.quizzes:
        quiz_score = 0
        for trial in quiz.trials:
            trial_score = 0
            for trial_question in trial.questions:
                question = trial_question.question
                if question.type == "S":
                    choice = trial_question.answer
                else:
                    pass

        total_score += quiz_score

    return total_score