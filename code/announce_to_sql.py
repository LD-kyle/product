import os
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import time
import re
logfilepath = 'logs'

user_SQL = 'likai'
pass_SQL = '2017422100'
host = 'rm-2ze86u1j19c151g4dmo.mysql.rds.aliyuncs.com:3306/'
database = 'lk_test'
tablename = 'key_test'       # 公告
SQLengine = 'mysql+pymysql://' + user_SQL + ':' + pass_SQL + '@'+ host + database + '?charset=utf8'
engine = create_engine(SQLengine,echo=True)