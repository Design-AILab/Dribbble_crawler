import requests
from fake_useragent import UserAgent
from lxml import etree
from lxml.html.clean import clean_html

# once we have links for individual pages, extract the information from the pages
sample_post = 'https://www.behance.net/gallery/96824657/A-selection-of-personal-illustrations'
sample_post2 = 'https://www.behance.net/gallery/81095977/Hilton-House-Brand-Identity'
ua = UserAgent()
post_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "Cookie": "gk_suid=26565821; gki=%7B%22db_semaphore%22%3Afalse%2C%22image_search_dark%22%3Afalse%7D; AMCVS_9E1005A551ED61CA0A490D45%40AdobeOrg=1; sign_up_prompt=true; bcp=ae72d5d7-5270-4fee-af49-d3281fb83776; bcp_generated=1589167093205; saw_community_support_message=true; s_sess=%20s_cpc%3D1%3B%20s_dmdbase_custom%3D1%3B%20s_dmdbase%3D1%3B%20s_cc%3Dtrue%3B%20s_sq%3Dadbadobenonacdcprod%25252Cadbadobeprototype%253D%252526c.%252526a.%252526activitymap.%252526page%25253Dbehance.net%2525253Aprofile%2525253Adefault%252526link%25253Dn1U1l1a1-Discover%252526region%25253Dother%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%3B%20s_ppv%3D%255B%2522www.behance.net%252Fdiscover%2522%252C93%252C0%252C971%252C1680%252C971%252C1680%252C1050%252C2%252C%2522P%2522%255D%3B; ilo0=true; AMCV_9E1005A551ED61CA0A490D45%40AdobeOrg=-227196251%7CMCMID%7C75609912311775381102274340397923266319%7CMCAAMLH-1589418756%7C11%7CMCAAMB-1589787500%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589189900s%7CNONE%7CMCAID%7CNONE; s_pers=%20cpn%3Dbehance.net%253Agalleries%7C1746937021039%3B%20ppn%3Dbehance.net%253Agallery%7C1746937021041%3B%20s_nr%3D1589182699715-Repeat%7C1620718699715%3B%20s_vs%3D1%7C1589184500246%3B; s_sess=%20s_cpc%3D1%3B%20s_dmdbase_custom%3D1%3B%20s_dmdbase%3D1%3B%20s_sq%3Dadbadobenonacdcprod%25252Cadbadobeprototype%253D%252526c.%252526a.%252526activitymap.%252526page%25253Dbehance.net%2525253Aprofile%2525253Adefault%252526link%25253Dn1U1l1a1-Discover%252526region%25253Dother%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%3B%20s_ppv%3D%255B%2522www.behance.net%252Fdiscover%2522%252C93%252C0%252C971%252C1680%252C971%252C1680%252C1050%252C2%252C%2522P%2522%255D%3B%20s_cc%3Dtrue%3B",
    "user-agent": ua.random
}


def parse_post(url, headers):
    '''
    List of things to grab:
    - url: str
    - images/media paths: list
    - title: str
    - author: list
    - description: str
    - comments: list
    - likes: int
    - views: int
    - creative fields: list
    - tag: list
    - published date: str
    '''
    res = requests.get(url, headers=headers)
    #source = clean_html(res.content.decode(res.encoding))
    source = res.content
    print(source)


parse_post(sample_post, post_headers)

# comment_headers = {
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "accept-encoding": "gzip, deflate, br",
#     "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
#     "user-agent": ua.random,
#     "x-csrf-token": "LVT78lsj/YV8NDO4UJ2dibwBAM/2b9H3MjAWgz+TxskcmM7EHj0ms7jrcW6fl6gQpeg386UqdstI9p4h8BZOcw==",
#     "x-requested-with": 'XMLHttpRequest'
# }

# res = requests.get(sample_post, headers=headers)
# source = clean_html(res.content.decode(res.encoding))


# def parse_post(url):
#     res = requests.get(url, headers=headers)
#     #source = clean_html(res.content.decode(res.encoding))
#     source = res.content
#     tree = etree.HTML(source)
#     data = {}
#     # image link
#     data['url'] = url
#     # image/video link
#     media_path = "//div[@class='media-content']//img | //div[@class='media-content']//video"
#     # get from meta
#     # media_path = "//meta"
#     media_nodes = tree.xpath(media_path)
#     try:
#         print(media_nodes[0].attrib['data-src'])
#         data['media file'] = media_nodes[0].attrib['data-src']
#     except:
#         print("Media file not found")

#     # short description
#     desc_path = "//div[@class='shot-desc']//p//text()"
#     desc_nodes = tree.xpath(desc_path)
#     short_description = ""
#     for d in desc_nodes:
#         short_description += d
#         # if d.text:
#         #     short_description += d.text
#     print(short_description)
#     data['short description'] = short_description

#     # comment section
#     # comments url: https://dribbble.com/shots/11290639-Still-life/comments
#     comment_url = url + '/comments'
#     comment_res = requests.get(comment_url, headers=comment_headers)
#     comment_tree = etree.HTML(comment_res.content)
#     comments_path = "//div[@class='comment-body']/p/text()"
#     comment_nodes = comment_tree.xpath(comments_path)
#     comments = []
#     for comment in comment_nodes:
#         if comment.strip():
#             comments.append(comment)
#     print(",".join(comments))
#     data['comments'] = comments

#     # tags
#     tag_path = "//div[@class='screenshot-stats']/div[@class='shot-tags']/ol/li//text()"
#     tag_nodes = tree.xpath(tag_path)
#     tags = []
#     for tag in tag_nodes:
#         if tag.strip():
#             tags.append(tag)
#     print(",".join(tags))
#     data['tags'] = tags

#     # color palette
#     palette_path = "//div[@class='screenshot-stats']/div[@class='shot-colors']/ul/li[@class='color']/a/text()"
#     palette_nodes = tree.xpath(palette_path)
#     color_palettes = []
#     for color in palette_nodes:
#         if color.strip():
#             color_palettes.append(color)
#     print(",".join(color_palettes))
#     data['color palette'] = color_palettes

#     # likes
#     likes_path = "//div[@class='screenshot-stats']/div[@class='shot-likes']/a/text()"
#     likes_node = tree.xpath(likes_path)[0]
#     # convert string to integer
#     try:
#         print(int(likes_node.split()[0]))
#         data['number of likes'] = int(likes_node.split()[0])
#     except:
#         data['number of likes'] = 0

#     # number of saves
#     saves_path = "//div[@class='screenshot-stats']/div[@class='shot-saves']/a/text()"
#     saves_node = tree.xpath(saves_path)[0]
#     try:
#         print(int(saves_node.split()[0]))
#         data['number of saves'] = int(saves_node.split()[0])
#     except:
#         data['number of saves'] = 0

#     # date
#     date_path = "//div[@class='screenshot-stats']/div[@class='shot-date']/text()"
#     date_node = tree.xpath(date_path)
#     date = ""
#     for d in date_node:
#         if d.strip():
#             date += d.strip()
#     print(date)
#     data['date'] = date

#     return data
