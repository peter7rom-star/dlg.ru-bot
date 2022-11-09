from dataclasses import dataclass
import re

import requests

from rss_parser import Parser
import lxml
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


@dataclass
class ArticleFeed:
    publish_date: str
    title: str
    content_image: str
    description: str
    link: str

class RSSParser:
    def __init__(self, url):
        self.url = url
        user_agent = generate_user_agent()
        headers = {'User-Agent': user_agent}
        self.xml = requests.get(self.url, headers=headers, cert=("cert/certificate.crt", "cert/my_tg_bot_key.key"))
        self.limit = 10
        self.parser = Parser(self.xml.text, limit=30)

    def parse(self):
        feed = self.parser.parse()
        return self.parse_content_images(feed)

    def parse_content_images(self, feed):
        self.raw_data: dict = feed.dict()
        soup = BeautifulSoup(self.xml.text, 'xml')
        nodes = soup.findAll('item')
        article_feeds = list()
        self.data = dict()
        if self.limit is not None:
            nodes = nodes[: self.limit]
            for index, item in enumerate(nodes):
                self.data['publish_date'] = self.raw_data['feed'][index]['publish_date']
                self.data['title'] = self.raw_data['feed'][index]['title']
                self.data['description'] = self.raw_data['feed'][index]['description'].split('\n')[0]
                self.data['content_image'] = ''
                self.data['link'] = self.raw_data['feed'][index]['link']
                c = item.find('content:encoded')
                soup_2 = BeautifulSoup(c.text, 'html.parser')
                img = soup_2.select_one('img')
                text = str(img)
                node = text.split('/>')[0]
                match = re.search(r'((\bhttps?:\/\/[\w\.\-\/]*\.(jpe?g|png))\b) (1\d+|2\d+|3\d+)w', node)
                if match:
                    image = match[1]
                    self.data['content_image'] = image
                article_feed = ArticleFeed(**self.data)
                article_feeds.append(article_feed)
        return article_feeds

class ArticleParser:
    def __init__(self, url):
        self.url = url
        self.html = requests.get(url)

    def parse_url(self):
        text = str()
        soup = BeautifulSoup(self.html.content, 'lxml')
        text += str(soup.h1)
        text += str(soup.select_one("img[src^=entry-thumb]"))
        for i in soup.select("div[class^=td-post-content] > *:not(script, div)"):
            text += str(i)
        print(text)
