import requests
from bs4 import BeautifulSoup

def get_UA(path):
    url = "https://udger.com" + path
    r = requests.get(url)
    soap = BeautifulSoup(r.content, "lxml")

    example = soap.find("b", text="Useragentstring example")
    for ua in example.find_next_siblings("p"):
        if ua:
            print ua.get_text()


def list_UA():
    url = "https://udger.com/resources/ua-list#Browser"
    href_tag = "a[href^=/resources/ua-list/browser-detail?browser=]"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")

    for href in soup.select(href_tag):
        if href:
            get_UA(href.get('href'))


def main():
    list_UA()

if __name__ == "__main__":
    main()
