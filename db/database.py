from certifi import where
from bot import logger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, select, update
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()


class Message(Base):
    __tablename__ = 'my_messages'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    message_title = Column(String)
    publish_date = Column(String)

    def __init__(self, chat_id, message_title, pub_date):
        self.chat_id = chat_id
        self.message_title = message_title
        self.publish_date = pub_date

    def __repr__(self):
        return "<Message %s, %s" % (self.message_title, self.publish_date)

class Database(object):
    db = "db/messages.db"
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{self.db}')
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        self.session = Session(self.engine)
        logger.info("database initialized")

    def init_table(self):
        if Message.metadata.tables[Message.__tablename__].exists(self.engine):
            Message.__table__.drop(self.engine)
        Message.__table__.create(bind=self.engine)
        # logger.info('Table %s created' % self.engine.Result.all())

    def add_data(self, chat_id, message_title, pub_date):
        data = Message(chat_id, message_title, pub_date)
        self.session.add(data)

    def update_messages(self, chat_id, message_title, pub_date):
        self.session.query(Message).filter(Message.chat_id == chat_id).update({
            Message.message_title: message_title, Message.publish_date: pub_date})

    def select_data(self):
        result = self.session.execute(select(Message.message_title, Message.publish_date)).fetchone()
        return result