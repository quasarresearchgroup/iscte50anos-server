from quiz.models import QuizImage
import requests
from bs4 import BeautifulSoup

images = QuizImage.objects.all()

def fix_image_link(link:str)-> str:
    if "flic.kr" in link:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        url = soup.find("meta", property="og:url")
        print(url["content"])
        return url["content"]
    return link

for image in images:
    newlink:str = fix_image_link(image.link)
    image.link = newlink
    image.save()
