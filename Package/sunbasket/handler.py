# -*- coding: utf-8 -*-
# author:shihua
# designer:shihua
# coder:shihua
# 这是一个日志处理器类，包括各种转发后端的处理器
"""
模块介绍
-------

这是一个日志处理器类，包括各种转发后端的处理器

设计模式：

    （1）  无 

关键点：    

    （1）日志转发处理

主要功能：            

    （1）提供各种转发后端的处理器                                

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



import logging
import datetime
import json
from sunbasket import SQLiteManager
from sqlalchemy import Column, String, create_engine, Integer, DateTime,Text,LargeBinary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pickle
import yaml
import sunbasket



####### 日志处理器类 ########################################################
### 设计模式：                                                           ###
### （1）无                                                              ###
### 关键点：                                                             ###
### （1）日志转发处理                                                     ###
### 主要功能：                                                           ###
### （1）提供各种转发后端的处理器                                          ###
############################################################################


####### 日志处理器类 ####################################################################################
########################################################################################################



### SQLite日志转发处理器
class SQLiteHandler(logging.Handler):
    '''
    类介绍：

        这是一个SQLite日志转发处理器类，主要功能提供SQLite日志转发功能，主要技术SQLite和方法重写。
    '''


    def __init__(self,log_database=None,log_table=None,remark = 'no remark'):
        '''
        属性功能：

            定义一个初始化SQLite转发处理器的方法

        参数：
            remark (str): 备注
            filter (object): 这是一个日志过滤器实例属性
            json_format (object): 这是一个json格式化实例属性
            log_database (str): 日志数据库
            log_table (str): 日志表，一般不使用
        '''
        
        super(SQLiteHandler,self).__init__()
        self.log_database = log_database
        self.log_table = log_table
        self.remark = remark
        ### 实例化自定义的日志过滤器并加入到处理器中
        filter = sunbasket.SQLiteLogFilter()
        self.addFilter(filter)
        ### 实例化自定义的日志格式化对象
        json_format = sunbasket.JsonFormatter()
        self.setFormatter(json_format)
        

    def emit(self,record):
        '''
        方法功能：

            重写一个处理日志的方法

        参数：
            record (object): logging的日志记录对象

        返回：
            无
        '''
        
        ### 配置SQLite日志记录table
        if self.log_database == None:
            SQLitelog_dict = sunbasket.SQLITE_CONFIG
            connect_info = SQLitelog_dict['connect']
        else:
            connect_info = self.log_database
        print(connect_info)
        ### 加载SQLite连接器
        tmp_SQLiteManager = sunbasket.SQLiteManager(connect_info)
        ### 声明数据基类
        Base= declarative_base(tmp_SQLiteManager.engine)
        ### 具体数据ORM对象类
        class ManualLog(Base):
            '''
            类介绍：

                这是一个手动日志数据ORM对象类
            '''
            __tablename__ = 'ManualLog'
            index = Column(Integer, autoincrement=True, primary_key=True)
            msg = Column(Text)
            levelname = Column(Text)
            filename = Column(Text)
            module = Column(Text)
            lineno = Column(Integer)
            time = Column(Text)
        ### 数据表预处理
        del_list = [ManualLog.__table__,]
        # Base.metadata.drop_all(tables=del_list)
        Base.metadata.create_all(tables=del_list)
        ### 开始处理日志记录，转为python的字典格式
        value = self.format(record)
        print(value)
        ### 创建具体数据表
        item = ManualLog(**value)
        ### SQLite数据增加操作
        tmp_SQLiteManager.insert_data(item)
        print('====================>>>>>> Log to SQLite well done!')



#############################################################################################################
#############################################################################################################


