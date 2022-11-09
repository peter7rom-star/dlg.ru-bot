import asyncio
import re
from datetime import datetime, timedelta, timezone

from bot import bot, logger
from db.database import Database
from parser import RSSParser

CHAT_ID = 909040171
db = Database()
count_sent_messages = 0


class Article:
    def __init__(self):
        parser = RSSParser('https://www.dgl.ru/feed')
        self.feed = parser.parse()
        self.sended_msg = None

    @property
    def article_text(self):
        self.article_title = self.feed[0].title
        self._article_text = self.feed[0].description + '\n' + self.feed[0].link
        return (self.article_title, self._article_text)

    def is_now_published(self):
        data = db.select_data()
        pub_date = self.feed[0].publish_date
        message_title = self.article_text[0]
        match = re.search(r'\d+ \w+ \d+ \d+:\d+:\d+', pub_date)
        s1 = match.group(0)
        format = "%d %b %Y %H:%M:%S"
        # tm = datetime.strptime(s1, format)
        # td = timedelta(days=tm.day, hours=tm.hour, minutes=tm.minute, seconds=tm.second)
        current_time = datetime.now(tz=timezone.utc)
        s2 = current_time.strftime(format)
        # td_2 = timedelta(days=current_time.day, hours=current_time.hour, 
        #                  minutes=current_time.minute, seconds=current_time.second)
        regexp = re.compile(r'(\d+\:35)')
        # res_td = td_2 - td
        if count_sent_messages == 0 and data is None:
            update_messages(chat_id=CHAT_ID, message_title=message_title, pub_date=pub_date)
        if regexp.search(s1) or not regexp.search(s2):
            if data is not None: 
                if data[0] != message_title: 
                    return True
                else:
                    return False
            else:
                return False


def update_messages(chat_id, message_title, pub_date):
    if count_sent_messages == 0:
        db.add_data(chat_id, message_title, pub_date)
    else:
        db.update_messages(chat_id, message_title, pub_date)

async def broadcaster():
    global count_sent_messages
    while True:
        article = Article()
        article_feed = article.feed[0]
        pub_date = article_feed.publish_date
        photo = article_feed.content_image
        title = article.article_text[0]
        text = article.article_text[1]
        html = f"<strong>{title}</strong>\n\n{text}"
        if article.is_now_published():
            count_sent_messages += 1
            if photo:
                await bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=html, parse_mode="html")
            else:
                await bot.send_message(chat_id=CHAT_ID, text=html, parse_mode="html", disable_web_page_preview=True)
        update_messages(chat_id=CHAT_ID, message_title=title, pub_date=pub_date)
        await asyncio.sleep(30)

asyncio.run(broadcaster())
