
def sure_prompt():
    try:
        choice = int(input("\nAre you sure? 1 for Yes, 2 for No:"))
        return choice == 1
    except:
        return False


while True:
    print("\nScripts\n")
    print("1: Import Timeline, Events and Content")
    print("2: Import Spots")
    print("3: Delete Logs")
    print("4: Create Levels")
    print("5: Delete Quiz Data")
    print("6: Check Broken Content Links")
    print("7: Export Quiz Questions")
    print("8: Import Quiz Question types")
    print("9: Fix Question images")
    print("10: Sync Questions")
    print("11: Import Quiz Questions")

    script = int(input())
    if script == 1:
        if sure_prompt():
            from __scripts import import_timeline_events_content
    elif script == 2:
        if sure_prompt():
            from __scripts.openday import import_spots
    elif script == 3:
        if sure_prompt():
            from __scripts import delete_logs
    elif script == 4:
        if sure_prompt():
            from __scripts import create_levels
    elif script == 5:
        if sure_prompt():
            from __scripts import delete_quiz_data
    elif script == 6:
        if sure_prompt():
            from __scripts import check_broken_content_links
    elif script == 7:
        if sure_prompt():
            from __scripts import export_quiz_questions
    elif script == 8:
        if sure_prompt():
            from __scripts import import_quiz_question_types
    elif script == 9:
        if sure_prompt():
            from __scripts import fix_quiz_images
    elif script == 10:
        if sure_prompt():
            from __scripts import sync_questions
    elif script == 11:
        if sure_prompt():
            from __scripts import import_quiz_questions_NEI

    exit(0)