import logging
from sunbasket.handler import SQLiteHandler



### 创建日志操作对象
logger = logging.getLogger()
### 设置日志操作对象的日志等级
logger.setLevel(logging.INFO)
### 创建一个SQLite处理器
# SQLiteHandler = SQLiteHandler(log_database='sqlite:///E:\\workspace\\SunBasket\\Demo\\test.db')
SQLiteHandler = SQLiteHandler()
### 设置SQLite处理器的日志等级
SQLiteHandler.setLevel(logging.INFO)
### 向日志操作对象添加SQLite处理器
logger.addHandler(SQLiteHandler)
logger.info('start test log handler')
logger.warning('this is a warning log')


