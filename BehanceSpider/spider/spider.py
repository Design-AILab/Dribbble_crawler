'''
Task 1: Conduct crawling
這是程式中爬蟲的部分 (與網頁連結的部分)
'''
from _dber.config import session
from _dber.pg_orm import Design
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

import traceback
from mrq.context import connections, log
from mrq.job import queue_job
from mrq.task import Task
from lxml import etree
import time

from fake_useragent import UserAgent
import json
from lxml.html.clean import clean_html
import sys
import os
sys.path.insert(0, os.path.abspath(os.getcwd()+'../../../'))
sys.path.insert(1, os.path.abspath(os.getcwd()+'../../../../'))


class BehanceSpider(Task):  # give ur spider a cute name ;) 給spider一個好聽的名字吧
    def run(self, params):
        '''
        Conduct Crawling and proceed to the next task
        When complete, make sure to send the job to parser!
        在此函數中執行爬蟲工作
        這個工作結束後要用 parser_job 分發新的解析任務
        在這個階段以獲取網頁源碼為主
        '''
        url = params['url']  # link to the search result page
        links = self.retrieve_urls(url)  # all links
        for link in links:
            # check if the patent already exist in our database
            sess = session()
            added = sess.query(Design).filter_by(url=link).first()
            sess.commit()
            sess.close()
            if added:
                continue
            else:
                # pass it to the parser
                params['design_url'] = link
                self.parser_job(params,
                                fpath=params['parseTask'],
                                nqueue=params['parsequeue'])

            # to update existing entries
            # params['design_url'] = link
            # self.parser_job(params,
            #                 fpath=params['parseTask'],
            #                 nqueue=params['parsequeue'])
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
                params, fpath=params['spiderTask'], nqueue=params['spiderqueue'])
            print(e)

    def retrieve_urls(self, url):
        ua = UserAgent()
        behance_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
            "Connection": "keep-alive",
            "Cookie": "gk_suid=26565821; gki=%7B%22db_semaphore%22%3Afalse%2C%22image_search_dark%22%3Afalse%7D; AMCVS_9E1005A551ED61CA0A490D45%40AdobeOrg=1; sign_up_prompt=true; bcp=ae72d5d7-5270-4fee-af49-d3281fb83776; bcp_generated=1589167093205; saw_community_support_message=true; ilo0=true; AMCV_9E1005A551ED61CA0A490D45%40AdobeOrg=-227196251%7CMCMID%7C75609912311775381102274340397923266319%7CMCAAMLH-1589418756%7C11%7CMCAAMB-1589851403%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589253803s%7CNONE%7CMCAID%7CNONE; s_sess=%20s_cpc%3D1%3B%20s_dmdbase_custom%3D1%3B%20s_dmdbase%3D1%3B%20s_sq%3Dadbadobenonacdcprod%25252Cadbadobeprototype%253D%252526c.%252526a.%252526activitymap.%252526page%25253Dbehance.net%2525253Aprofile%2525253Adefault%252526link%25253Dn1U1l1a1-Discover%252526region%25253Dother%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%3B%20s_cc%3Dtrue%3B%20s_ppv%3D%255B%2522www.behance.net%252Fgallery%252F94529637%252FLakanna%2522%252C7%252C0%252C971%252C941%252C971%252C1680%252C1050%252C2%252C%2522L%2522%255D%3B; s_pers=%20s_nr%3D1589246619721-Repeat%7C1620782619721%3B%20cpn%3Dbehance.net%253Agallery%7C1747013019900%3B%20ppn%3Dbehance.net%253Agalleries%7C1747013019905%3B%20s_vs%3D1%7C1589248419963%3B; s_sess=%20s_cpc%3D1%3B%20s_dmdbase_custom%3D1%3B%20s_dmdbase%3D1%3B%20s_sq%3Dadbadobenonacdcprod%25252Cadbadobeprototype%253D%252526c.%252526a.%252526activitymap.%252526page%25253Dbehance.net%2525253Aprofile%2525253Adefault%252526link%25253Dn1U1l1a1-Discover%252526region%25253Dother%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%3B%20s_ppv%3D%255B%2522www.behance.net%252Fgallery%252F94529637%252FLakanna%2522%252C7%252C0%252C971%252C941%252C971%252C1680%252C1050%252C2%252C%2522L%2522%255D%3B%20s_cc%3Dtrue%3B",
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
        res = requests.get(url, headers=behance_headers,
                           auth=HTTPDigestAuth('user', 'pass'))
        projects = json.loads(res.content)['category_projects']
        urls = []
        for p in projects:
            urls.append(p['url'])
        return urls

    def parser_job(self, params, fpath=None, nqueue=None):
        '''
        Add to the queue of the Parser task
        '''
        queue_job(fpath, params, queue=nqueue)

    def requeue_job(self, params, fpath=None, nqueue=None):
        '''
        Requeue a failed job
        '''
        log.warning('Job Failed, re-queue...%s' % params['url'])
        queue_job(fpath, params, queue=nqueue)
