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

from _dber.pg_orm import Design
from _dber.config import session

import os
import sys

sys.path.insert(0, os.path.abspath(os.getcwd()+'../'))
sys.path.insert(1, os.path.abspath(os.getcwd()+'../../'))
sys.path.insert(2, os.path.abspath(os.getcwd()+'../../../'))
sys.path.insert(3, os.path.abspath(os.getcwd()+'../../../../'))


class DribbbleParser(Task):  # make sure you give it a name :) 記得給parser一個名字呦
    def run(self, params):
        '''
        Run parser
        parser任務主要是負責解析spider爬下來的源碼，並將其存入數據庫
        '''
        url = params['design_url']
        # retrieve info
        dsgn = self.retrieve_info(url)

        inserted = self.insertData(dsgn)

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
            data['media file'] = media_nodes[0].attrib['data-src']
        except:
            data['media file'] = None

        # short description
        desc_path = "//div[@class='shot-desc']//p//text()"
        desc_nodes = tree.xpath(desc_path)
        short_description = ""
        for d in desc_nodes:
            short_description += d
            # if d.text:
            #     short_description += d.text
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
        data['comments'] = comments

        # tags
        tag_path = "//div[@class='screenshot-stats']/div[@class='shot-tags']/ol/li//text()"
        tag_nodes = tree.xpath(tag_path)
        tags = []
        for tag in tag_nodes:
            if tag.strip():
                tags.append(tag)
        data['tags'] = tags

        # color palette
        palette_path = "//div[@class='screenshot-stats']/div[@class='shot-colors']/ul/li[@class='color']/a/text()"
        palette_nodes = tree.xpath(palette_path)
        color_palettes = []
        for color in palette_nodes:
            if color.strip():
                color_palettes.append(color)
        data['color palette'] = color_palettes

        # likes
        likes_path = "//div[@class='screenshot-stats']/div[@class='shot-likes']/a/text()"
        likes_node = tree.xpath(likes_path)
        # convert string to integer
        try:
            data['number of likes'] = int(likes_node[0].split()[0])
        except:
            data['number of likes'] = 0

        # number of saves
        saves_path = "//div[@class='screenshot-stats']/div[@class='shot-saves']/a/text()"
        saves_node = tree.xpath(saves_path)
        try:
            data['number of saves'] = int(saves_node[0].split()[0])
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
        dsgn = Design(
            url=data['url'],
            media_path=data['media file'],
            description=data['short description'],
            comments=data['comments'],
            tags=data['tags'],
            color_palette=data['color palette'],
            likes=data['number of likes'],
            saves=data['number of saves'],
            date=data['date'],
            write_date=str(datetime.now())
        )
        return dsgn

    def insertData(self, cnt):
        '''
        Store result to database
        將解析好的內容存入數據庫
        '''
        try:
            sess = session()
            sess.add(cnt)
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
