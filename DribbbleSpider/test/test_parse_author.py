import requests
from fake_useragent import UserAgent
from lxml import etree

sample_author1 = "https://dribbble.com/Dimest/about"
sample_author2 = "https://dribbble.com/dannniel/about"
sample_author3 = ""


ua = UserAgent()
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "user-agent": ua.random,
}


def crawl_author_info(url, headers):
    '''

    '''

    res = requests.get(url, headers=headers)

print(crawl_author_info(sample_author1, headers))
