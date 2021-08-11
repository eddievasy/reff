from urllib.parse import urlparse

def url_parser(long_url):
    domain = urlparse(long_url).netloc
    if 'www.' in domain:
        domain=domain.replace('www.','')
    return domain

url_parser("https://www.google.com/search?q=how+amazing+is+life&rlz=1C5CHFA_enGB963GB963&oq=how+amazing+is+life&aqs=chrome..69i57j0i512l9.2338j0j7&sourceid=chrome&ie=UTF-8")

