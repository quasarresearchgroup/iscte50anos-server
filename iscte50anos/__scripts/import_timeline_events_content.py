
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
p_contents = Path(__file__).parent / 'files' / 'Cronologia Cinquentenário.xlsx - CONTEÚDOS.tsv'


def translate_scope(scope):
    if scope == "Iscte":
        return "iscte"
    if scope == "Portugal" or scope == "Nacional":
        return "portugal"
    else:
        return "world"


def import_contents() -> dict[str,list[str]] :
    content_map = {} #:defaultdict[str,list[str]] = defaultdict(list)
    with p_contents.open() as csvfile:
        content_reader = csv.reader(csvfile, delimiter="\t")
        header = next(content_reader)
        for row in content_reader:
            content_map[row[1].strip()].append(row[0::])
    print(f"lenght of contents map: {len(content_map)}")
    dictMap = dict(content_map)
    return dictMap

def create_events(map:dict):
    Event.content.through.objects.all().delete()
    Event.topics.through.objects.all().delete()
    Event.objects.all().delete()

    Content.topics.through.objects.all().delete()
    Content.objects.all().delete()
    Topic.objects.all().delete()
    
    with p_eventos.open() as csvfile:
        topic_counter:int = 0
        timeline_reader = csv.reader(csvfile, delimiter="\t")
        header = next(timeline_reader)
        content_id =0
        for index,eventRow in enumerate(timeline_reader):
            date = datetime.strptime(eventRow[0], '%Y-%m-%d')
            # print(row)
            event, created = Event.objects.get_or_create(id=index, date = date, title = eventRow[2].strip() )
            topics_list = []
            for x in eventRow[4::]:
                if x:
                    stored_topic,created = Topic.objects.get_or_create(title=x)
                    topic_counter+=1
                    topics_list.append(stored_topic)
            # print(f"topics_list:{topics_list}")
            event.topics.clear()
            event.topics.set(topics_list)
            topics_list.clear()


            title:str = event.title
            # print(f"--- {event} --- ")
            content_list = []
            try:
                for content in map[title]:
                    # print(content)
                    if(  content[5] and "http" in content[5] ):
                        stored_content,created  = Content.objects.get_or_create(id=content_id,title=content[3],type= content[4] , link=content[5])
                        content_id+=1
                        content_list.append(stored_content)
                # print(f"content_list:{content_list}")
            except KeyError: 
               print(f"KeyError f{content}")
            event.content.clear()
            event.content.set(content_list)
            content_list.clear()


contents_map = import_contents()
print(f"number of contents: {len(Content.objects.all())}")
with open('filename.json', 'w',encoding='utf-8') as f:
    encoded_data=json.dumps(dict(contents_map), indent=4)
    f.write(encoded_data)
    # print(json.dumps(dict(contents_map), indent=4),file=f)

create_events(map=contents_map )
print("completed imports")
