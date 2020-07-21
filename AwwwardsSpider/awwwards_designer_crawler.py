import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from fake_useragent import UserAgent
from lxml import etree
from lxml.html.clean import clean_html
import json
import pandas as pd


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

        # data columns
        self.designers = []
        self.designers_url = []
        self.designers_twitter = []
        self.designers_instagram = []
        self.designers_linkedin = []
        self.designers_facebook = []

    def retrieve_urls(self, url):
        res = requests.get(url, headers=self.headers)
        source = res.content
        tree = etree.HTML(source)
        designer_path = "//ul[contains(@class, 'list-items')]/li//a[@class='profile-link']"
        designer_nodes = tree.xpath(designer_path)
        for node in designer_nodes:
            try: 
                self.designers.append(node.text)
                self.designers_url.append("https://www.awwwards.com" + node.attrib['href'])
            except:
                self.designers.append(None)
                self.designers_url.append(None)
        return True 

    def crawl_designer(self, url):
        '''
        Get the designers social media contacts:
        - Facebook
        - Instagram
        - LinkedIn
        - Twitter
        '''
        res = requests.get(url, headers=self.headers)
        source = res.content
        tree = etree.HTML(source)
        link_path = "//ul[contains(@class, 'list-bts')]/li/a"
        link_nodes = tree.xpath(link_path)
        self.designers_facebook.append(None)
        self.designers_instagram.append(None)
        self.designers_linkedin.append(None)
        self.designers_twitter.append(None)
        for link in link_nodes:
            if 'bt-facebook' in link.attrib['class']:
                self.designers_facebook[-1] = link.attrib['href']
            if 'bt-twitter' in link.attrib['class']:
                self.designers_twitter[-1] = link.attrib['href']
            if 'bt-linkedin' in link.attrib['class']:
                self.designers_linkedin[-1] = link.attrib['href']
            if 'bt-instagram' in link.attrib['class']:
                self.designers_instagram[-1] = link.attrib['href']
        return True

    def run(self):
        # crawl user names and their profiles
        for page in range(self.start, self.end+1):
            target = self.url + str(page)
            self.retrieve_urls(target)
        # base on the profiles, crawl their respective contact links
        for profiles in self.designers_url:
            print(f"Crawling {profiles} ...")
            self.crawl_designer(profiles)
        

    def output_csv(self):
        # set up dataframe
        contact_list = pd.DataFrame(
            {
                "designers": self.designers, 
                "profiles": self.designers_url,
                "facebook": self.designers_facebook,
                "twitter": self.designers_twitter,
                "linkedin": self.designers_linkedin,
                "instagram": self.designers_instagram
                }
            )
        # deal with duplicate designers
        contact_list = contact_list.drop_duplicates(subset ="profiles", 
                     keep ="first") 
        contact_list.to_csv('../../awwwards_contact_list.csv')

if __name__ == "__main__":
    crawler = Awwwards_Designer_Crawler(1, 1)
    crawler.run()
    # make csv
    crawler.output_csv()

