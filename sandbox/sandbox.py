from urllib.parse import urlparse

url = "https://stackoverflow.com/questions/35691093/django-how-to-create-a-field-based-on-another-field-in-the-same-model"
url = url.replace(':',' ').replace('.', ' ').replace('/',' ')
url = " ".join(url.split())
print(url)