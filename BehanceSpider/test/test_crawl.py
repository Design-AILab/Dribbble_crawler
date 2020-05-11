import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from fake_useragent import UserAgent
from lxml import etree
from lxml.html.clean import clean_html
import json


ua = UserAgent()
behance_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
    "Connection": "keep-alive",
    "Cookie": "gk_suid=26565821; gki=%7B%22db_semaphore%22%3Afalse%2C%22image_search_dark%22%3Afalse%7D; AMCVS_9E1005A551ED61CA0A490D45%40AdobeOrg=1; sign_up_prompt=true; s_sess=%20s_cpc%3D1%3B%20s_dmdbase_custom%3D1%3B%20s_dmdbase%3D1%3B%20s_sq%3Dadbadobenonacdcprod%25252Cadbadobeprototype%253D%252526c.%252526a.%252526activitymap.%252526page%25253Dbehance.net%2525253Agalleries%252526link%25253Dd2d1d1d1d1d1d2d1d1d1d1d1d1d2a1-%252526region%25253Dother%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%3B%20s_cc%3Dtrue%3B%20s_ppv%3D%255B%2522www.behance.net%252Fgallery%252F88426043%252Flogo-collection%2522%252C100%252C0%252C13484%252C1680%252C971%252C1680%252C1050%252C2%252C%2522P%2522%255D%3B; bcp=ae72d5d7-5270-4fee-af49-d3281fb83776; bcp_generated=1589167093205; AMCV_9E1005A551ED61CA0A490D45%40AdobeOrg=-227196251%7CMCMID%7C75609912311775381102274340397923266319%7CMCAAMLH-1589418756%7C11%7CMCAAMB-1589771905%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589174305s%7CNONE%7CMCAID%7CNONE; s_sess=%20s_cpc%3D1%3B%20s_dmdbase_custom%3D1%3B%20s_dmdbase%3D1%3B%20s_sq%3Dadbadobenonacdcprod%25252Cadbadobeprototype%253D%252526c.%252526a.%252526activitymap.%252526page%25253Dbehance.net%2525253Agalleries%252526link%25253Dd2d1d1d1d1d1d2d1d1d1d1d1d1d2a1-%252526region%25253Dother%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%3B%20s_ppv%3D%255B%2522www.behance.net%252Fgallery%252F88426043%252Flogo-collection%2522%252C100%252C0%252C13484%252C1680%252C971%252C1680%252C1050%252C2%252C%2522P%2522%255D%3B%20s_cc%3Dtrue%3B; s_pers=%20s_nr%3D1589167104655-Repeat%7C1620703104655%3B%20cpn%3Dbehance.net%253Agallery%7C1746933504841%3B%20ppn%3Dbehance.net%253Agalleries%7C1746933504844%3B%20s_vs%3D1%7C1589168908554%3B; saw_community_support_message=true",
    "Host": "www.behance.net",
    "Referer": "https://www.behance.net/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    "X-BCP": "ae72d5d7-5270-4fee-af49-d3281fb83776",
    "X-NewRelic-ID": "VgUFVldbGwACXFJSBAUF",
    "X-Requested-With": "XMLHttpRequest",

}
page = 1  # 48 posts at a time
target_url = f"https://www.behance.net/v2/discover/?ordinal={page}"


def retrieve_urls(url, headers):
    res = requests.get(target_url, headers=headers,
                       auth=HTTPDigestAuth('user', 'pass'))
    projects = json.loads(res.content)['category_projects']
    urls = []
    for p in projects:
        urls.append(p['url'])
    return urls


posts = retrieve_urls(target_url, behance_headers)
print(posts)
