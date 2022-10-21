from django.db import models
from content.models import Content
import json
import requests
from threading import Thread
 

links = Content.objects.values("link")
links_length : int= len(links)
last_progress_str : str = ""

resultsDict = {"errors":{}}



def check_link(link:dict,externalDict:dict ):
    #internal_dict = {"errors":{}}
    try:
        linkUrl = link["link"]
        statusCode: int = requests.get(linkUrl).status_code
        
        if(statusCode != 200):
            externalDict[statusCode].append(link["link"])
    except KeyError:
        externalDict[statusCode] = []
        externalDict[statusCode].append(link["link"])
    except  Exception as e :
        #print(e)
        externalDict["errors"][linkUrl] = f"{e}"
        #print(f"Adding error: {e}\n {internal_dict}")
    #finally:
        #externalDict.update(internal_dict)
        #print("internal_dict: {internal_dict}")
        #print("externalDict: {externalDict}")



try:
    threads = list()
    for link in links:
        thread = Thread(target=check_link, args=( link, resultsDict ))
        threads.append(thread)

    print(f'Created {len(threads)} threads')
    # start threads
    for thread in threads:
        thread.start()
    # wait for threads to finish
    threads_max=len(threads)-1
    for index,thread in enumerate(threads):
        thread.join()
        print(" " * len(last_progress_str),end="\r")
        progress = f"{index}/{threads_max}"
        last_progress_str = progress
        print(f"\r{progress}",end="")

except Exception as e :
        print(e)
finally:
    print(end="\r")
    print(" " * len(last_progress_str), end='\r')
    print(json.dumps(resultsDict, indent=4))

    with open('check_broken_content_links.json', 'w',encoding='UTF8') as f:
        f.write(json.dumps(resultsDict, indent=4))



