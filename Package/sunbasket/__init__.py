# -*- coding: utf-8 -*-
# author:shihua
# designer:shihua
# coder:shihua
# 这是一个基础工具集合类
"""
模块介绍
-------

这是一个基础工具集合类

设计模式：

    （1）  无 

关键点：    

    （1）基础依赖

主要功能：            

    （1）基础操作工具集合                                

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
from sqlalchemy import Column,String,create_engine,Integer, DateTime,Text,LargeBinary
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pickle
import yaml
import sunbasket as sbk




####### 基础工具集合类 ######################################################
### 设计模式：                                                           ###
### （1）无                                                              ###
### 关键点：                                                             ###
### （1）基础依赖                                                        ###
### 主要功能：                                                           ###
### （1）基础操作工具集合                                                 ###
############################################################################


####### 基础工具集合 ####################################################################################
########################################################################################################



### 暴露指定的公开接口
__all__ = ['SAVE_ATTR','LOGLEVEL_ALLOWED','SQLITE_CONFIG','SQLiteLogFilter','JsonFormatter','SQLiteManager']



### 基础参数配置-使用yaml保存配置
sunbasket_package_path = sbk.__file__.replace('__init__.py','')
# sunbasket_package_path = 'E:\workspace\SunBasket\Demo\sunbasket' ### 打包的时候此处需要更改为上一行的代码
sunbasket_config_file = open('{}\sunbasket_config.yaml'.format(sunbasket_package_path),encoding='UTF-8')
sunbasket_config_yaml = yaml.load(sunbasket_config_file,Loader=yaml.FullLoader)
### 获取输出参数和日志允许等级
SAVE_ATTR = sunbasket_config_yaml['SAVE_ATTR']
LOGLEVEL_ALLOWED = sunbasket_config_yaml['LOGLEVEL_ALLOWED']
SQLITE_CONFIG = sunbasket_config_yaml['SQLITE_CONFIG']



### SQLite日志等级过滤器类
class SQLiteLogFilter(logging.Filter):
    '''
    类介绍：

        这是一个针对SQLite的日志过滤器类，主要功能提供日志过滤功能，主要技术方法重写。
    '''


    def __init__(self,remark='no remark'):
        '''
        属性功能：

            定义一个初始化SQLite日志等级过滤器的初始化方法
        
        参数：
            remark (str): 备注
        '''

        super(SQLiteLogFilter,self).__init__()
        self.remark = remark


    def filter(self,record):
        '''
        方法功能：

            重写一个过滤方法

        参数：
            record (object): logging日志记录对象

        返回：
            bool (bool): 是否过滤判断
        '''

        if record.__dict__['levelname'] in LOGLEVEL_ALLOWED:
            return True
        else:
            return False
        


### JSON格式化类             
class JsonFormatter(logging.Formatter):
    '''
    类介绍：

        这是一个JSON格式化类，主要功能提供json格式化日志功能，主要技术方法重写
    '''


    def format(self,record):
        '''
        方法功能：

            重写一个格式化方法

        参数：
            record (object): logging日志记录对象

        返回：
            msg (dict): 日志字典
        '''

        msg = self.translate(record)
        self.set_format_time(msg)

        return msg


    @staticmethod
    def translate(record):
        '''
        方法功能：

            定义一个转化日志记录为json的静态方法

        参数：
            record (object): logging日志记录对象

        返回：
            json_dict (dict): json日志字典
        '''

        json_dict = {}
        for attr_name in record.__dict__:
            if attr_name in SAVE_ATTR:
                json_dict[attr_name] = record.__dict__[attr_name]

        return json_dict


    @staticmethod
    def set_format_time(msg):
        '''
        方法功能：

            定义一个设置格式化时间的静态方法

        参数：
            msg (dict): json日志字典

        返回：
            无
        '''

        ### 获取当前时间
        nowtime = datetime.datetime.now()
        ### 将时间转为字符串后存入日志信息中
        msg['time'] = nowtime.strftime("%Y-%m-%d %H:%M:%S" + ".%03d" % (nowtime.microsecond / 1000))



### SQLite管理类
class SQLiteManager(object):
    '''
    类介绍：

        这是一个SQLite数据库连接管理类
    '''


    def __init__(self,connect_info):
        '''
        属性功能：

            定义一个汇总数据库基本信息的属性方法

        参数：
            connect_info (str): SQLite连接信息
            engine (object): SQLite数据库引擎
            connector (object): SQLite连接对象，已包含会话对象

        返回：
            无
        '''

        self.connect_info = connect_info
        self.engine = create_engine(self.connect_info)
        self.connector = self.create_connector()


    def create_connector(self):
        '''
        方法功能：

            定义一个创建SQLite数据库连接的方法，已包含会话对象

        参数：
            无

        返回：
            connector (object): SQLite数据库连接对象，已包含会话对象
        '''

        ### 创建数据库引擎并绑定到会话实例上
        engine = create_engine(str(self.connect_info))
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        connector = session

        return connector
    

    def insert_data(self,data_orm_object):
        '''
        方法功能：

            定义一个将数据ORM对象添加到数据库中

        参数：
            data_orm_object (object): 数据ORM对象

        返回：
            无
        '''

        ### 将数据ORM对象添加到数据库中
        self.connector.add(data_orm_object)
        ### 提交数据库操作
        self.connector.commit()
        print("Insert data well done!")


    def query_data(self,data_table,**data_columns):
        '''
        方法功能：

            定义一个从数据库中进行数据查询的方法

        参数：
            data_table (class): 数据表对应的ORM类
            data_columns (dict): 查询条件字典

        返回：
            query_result (object): 查询结果对象
        '''

        ### 使用数据表类在SQLite数据库连接会话中进行查询
        query_result = self.connector.query(data_table).filter_by(**data_columns).first()
        print("Query data well done!")
        
        return query_result


    def update_data(self,data_table,update_data_dict,**data_columns):
        '''
        方法功能：

            定义一个从数据库中进行数据更新的方法

        参数：
            data_table (class): 数据表对应的ORM类
            update_data_dict (dict): 更新数据字典
            data_columns (dict): 查询条件字典

        返回：
            无
        '''

        ### 使用数据表类在SQLite数据库连接会话中进行查询
        query_result = self.connector.query(data_table).filter_by(**data_columns).first()
        ### 使用查询结果对象在SQLite数据库连接会话中进行修改
        ### 此处使用循环zip处理参数收集，使用exec处理语句运行组合问题
        for i,j in zip(update_data_dict.keys(),update_data_dict.values()):
            exec("query_result.{}={}".format(i,j))
        ### 提交数据库操作
        self.connector.commit()
        print("Update data well done!")


    def delete_data(self,data_table,**data_columns):
        '''
        方法功能：

            定义一个从数据库中进行数据删除的方法

        参数：
            data_table (class): 数据表对应的ORM类
            data_columns (dict): 查询条件字典
        '''

        ### 使用数据表类在SQLite数据库连接会话中进行查询
        query_result = self.connector.query(data_table).filter_by(**data_columns).first()
        ### 使用查询结果对象在SQLite数据库连接会话中进行删除
        self.connector.delete(query_result)
        ### 提交数据库操作
        self.connector.commit()
        print("Delete data well done!")


###################################################################################################################
###################################################################################################################


