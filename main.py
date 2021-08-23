from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re
import sys


def get_ddlinks():
    cleaned_links = []
    for link in links:
        z = re.match("http.*720.*mkv", str(link))
        if z:
            cleaned_links.append(link)

    return cleaned_links


def download():
    cleaned_links = get_ddlinks()
    for url in cleaned_links:
        name = url.split("/")[-1]
        print("Downloading " + name)
        response = requests.get(url, allow_redirects=True, stream=True)

        with open(name, "wb") as f:
            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()


with open('animeurls.txt') as file:
    urls = file.read().splitlines()

for url in urls:
    links = []
    soup = BeautifulSoup(urlopen(url), 'html.parser')
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    download()
