import requests
from fake_useragent import UserAgent
from lxml import etree
from lxml.html.clean import clean_html

# once we have links for individual pages, extract the information from the pages
sample_post = "http://dribbble.com/shots/11322751-Washing-machine"
sample_post2 = "http://dribbble.com/shots/11290639-Still-life"
ua = UserAgent()
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "user-agent": ua.random,
}

# res = requests.get(sample_post, headers=headers)
# source = clean_html(res.content.decode(res.encoding))


def parse_post(url):
    res = requests.get(url, headers=headers)
    #source = clean_html(res.content.decode(res.encoding))
    source = res.content
    tree = etree.HTML(source)
    data = {}
    # image link
    data['url'] = url
    # image/video link
    media_path = "//div[@class='media-content']//img | //div[@class='media-content']//video"
    # get from meta
    # media_path = "//meta"
    media_nodes = tree.xpath(media_path)
    try:
        print(media_nodes[0].attrib['data-src'])
        data['media file'] = media_nodes[0].attrib['data-src']
    except:
        print("Media file not found")

    # short description
    desc_path = "//div[@class='shot-desc']//p//text()"
    desc_nodes = tree.xpath(desc_path)
    short_description = ""
    for d in desc_nodes:
        short_description += d
        # if d.text:
        #     short_description += d.text
    print(short_description)
    data['short description'] = short_description

    # comment section

    return data


parse_post(sample_post)
