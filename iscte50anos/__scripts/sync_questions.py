from collections import defaultdict
import csv
from datetime import datetime
import json
from typing import Optional

from events.models import Event
from pathlib import Path

from quiz.models import Question , Choice, QuizImage

p_quiz = Path(__file__).parent / 'files' / 'Cronologia Cinquentenário - QUIZ.tsv'
SAVETODBGUARD:bool = True


def translate_question_category(category:str)->Optional[str]:
# AutoExplicativa
    if category == "AutoExplicativa":
        return "self_explanatory"
# Quotidiano
    if category == "Quotidiano":
        return "daily_life"
# Georeferenciação
    if category == "Georeferenciação":
        return "georeferencing"
# Cronologia
    if category == "Cronologia":
        return "chronology"
# Dimensões
    if category == "Dimensões":
        return "dimensions"
    else:
        return None

def generateJsonWithDiffs() -> dict:
    questionsJson={"remove":{},"sync":{}}
    with p_quiz.open(encoding='UTF8') as quizFile:
        quiz_reader = csv.reader(quizFile, delimiter="\t")
        header = next(quiz_reader)

        for index,quizRow in enumerate(quiz_reader):
            # print(quizRow)
            csv_question_id:int = int(quizRow[0])
            csv_question_string:str = quizRow[1]
            csv_question_image_link:str = quizRow[2]
            csv_question_correct_choice:str = quizRow[4]
            csv_question_category:str = translate_question_category(quizRow[5])
            csv_question_state:str = quizRow[7]
            csv_question_dict = {
                "question_text":csv_question_string,
                "question_category":csv_question_category,
                "question_image_link":csv_question_image_link,
                "correct_choice":csv_question_correct_choice,
                "state":csv_question_state,
                }

            for db_question in  Question.objects.filter(pk=csv_question_id):
                db_question_id = db_question.id
                db_question_text = str(db_question.text)
                db_question_category = str(db_question.category)
                db_question_image_link = str(db_question.image_link())

                correct_choice = Choice.objects.filter(question=db_question_id, is_correct=True)
                db_question_correct_choice = ""
                if len(correct_choice) > 1:
                    for choice in correct_choice:
                        db_question_correct_choice += f"{choice.text};"
                elif len(correct_choice) == 1:
                    db_question_correct_choice = correct_choice[0].text

                db_question_dict = {
                    "question_text":str(db_question_text),
                    "question_category":str(db_question_category),
                    "question_image_link":str(db_question_image_link),
                    "correct_choice":str(db_question_correct_choice),
                    }


                if (db_question_text != csv_question_string  or
                    db_question_category != csv_question_category  or
                    db_question_image_link != csv_question_image_link  or
                    db_question_correct_choice != csv_question_correct_choice  or
                    csv_question_state == "Não Colocar"):
                        
                    if (csv_question_state == "Não Colocar"):
                        questionsJson["remove"].update({db_question_id:{
                        "db":db_question_dict,
                        "csv":csv_question_dict
                        }})
                    else:
                        questionsJson["sync"].update({db_question_id:{
                            "db":db_question_dict,
                            "csv":csv_question_dict,
                            "diff":{}
                            }})

                        if db_question_text != csv_question_string  :
                            questionsJson["sync"][db_question_id]["diff"].update({
                                "question_text":{
                                    "db": db_question_text,
                                    "csv": csv_question_string
                                    }})

                        if db_question_category != csv_question_category  :
                            questionsJson["sync"][db_question_id]["diff"].update({
                                "question_category":{
                                    "db": db_question_category,
                                    "csv": csv_question_category
                                    }})

                        if db_question_image_link != csv_question_image_link  :
                            questionsJson["sync"][db_question_id]["diff"].update({
                                "question_image_link":{
                                    "db": db_question_image_link,
                                    "csv": csv_question_image_link
                                    }})

                        if db_question_correct_choice != csv_question_correct_choice :
                            questionsJson["sync"][db_question_id]["diff"].update({
                                "correct_choice":{
                                    "db": db_question_correct_choice,
                                    "csv": csv_question_correct_choice
                                    }})
                            


                #db_question.save()
        return questionsJson


