'''
Task 2: Parsing
'''
from mrq.task import Task
from mrq.job import queue_job
from mrq.context import connections, log

import requests
from lxml import etree
from lxml.html.clean import clean_html
from fake_useragent import UserAgent
import traceback
from datetime import datetime
import json


from _dber.pg_orm import Design
from _dber.config import session

import os
import sys

sys.path.insert(0, os.path.abspath(os.getcwd()+'../'))
sys.path.insert(1, os.path.abspath(os.getcwd()+'../../'))
sys.path.insert(2, os.path.abspath(os.getcwd()+'../../../'))
sys.path.insert(3, os.path.abspath(os.getcwd()+'../../../../'))


class BehanceParser(Task):  # make sure you give it a name :) 記得給parser一個名字呦
    def run(self, params):
        '''
        Run parser
        parser任務主要是負責解析spider爬下來的源碼，並將其存入數據庫
        '''
        url = params['design_url']
        # retrieve info
        data = self.retrieve_info(url)

        sess = session()
        added = sess.query(Design).filter_by(url=url).first()
        sess.commit()
        sess.close()
        if added:
            # update
            inserted = self.updateData(data)
        else:
            inserted = self.insertData(data)

        if not inserted:
            queue_job(params['parseTask'],
                      params,
                      queue=params['parsequeue'])
        return True

    def run_wrapped(self, params):
        """ 
        Wrap all calls to tasks in init & safety code. 
        """
        try:
            return self.run(params)
        except Exception as e:
            traceback.print_exc()
            self.requeue_job(
                params, fpath=params['parseTask'], nqueue=params['parsequeue'])
            print(e)

    def retrieve_info(self, url):
        '''
        Parser job based on the source
        Output should be a database object
        在這裡，為了以防再次訪問網站，我們已在spider階段將源碼存入數據庫的pagesource表
        現在，我們只需要將源碼從數據庫中拿出來進行解析就好
        這個函數是parser 的核心，進行主要的解析工作
        '''
        ua = UserAgent()
        post_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
            "Cookie": "gk_suid=26565821; gki=%7B%22db_semaphore%22%3Afalse%2C%22image_search_dark%22%3Afalse%7D; AMCVS_9E1005A551ED61CA0A490D45%40AdobeOrg=1; sign_up_prompt=true; bcp=ae72d5d7-5270-4fee-af49-d3281fb83776; bcp_generated=1589167093205; saw_community_support_message=true; s_sess=%20s_cpc%3D1%3B%20s_dmdbase_custom%3D1%3B%20s_dmdbase%3D1%3B%20s_cc%3Dtrue%3B%20s_sq%3Dadbadobenonacdcprod%25252Cadbadobeprototype%253D%252526c.%252526a.%252526activitymap.%252526page%25253Dbehance.net%2525253Aprofile%2525253Adefault%252526link%25253Dn1U1l1a1-Discover%252526region%25253Dother%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%3B%20s_ppv%3D%255B%2522www.behance.net%252Fdiscover%2522%252C93%252C0%252C971%252C1680%252C971%252C1680%252C1050%252C2%252C%2522P%2522%255D%3B; ilo0=true; AMCV_9E1005A551ED61CA0A490D45%40AdobeOrg=-227196251%7CMCMID%7C75609912311775381102274340397923266319%7CMCAAMLH-1589418756%7C11%7CMCAAMB-1589787500%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589189900s%7CNONE%7CMCAID%7CNONE; s_pers=%20cpn%3Dbehance.net%253Agalleries%7C1746937021039%3B%20ppn%3Dbehance.net%253Agallery%7C1746937021041%3B%20s_nr%3D1589182699715-Repeat%7C1620718699715%3B%20s_vs%3D1%7C1589184500246%3B; s_sess=%20s_cpc%3D1%3B%20s_dmdbase_custom%3D1%3B%20s_dmdbase%3D1%3B%20s_sq%3Dadbadobenonacdcprod%25252Cadbadobeprototype%253D%252526c.%252526a.%252526activitymap.%252526page%25253Dbehance.net%2525253Aprofile%2525253Adefault%252526link%25253Dn1U1l1a1-Discover%252526region%25253Dother%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%3B%20s_ppv%3D%255B%2522www.behance.net%252Fdiscover%2522%252C93%252C0%252C971%252C1680%252C971%252C1680%252C1050%252C2%252C%2522P%2522%255D%3B%20s_cc%3Dtrue%3B",
            "user-agent": ua.random
        }

        res = requests.get(url, headers=post_headers)
        #source = clean_html(res.content.decode(res.encoding))
        source = res.content
        tree = etree.HTML(source)

        data = {}
        data['url'] = url
        # images or media paths
        media_path = "//div[@id='project-modules']//img"
        media_nodes = tree.xpath(media_path)
        media_files = []
        if media_nodes:
            for node in media_nodes:
                media_files.append(node.attrib['src'])
        data['media paths'] = media_files

        # title
        title_path = "//meta[@property='og:title']"
        title_node = tree.xpath(title_path)
        if title_node:
            title = title_node[0].attrib['content']
            data['title'] = title
        else:
            data['title'] = ''
        # author
        authors_path = "//div[@class='ProjectOwnersInfo-individualProfile-19h']//div[contains(@class, 'ProjectOwnersInfo-userInfo-2WK')]/a"
        authors_nodes = tree.xpath(authors_path)
        authors = []
        authors_url = []
        try:
            for node in authors_nodes:
                if node.text and node.text not in authors:
                    authors.append(node.text)
                    authors_url.append(node.attrib['href'])
        except:
            pass
        data['authors'] = authors
        data['authors profile'] = authors_url

        # json
        json_path = "//script[@id='beconfig-store_state']/text()"
        json_node = tree.xpath(json_path)
        json_data = json.loads(json_node[0])
        # for key, value in json_data['project']['project'].items():
        #     print(key)
        # print(json_data['project']['project']['tags'])
        # # for key, value in json_data['project']['project'].items():
        # #     print(key)
        # # print(json_data['project']['commentCount'])
        # description
        data['description'] = json_data['project']['project']['description']
        # number of comments
        data['comment counts'] = json_data['project']['commentCount']
        # number of likes
        data['number of likes'] = json_data['project']['appreciationCount']
        # publish date
        data['date'] = datetime.fromtimestamp(
            json_data['project']['project']['published_on']).strftime('%m/%d/%Y')
        # creative fields
        c_fields = []
        for field in json_data['project']['project']['fields']:
            c_fields.append(field['name'])
        data['creative fields'] = c_fields
        # tags
        tags = []
        for tag in json_data['project']['project']['tags']:
            tags.append(tag['title'])
        data['tags'] = tags
        return data

    def insertData(self, data):
        '''
        Store result to database
        將解析好的內容存入數據庫
        '''
        dsgn = Design(
            url=data['url'],
            media_path=data['media paths'],
            title=data['title'],
            author=data['authors'],
            author_profiles=data['authors profile'],
            description=data['description'],
            tags=data['tags'],
            creative_fields=data['creative fields'],
            likes=data['number of likes'],
            comments=data['comment counts'],
            date=data['date'],
            write_date=datetime.now().strftime('%m/%d/%Y')
        )
        try:
            sess = session()
            sess.add(dsgn)
            sess.commit()
            return True
        except Exception as e:
            sess.rollback()
            traceback.print_exc()
            print(e)
            return False
        finally:
            sess.close()

    def updateData(self, info):
        '''
        Update data
        '''
        sess = session()
        try:
            dsgn = sess.query(Design).filter_by(url=info['url']).first()
            dsgn.media_path = info['media paths']
            dsgn.write_date = datetime.now().strftime('%m/%d/%Y')
            dsgn.title = info['title']
            dsgn.author = info['authors']
            dsgn.author_profiles = info['authors profile']
            dsgn.description = info['description']
            dsgn.comments = info['comment counts']
            dsgn.tags = info['tags']
            dsgn.creative_fields = info['creative fields']
            dsgn.likes = info['number of likes']
            dsgn.date = info['date']
            sess.commit()
            return True
        except Exception as e:
            sess.rollback()
            traceback.print_exc()
            print(e)
            return False
        finally:
            sess.close()

    def requeue_job(self, params, fpath=None, nqueue=None):
        '''
        requeue an unfinished job
        '''
        log.warning('Job Failed, re-queue...%s' % params['url'])
        queue_job(fpath, params, queue=nqueue)
