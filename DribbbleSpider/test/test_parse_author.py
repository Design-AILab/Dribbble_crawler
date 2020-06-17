import requests
from fake_useragent import UserAgent
from lxml import etree

sample_author1 = "https://dribbble.com/Dimest/about"
sample_author2 = "https://dribbble.com/dannniel/about"
sample_author3 = "https://dribbble.com/mintion/about"


ua = UserAgent()
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "user-agent": ua.random,
}


def crawl_author_info(url, headers):
    '''
    Given the about page of a Dribbble user, get the following information:
    - number of shots
    - number of projects
    - number of collections
    - number of liked shots
    - number of followers
    - number of following
    - number of tags
    '''

    res = requests.get(url, headers=headers)
    source = res.content
    tree = etree.HTML(source)
    data = {}

    # number of shots
    shots_path = "//ul[@class='scrolling-subnav-list']/li[contains(@class, 'shots')]/a/span[@class='count']/text()"
    shots_node = tree.xpath(shots_path)
    print(shots_node[0])
    data['shots'] = shots_node[0]

    # number of projects
    projects_path = "//ul[@class='scrolling-subnav-list']/li[contains(@class, 'projects')]/a/span[@class='count']/text()"
    projects_node = tree.xpath(projects_path)
    print(projects_node[0])
    data['projects'] = projects_node[0]

    # number of collections
    collections_path = "//ul[@class='scrolling-subnav-list']/li[contains(@class, 'collections')]/a/span[@class='count']/text()"
    collections_node = tree.xpath(collections_path)
    print(collections_node[0])
    data['collections'] = collections_node[0]

    # number of liked shots
    liked_shots_path = "//ul[@class='scrolling-subnav-list']/li[contains(@class, 'liked shots')]/a/span[@class='count']/text()"
    liked_shots_node = tree.xpath(liked_shots_path)
    print(liked_shots_node[0])
    data['liked shots'] = liked_shots_node[0]

    # number of followers, number of following, number of tags
    stats_path = "//div[@class='about-content-main']//section[contains(@class, 'profile-stats-section')]/a/span[contains(@class,'count')]/text()"
    # it's followers, following, and then tags
    stats_node = tree.xpath(stats_path)
    print(stats_node)
    data['followers'] = stats_node[0]
    data['following'] = stats_node[1]
    data['tags'] = stats_node[2]
    return data


crawl_author_info(sample_author1, headers)
