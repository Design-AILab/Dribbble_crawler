'''
Task 1: Conduct crawling
這是程式中爬蟲的部分 (與網頁連結的部分)
'''
from _dber.config import session
from _dber.pg_orm import Design
from datetime import datetime
import requests
import traceback
from mrq.context import connections, log
from mrq.job import queue_job
from mrq.task import Task
from lxml import etree
import time

from fake_useragent import UserAgent
from lxml.html.clean import clean_html
import sys
import os
sys.path.insert(0, os.path.abspath(os.getcwd()+'../../../'))
sys.path.insert(1, os.path.abspath(os.getcwd()+'../../../../'))


class DribbbleSpider(Task):  # give ur spider a cute name ;) 給spider一個好聽的名字吧
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
        headers = {
            "user-agent": ua.random
        }
        res = requests.get(url, headers=headers)
        source = clean_html(res.content.decode(res.encoding))
        tree = etree.HTML(source)
        link_path = "//div[@id = 'main']//a[contains(@class,'dribbble-link')]"
        link_nodes = tree.xpath(link_path)
        url = []
        for a in link_nodes:
            a_url = a.attrib['href']
            if a_url not in url:
                url.append("https://dribbble.com"+a_url)
        return url

    # def insertData(self, ps):
    #     '''
    #     Insert data into PageSource
    #     這個功能是將源碼存入數據庫中
    #     '''
    #     try:
    #         sess = session()
    #         sess.add(ps)
    #         sess.commit()
    #         return True
    #     except Exception as e:
    #         sess.rollback()
    #         traceback.print_exc()
    #         print(e)
    #         return False
    #     finally:
    #         sess.close()

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
