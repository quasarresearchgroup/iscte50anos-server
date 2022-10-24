
# # in manage.py before execute_from_command_line(sys.argv)
# # Generally there is only settings module set up:
# import os
# from iscte50anos.iscte50anos import settings
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

# # Initialize django application
# import django
# django.setup()


from collections import defaultdict
import csv
from datetime import datetime
import json

from events.models import Event
from pathlib import Path

from content.models import Content
from topics.models import Topic

p_eventos= Path(__file__).parent / 'files' / 'Cronologia Cinquentenário.xlsx - EVENTOS.tsv'
p_contents = Path(__file__).parent / 'files' / 'Cronologia Cinquentenário.xlsx - FONTES.tsv'


def translate_scope(scope):
    if scope == "Iscte":
        return "iscte"
    if scope == "Portugal" or scope == "Nacional":
        return "portugal"
    else:
        return "world"



def translate_content_type(scope):
# documento
    if scope == "documento":
        return "document"
# pagina_web
    if scope == "pagina_web":
        return "web_page"
# imagem
    if scope == "imagem":
        return "image"
# musica
    if scope == "musica":
        return "audio"
# video
    if scope == "video":
        return "video"
# pagina_social
    if scope == "pagina_social":
        return "social_media"
# # texto
#     if scope == "texto":
#         return "text"
# # entrevista
#     if scope == "entrevista":
#         return "interview"
    else:
        return "web_page"

def import_contents():
    contents_map: defaultdict[str, list[dir]] = defaultdict(list)
    with p_contents.open(encoding='UTF8') as csvfile:
        content_reader = csv.reader(csvfile, delimiter="\t")
        header = next(content_reader)
        for index, row in enumerate(content_reader):
            mapEntry = {}
            mapEntry["id"] = index + 1
            mapEntry["title"] = row[5]
            mapEntry["type"] = translate_content_type(row[6])
            mapEntry["link"] = row[7]
            contents_map[row[2].strip()].append(mapEntry)
    print(f"length of contents map: {len(contents_map)}")
    dictMap = dict(contents_map)
    return dictMap


def create_events(map:dict):
    Event.objects.all().delete()
    Content.objects.all().delete()
    keyErrors:list = []

    with p_eventos.open(encoding='UTF8') as eventsFile:
        timeline_record_length = sum(1 for line in eventsFile)

    with p_eventos.open(encoding='UTF8') as eventsFile:
        topic_counter: int = 0
        timeline_reader = csv.reader(eventsFile, delimiter="\t")
        header = next(timeline_reader)
        last_progress_str:str=""
        for index,eventRow in enumerate(timeline_reader):
            date = datetime.strptime(eventRow[0], '%Y-%m-%d')
            event, created = Event.objects.get_or_create(id=index+1, date=date, title=eventRow[2].strip(), scope=translate_scope(eventRow[3]))
            topics_list = []
            for x in eventRow[4::]:
                if x:
                    stored_topic, created = Topic.objects.get_or_create(title=x)
                    topic_counter += 1
                    topics_list.append(stored_topic)
            event.topics.clear()
            event.topics.set(topics_list)
            topics_list.clear()

            title: str = event.title
            content_list = []
            try:
                for content in map[title]:
                    if content["link"] and "http" in content["link"]:
                        stored_content,created  = Content.objects.get_or_create(id=content["id"], title=content["title"], type=content["type"] , link=content["link"])
                        content_list.append(stored_content)
            except KeyError: 
                keyErrors.append(title)
            event.content.clear()
            event.content.set(content_list)
            content_list.clear()

            print(" " * len(last_progress_str), end='\r')
            progress:str = f"{round(index/timeline_record_length,4)*100}%"
            last_progress_str = progress
            print(progress ,end="\r" )
        return keyErrors


contents_map = import_contents()
# print(f"number of contents: {len(Content.objects.all())}")
# with open('filename.json', 'w',encoding='UTF8') as f:
    # encoded_data=json.dumps(dict(contents_map), indent=4)
    # f.write(encoded_data)
    # print(json.dumps(dict(contents_map), indent=4),file=f)

keyErrors = create_events(map=contents_map)
print(*keyErrors,sep = "\n")
print(f"{len(keyErrors)} event key errors")
print("completed imports")
