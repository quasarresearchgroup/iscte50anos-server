from collections import defaultdict
import csv
from datetime import datetime

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

def import_contents() -> defaultdict[str,list[str]] :
    map:defaultdict[str,list[str]] = defaultdict(list)
    with p_contents.open() as csvfile:
        content_reader = csv.reader(csvfile, delimiter="\t")
        header = next(content_reader)
        for row in content_reader:
            map[row[1]].append(row[0::])
    return map

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
        for index,row in enumerate(timeline_reader):
            date = datetime.strptime(row[0], '%Y-%m-%d')
            # print(row)
            event = Event.objects.create(id=index, date = date, title = row[2] , )
            topics_list = []
            for x in row[4::]:
                if x:
                    # print(x)
                    # print(type(x))
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
            for content in map[title]:
                # print(content)
                if( content[4] and  content[5] ):
                    stored_content,created  = Content.objects.get_or_create(title=content[3],type= content[4] , link=content[5])
                    content_list.append(stored_content)
            # print(f"content_list:{content_list}")
            event.content.clear()
            event.content.set(content_list)
            content_list.clear()

contents_map = import_contents()
# with open('filename.txt', 'w') as f:
    # print(contents_map,file=f)
create_events(map=contents_map )
