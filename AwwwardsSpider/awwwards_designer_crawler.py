import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from fake_useragent import UserAgent
from lxml import etree
from lxml.html.clean import clean_html
import json



page = 1  # 48 posts at a time
target_url = f"https://www.awwwards.com/directory/freelance/?page={page}"


def retrieve_urls(url, headers):
    pass

class Awwwards_Designer_Crawler():
    def __init__(self, start_page=1, end_page=10):
        self.ua = UserAgent()
        # update the cookie
        self.headers = {
            "User-Agent": self.ua.random,
        }
        self.url = "https://www.awwwards.com/directory/freelance/?page="
        self.start = start_page
        self.end = end_page

    def retrieve_urls(self, url):
        res = requests.get(url, headers=self.headers)
        source = res.content
        tree = etree.HTML(source)
        designer_path = "//ul[contains(@class, 'list-items')]/li//a[@class='profile-link']"
        designer_nodes = tree.xpath(designer_path)
        designers_url = []
        designers = []
        for node in designer_nodes:
            designers.append(node.text)
            designers_url.append("https://www.awwwards.com" + node.attrib['href'])
        print(designers)
        print(designers_url)

    def run(self):
        for page in range(self.start, self.end+1):
            target = self.url + str(page)
            self.retrieve_urls(target)


if __name__ == "__main__":
    crawler = Awwwards_Designer_Crawler(1, 1)
    crawler.run()