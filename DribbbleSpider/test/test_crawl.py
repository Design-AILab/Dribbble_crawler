import requests
from fake_useragent import UserAgent
from lxml import etree
from lxml.html.clean import clean_html

ua = UserAgent()
headers = {
    "user-agent": ua.random
}
page = 1
target_url = f"https://dribbble.com/?page={page}"

# xpath: //*[@class="group shot-thumbnail shot-thumbnail-with-hover-overlay"]/div/a


def grab_design_links(url, headers):
    res = requests.get(target_url, headers=headers)
    source = clean_html(res.content.decode(res.encoding))
    tree = etree.HTML(source)
    link_path = "//div[@id = 'main']//li[contains(@class, 'shot-thumbnail-with-hover-overlay')]/div//a[contains(@class,'dribbble-link')]"
    link_nodes = tree.xpath(link_path)
    url = []
    for a in link_nodes:
        a_url = a.attrib['href']
        if a_url not in url:
            url.append("https://dribbble.com"+a_url)
    return url


links = grab_design_links(target_url, headers)
print(len(links))
print(links)
