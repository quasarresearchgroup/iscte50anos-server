
def sure_prompt():
    choice = int(input("\nAre you sure? 1 for Yes, 2 for No:"))
    return choice == 1


while True:
    print("\nScripts\n")
    print("1: Import Timeline, Events and Content")
    print("2: Import Spots")
    print("3: Delete Logs")
    print("4: Create Levels")
    print("5: Delete Quiz Data")
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
    else:
        exit(0)