def synchronizeDbWithDict(questionsDict:dict)->None:

    toRemoveIDs = [id for id,_ in questionsDict["remove"].items()]
    print(f"You are about to REMOVE {len(toRemoveIDs)} questions with ids: {toRemoveIDs}")
    toUpdateIDs = [id for id,_ in questionsDict["sync"].items()]
    print(f"You are about to UPDATE {len(toUpdateIDs)} questions with ids: {toUpdateIDs}")

    savetoDb:bool = sure_prompt()
    if not savetoDb:
        print("No changes saved to the db, exiting...")
        return
    print("Updating...")

    for id in toRemoveIDs:
        Question.objects.filter(id=id).delete()

    for id,value in questionsDict["sync"].items():
        csv = value["csv"]
        db = value["db"]
        sync = value["diff"]
        storedQuestion = Question.objects.get(pk=id)

        questionTextField = 'question_text'
        questionCategoryField = 'question_category'
        questionImageLinkField = 'question_image_link'
        correctChoiceField = "correct_choice"

        print(f"id:{id}")
        print(f"\t{storedQuestion}")

        if "question_text" in sync:
            print(f"\t updating question_text for index nr {id}")
            print(f"\t db: question_text: {db[questionTextField]}")
            print(f"\t csv: question_text: {csv[questionTextField]}")
            if SAVETODBGUARD and savetoDb:
                storedQuestion.text = csv[questionTextField]
                storedQuestion.save()
                print(f"saved question_text {storedQuestion.text}")


        if "question_category" in sync:
            print(f"\t updating question_category for index nr {id}")
            print(f"\t db: question_category: {db[questionCategoryField]}")
            print(f"\t csv: question_category: {csv[questionCategoryField]}")
            
            if SAVETODBGUARD and savetoDb:
                storedQuestion.category = csv[questionCategoryField]
                storedQuestion.save()
                print(f"saved question_category {storedQuestion.category}")

        if "question_image_link" in sync:
            print(f"\tupdating question_image_link for index nr {id}")
            print(f"\t db: question_image_link: {db[questionImageLinkField]}")
            print(f"\t csv: question_image_link: {csv[questionImageLinkField]}")
            print(storedQuestion.image)
            if(storedQuestion.image is None):
                print("No image set, creating new one")
                if SAVETODBGUARD and savetoDb:
                    newImage = QuizImage.objects.create(
                        description=db[correctChoiceField],
                        link=csv[questionImageLinkField],
                    )
                    storedQuestion.image = newImage
                    newImage.save()
                    storedQuestion.save()
                    storedQuestion.image.save()
                    print(f"saved new image {storedQuestion.image}")
            else:
                storedQuestion.image.link = csv[questionImageLinkField]
                if SAVETODBGUARD and savetoDb:
                    storedQuestion.image.save()
                    storedQuestion.save()
                    print(f"saved new image link {storedQuestion.image}")

        if "correct_choice" in sync:
            print(f"\t updating correct_choice for index nr {id}")
            print(f"\t db: correct_choice: {db[correctChoiceField]}")
            print(f"\t csv: correct_choice: {csv[correctChoiceField]}")

            correct_choices = Choice.objects.filter(question=id, is_correct=True)
            other_choices = Choice.objects.filter(question=id, is_correct=False)

            if len(correct_choices) > 0:
                print(f"correct_choice {correct_choices}")
                correct_choices[0].text = csv[correctChoiceField]
                if SAVETODBGUARD and savetoDb:
                    correct_choices[0].save()
                    print("saved new correct_choice text")
            else:
                if len(other_choices) == 0:
                    print(f"other_choices: {other_choices}")
                    print("QUESTION WITHOUTH CHOICES NEED TO CREATE MORE (CORRECT CHOICE ALREADY ADDED FROM CSV)")
                if SAVETODBGUARD and savetoDb:
                    newChoice = Choice.objects.create(
                        question=storedQuestion,
                        text=csv[correctChoiceField],
                        is_correct=True,
                    )
                    newChoice.save()
                    print(f"saved new correct_choice: {newChoice}")


        print ("="*20)


def sure_prompt()-> bool:
    try:
        choice = int(input("Are you sure? 1 for Yes, 2 for No:"))
        return choice == 1
    except:
        return False

changesJson = generateJsonWithDiffs()
synchronizeDbWithDict(changesJson)

with open("db_question_test.json", mode="w", encoding="UTF8") as f:
    f.write(json.dumps(changesJson,indent=2))
