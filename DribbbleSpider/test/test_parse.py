import requests
from fake_useragent import UserAgent
from lxml import etree
from lxml.html.clean import clean_html

# once we have links for individual pages, extract the information from the pages
sample_post = "http://dribbble.com/shots/11322751-Washing-machine"
sample_post2 = "http://dribbble.com/shots/11290639-Still-life"
sample_post3 = "https://dribbble.com/shots/11780117-2-Reading"
ua = UserAgent()
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "user-agent": ua.random,
}


comment_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "user-agent": ua.random,
    "x-csrf-token": "LVT78lsj/YV8NDO4UJ2dibwBAM/2b9H3MjAWgz+TxskcmM7EHj0ms7jrcW6fl6gQpeg386UqdstI9p4h8BZOcw==",
    "x-requested-with": 'XMLHttpRequest'
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

    # author url
    author_path = "//header[contains(@class,'shot-header')]//div[@class='slat-details']/a[@class='hoverable url']"
    author_nodes = tree.xpath(author_path)
    print("https://dribbble.com" + author_nodes[0].attrib['href'])
    data['author_url'] = "https://dribbble.com" + \
        author_nodes[0].attrib['href']
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
    # comments url: https://dribbble.com/shots/11290639-Still-life/comments
    comment_url = url + '/comments'
    comment_res = requests.get(comment_url, headers=comment_headers)
    comment_tree = etree.HTML(comment_res.content)
    comments_path = "//div[@class='comment-body']/p/text()"
    comment_nodes = comment_tree.xpath(comments_path)
    comments = []
    for comment in comment_nodes:
        if comment.strip():
            comments.append(comment)
    print(",".join(comments))
    data['comments'] = comments

    # tags
    tag_path = "//div[@class='screenshot-stats']/div[@class='shot-tags']/ol/li//text()"
    tag_nodes = tree.xpath(tag_path)
    tags = []
    for tag in tag_nodes:
        if tag.strip():
            tags.append(tag)
    print(",".join(tags))
    data['tags'] = tags

    # color palette
    palette_path = "//div[@class='screenshot-stats']/div[@class='shot-colors']/ul/li[@class='color']/a/text()"
    palette_nodes = tree.xpath(palette_path)
    color_palettes = []
    for color in palette_nodes:
        if color.strip():
            color_palettes.append(color)
    print(",".join(color_palettes))
    data['color palette'] = color_palettes

    # likes
    likes_path = "//div[@class='screenshot-stats']/div[@class='shot-likes']/a/text()"
    likes_node = tree.xpath(likes_path)[0]
    # convert string to integer
    try:
        print(int(likes_node.split()[0]))
        data['number of likes'] = int(likes_node.split()[0])
    except:
        data['number of likes'] = 0

    # number of saves
    saves_path = "//div[@class='screenshot-stats']/div[@class='shot-saves']/a/text()"
    saves_node = tree.xpath(saves_path)[0]
    try:
        print(int(saves_node.split()[0]))
        data['number of saves'] = int(saves_node.split()[0])
    except:
        data['number of saves'] = 0

    # date
    date_path = "//div[@class='screenshot-stats']/div[@class='shot-date']/text()"
    date_node = tree.xpath(date_path)
    date = ""
    for d in date_node:
        if d.strip():
            date += d.strip()
    print(date)
    data['date'] = date

    return data


parse_post(sample_post3)
