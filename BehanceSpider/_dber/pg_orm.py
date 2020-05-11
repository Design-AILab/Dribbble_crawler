# table models
# reference samePost.py
from sqlalchemy import Column, Integer, String, Table, Text, Date, Boolean, Time, TIMESTAMP, VARCHAR, func, ARRAY
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
metadata = Base.metadata
'''
two base tables:
PageSource -- store results from spider
Content -- store results from parser
本程式用的表將於此處定義
Base class中每一行是一個Column
根據需求來改變及增加表
'''
# modify tables according to the information needed to be retrieved

'''
class PageSource(Base):
    __tablename__ = "uspto_pagesource"  
    uid = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    collection_time = Column(TIMESTAMP, nullable=True,
                             server_default=func.now())
    page_source = Column(VARCHAR)
    write_date = Column(Date)

    def __repr__(self):
        return f"USPTO Source(Url: '{self.url}', Write Date: '{self.write_date})'"
'''


class Design(Base):
    __tablename__ = "behance_designs"
    __table_args__ = {"useexisting": False}
    uid = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=True)
    media_path = Column(ARRAY(String))
    title = Column(String)
    author = Column(ARRAY(String))
    author_profiles = Column(ARRAY(String))
    description = Column(String)
    tags = Column(ARRAY(String))
    creative_fields = Column(ARRAY(String))
    likes = Column(Integer)
    comments = Column(Integer)
    date = Column(String)
    collection_time = Column(TIMESTAMP, nullable=True,
                             server_default=func.now())
    write_date = Column(String)

    def __repr__(self):
        return f"Behance Posts(Title: '{self.title}', Write Date: '{self.write_date}')"
