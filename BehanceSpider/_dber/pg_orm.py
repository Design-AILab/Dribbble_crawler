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

'''
Tables:
All: dribbble_designs
animation: dribbble_designs_animation
branding: dribbble_designs_branding
illustration: dribbble_designs_illustration
mobile: dribbble_designs_mobile
print: dribbble_designs_print
product design: dribbble_designs_product_design
typography: dribbble_designs_typography
web design: dribbble_designs_web_designs
'''


class Design(Base):
    __tablename__ = "dribbble_designs_animation"
    __table_args__ = {"useexisting": False}
    uid = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=True)
    media_path = Column(String)
    description = Column(String)
    comments = Column(ARRAY(String))
    tags = Column(ARRAY(String))
    color_palette = Column(ARRAY(String))
    likes = Column(Integer)
    saves = Column(Integer)
    date = Column(String)
    collection_time = Column(TIMESTAMP, nullable=True,
                             server_default=func.now())
    write_date = Column(String)

    def __repr__(self):
        return f"Dribbble Content(Title: '{self.title}', Write Date: '{self.write_date}')"
