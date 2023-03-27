from quiz.models import QuizImage
import requests
from bs4 import BeautifulSoup

images = QuizImage.objects.all()

for image in images:
    if "flic.kr" in image.link:
        response = requests.get(image.link)
        soup = BeautifulSoup(response.text, 'html.parser')
        url = soup.find("meta", property="og:url")
        print(url)
        image.link = url["content"]
        image.save()

