# -*- coding: utf-8 -*-
# author:shihua
# designer:shihua
# coder:shihua
# 这是一个数据实例管理类，包括算法、模型、参数、应用、数据的信息管理和二进制对象的存储管理
"""
模块介绍
-------

这是一个数据实例类，包括算法、模型、参数、应用、数据的信息管理和二进制对象的存储管理

设计模式：

    （1）函数式编程 

关键点：    

    （1）信息管理

    （2）存储管理

主要功能：            

    （1）算法、模型、参数、应用、数据的信息管理
    
    （2）二进制对象的存储管理                                

使用示例
-------


类说明
------

"""



####### 载入程序包 ##########################################################
############################################################################



from sunbasket import SQLiteManager
from sqlalchemy import Column, String, create_engine, Integer, DateTime,Text,LargeBinary
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import pickle
import yaml
import sunbasket



####### 数据实例管理类 ########################################################
### 设计模式：                                                              ###
### （1）函数式编程                                                          ###
### 关键点：                                                                ###
### （1）信息管理                                                           ###
### （2）存储管理                                                           ###
### 主要功能：                                                              ###
### （1）算法、模型、参数、应用、数据的信息管理                                ###
### （2）二进制对象的存储管理                                                ###
##############################################################################


####### 辅助工具集合 ######################################################################################
##########################################################################################################


def sqlite_config(connect_info):
    '''
    函数功能：

        定义一个SQLite数据库连接和ORM对象基类开放的函数

    参数：
        connect_info (str): SQLite连接信息

    返回：
        Base (object): ORM对象基类
        tmp_SQLiteManager (object): SQLite连接器
    '''

    ### 配置SQLite数据记录table
    if connect_info == None:
        SQLitelog_dict = sunbasket.SQLITE_CONFIG
        connect_info = SQLitelog_dict['connect']
    else:
        connect_info = connect_info
    print(connect_info)
    ### 加载SQLite连接器
    tmp_SQLiteManager = sunbasket.SQLiteManager(connect_info)
    ### 声明数据基类
    Base= declarative_base(tmp_SQLiteManager.engine)

    return Base,tmp_SQLiteManager


def serialize_data(data):
    '''
    函数功能：

        定义一个使用pickle序列化数据对象的函数

    参数：
        data (object): 数据对象

    返回：
        serialized_data (bytes): 序列化后的二进制对象 
    '''

    ### 序列化数据对象
    serialized_data = pickle.dumps(data)

    return serialized_data


def deserialize_data(serialized_data):
    '''
    函数功能：

        定义一个使用pickle反序列化数据对象的函数

    参数：
        serialized_data (bytes): 序列化后的二进制对象

    返回：
        data (object): 数据对象
    '''    

    ### 反序列化数据对象
    data = pickle.loads(serialized_data)

    return data



####### 信息管理类 ######################################################################################
########################################################################################################



### 算法信息管理
class AlgorithmInfoManager(object):
    '''
    类介绍：

        这是一个算法信息管理类
    '''


    def __init__(self,connect_info=None,data_dict=None):
        '''
        属性功能：

            定义一个初始化属性的方法

        参数：
            connect_info (str): SQLite连接信息
            data_dict (dict): 数据字典

        返回：
            无
        '''

        self.data,self.SQLiteManager = self.gen_algorithm_info(connect_info=connect_info,data_dict=data_dict)
        print("Algorithm info create well done!")


    def gen_algorithm_info(self,connect_info=None,data_dict=None):
        '''
        方法功能：

            定义一个生成算法信息ORM对象和SQLite数据连接器的函数

        参数：
            connect_info (str): SQLite连接信息
            data_dict (dict): 数据字典        

        返回：
            data (Object): ORM对象 
            tmp_SQLiteManager (Object): SQLite连接器
        '''

        ### 根据连接信息创建Base连接基类和SQLite连接管理器
        Base,tmp_SQLiteManager = sqlite_config(connect_info=connect_info)
        ### 具体数据ORM对象类
        class AlgorithmInfo(Base):
            '''
            类介绍：

                这是一个算法信息数据ORM对象类
            '''
            __tablename__='AlgorithmInfo'
            index = Column(Integer, autoincrement=True, primary_key=True)
            name = Column(Text)
            version = Column(Text)
            summary = Column(Text)
            config = Column(Text)
            remark = Column(Text)
            homepage = Column(Text)
            author = Column(Text)
            authoremail = Column(Text)
            license = Column(Text)
            requires = Column(Text)
            requiredby = Column(Text)
        ### 数据表预处理
        del_list = [AlgorithmInfo.__table__,]
        # Base.metadata.drop_all(tables=del_list)
        Base.metadata.create_all(tables=del_list)
        ### 根据数据字典创建具体数据表对象
        data = AlgorithmInfo(**data_dict)

        return data,tmp_SQLiteManager


    def add_data(self):
        '''
        方法功能：

            定义一个添加数据到数据库的函数

        参数：
            无

        返回：
            无
        '''

        ### SQLite数据增加操作
        self.SQLiteManager.insert_data(self.data)
        print('Add algorithm info well done!')



### 模型信息管理
class ModelInfoManager(object):
    '''
    类介绍：

        这是一个模型信息管理类
    '''


    def __init__(self,connect_info=None,data_dict=None):
        '''
        属性功能：

            定义一个初始化属性的方法

        参数：
            connect_info (str): SQLite连接信息
            data_dict (dict): 数据字典

        返回：
            无
        '''

        self.data,self.SQLiteManager = self.gen_model_info(connect_info=connect_info,data_dict=data_dict)
        print("Model info create well done!")


    def gen_model_info(self,connect_info=None,data_dict=None):
        '''
        方法功能：

            定义一个生成模型信息ORM对象和SQLite数据连接器的函数

        参数：
            connect_info (str): SQLite连接信息
            data_dict (dict): 数据字典        

        返回：
            data (Object): ORM对象 
            tmp_SQLiteManager (Object): SQLite连接器
        '''

        ### 根据连接信息创建Base连接基类和SQLite连接管理器
        Base,tmp_SQLiteManager = sqlite_config(connect_info=connect_info)
        ### 具体数据ORM对象类
        class ModelInfo(Base):
            '''
            类介绍：

                这是一个模型信息数据ORM对象类
            '''
            __tablename__='ModelInfo'
            index = Column(Integer, autoincrement=True, primary_key=True)
            name = Column(Text)
            version = Column(Text)
            summary = Column(Text)
            config = Column(Text)
            remark = Column(Text)
            requires = Column(Text)
            data = Column(Text)
            algorithm = Column(Text)
        ### 数据表预处理
        del_list = [ModelInfo.__table__,]
        # Base.metadata.drop_all(tables=del_list)
        Base.metadata.create_all(tables=del_list)
        ### 根据数据字典创建具体数据表对象
        data = ModelInfo(**data_dict)

        return data,tmp_SQLiteManager


    def add_data(self):
        '''
        方法功能：

            定义一个添加数据到数据库的函数

        参数：
            无

        返回：
            无
        '''

        ### SQLite数据增加操作
        self.SQLiteManager.insert_data(self.data)
        print('Add model info well done!')



### 参数信息管理
class ParameterInfoManager(object):
    '''
    类介绍：

        这是一个参数信息管理类
    '''


    def __init__(self,connect_info=None,data_dict=None):
        '''
        属性功能：

            定义一个初始化属性的方法

        参数：
            connect_info (str): SQLite连接信息
            data_dict (dict): 数据字典

        返回：
            无
        '''

        self.data,self.SQLiteManager = self.gen_parameter_info(connect_info=connect_info,data_dict=data_dict)
        print("Parameter info create well done!")


    def gen_parameter_info(self,connect_info=None,data_dict=None):
        '''
        方法功能：

            定义一个生成参数信息ORM对象和SQLite数据连接器的函数

        参数：
            connect_info (str): SQLite连接信息
            data_dict (dict): 数据字典        

        返回：
            data (Object): ORM对象 
            tmp_SQLiteManager (Object): SQLite连接器
        '''

        ### 根据连接信息创建Base连接基类和SQLite连接管理器
        Base,tmp_SQLiteManager = sqlite_config(connect_info=connect_info)
        ### 具体数据ORM对象类
        class ParameterInfo(Base):
            '''
            类介绍：

                这是一个参数信息数据ORM对象类
            '''
            __tablename__='ParameterInfo'
            index = Column(Integer, autoincrement=True, primary_key=True)
            name = Column(Text)
            version = Column(Text)
            summary = Column(Text)
            config = Column(Text)
            remark = Column(Text)
            datatype = Column(Text)
            requiredby = Column(Text)
        ### 数据表预处理
        del_list = [ParameterInfo.__table__,]
        # Base.metadata.drop_all(tables=del_list)
        Base.metadata.create_all(tables=del_list)
        ### 根据数据字典创建具体数据表对象
        data = ParameterInfo(**data_dict)

        return data,tmp_SQLiteManager


    def add_data(self):
        '''
        方法功能：

            定义一个添加数据到数据库的函数

        参数：
            无

        返回：
            无
        '''

        ### SQLite数据增加操作
        self.SQLiteManager.insert_data(self.data)
        print('Add parameter info well done!')



### 应用信息管理
class ApplicationInfoManager(object):
    '''
    类介绍：

        这是一个应用信息管理类
    '''


    def __init__(self,connect_info=None,data_dict=None):
        '''
        属性功能：

            定义一个初始化属性的方法

        参数：
            connect_info (str): SQLite连接信息
            data_dict (dict): 数据字典

        返回：
            无
        '''

        self.data,self.SQLiteManager = self.gen_application_info(connect_info=connect_info,data_dict=data_dict)
        print("Application info create well done!")


    def gen_application_info(self,connect_info=None,data_dict=None):
        '''
        方法功能：

            定义一个生成应用信息ORM对象和SQLite数据连接器的函数

        参数：
            connect_info (str): SQLite连接信息
            data_dict (dict): 数据字典        

        返回：
            data (Object): ORM对象 
            tmp_SQLiteManager (Object): SQLite连接器
        '''

        ### 根据连接信息创建Base连接基类和SQLite连接管理器
        Base,tmp_SQLiteManager = sqlite_config(connect_info=connect_info)
        ### 具体数据ORM对象类
        class ApplicationInfo(Base):
            '''
            类介绍：

                这是一个应用信息数据ORM对象类
            '''
            __tablename__='ApplicationInfo'
            index = Column(Integer, autoincrement=True, primary_key=True)
            name = Column(Text)
            version = Column(Text)
            summary = Column(Text)
            config = Column(Text)
            remark = Column(Text)
            requires = Column(Text)
            project = Column(Text)
        ### 数据表预处理
        del_list = [ApplicationInfo.__table__,]
        # Base.metadata.drop_all(tables=del_list)
        Base.metadata.create_all(tables=del_list)
        ### 根据数据字典创建具体数据表对象
        data = ApplicationInfo(**data_dict)

        return data,tmp_SQLiteManager


    def add_data(self):
        '''
        方法功能：

            定义一个添加数据到数据库的函数

        参数：
            无

        返回：
            无
        '''

        ### SQLite数据增加操作
        self.SQLiteManager.insert_data(self.data)
        print('Add application info well done!')



### 数据信息管理
class DataInfoManager(object):
    '''
    类介绍：

        这是一个数据信息管理类
    '''


    def __init__(self,connect_info=None,data_dict=None):
        '''
        属性功能：

            定义一个初始化属性的方法

        参数：
            connect_info (str): SQLite连接信息
            data_dict (dict): 数据字典

        返回：
            无
        '''

        self.data,self.SQLiteManager = self.gen_data_info(connect_info=connect_info,data_dict=data_dict)
        print("Data info create well done!")


    def gen_data_info(self,connect_info=None,data_dict=None):
        '''
        方法功能：

            定义一个生成数据信息ORM对象和SQLite数据连接器的函数

        参数：
            connect_info (str): SQLite连接信息
            data_dict (dict): 数据字典        

        返回：
            data (Object): ORM对象 
            tmp_SQLiteManager (Object): SQLite连接器
        '''

        ### 根据连接信息创建Base连接基类和SQLite连接管理器
        Base,tmp_SQLiteManager = sqlite_config(connect_info=connect_info)
        ### 具体数据ORM对象类
        class DataInfo(Base):
            '''
            类介绍：

                这是一个数据信息数据ORM对象类
            '''
            __tablename__='DataInfo'
            index = Column(Integer, autoincrement=True, primary_key=True)
            name = Column(Text)
            version = Column(Text)
            summary = Column(Text)
            config = Column(Text)
            remark = Column(Text)
            requiredby = Column(Text)
            datatype = Column(Text)
            project = Column(Text)
        ### 数据表预处理
        del_list = [DataInfo.__table__,]
        # Base.metadata.drop_all(tables=del_list)
        Base.metadata.create_all(tables=del_list)
        ### 根据数据字典创建具体数据表对象
        data = DataInfo(**data_dict)

        return data,tmp_SQLiteManager


    def add_data(self):
        '''
        方法功能：

            定义一个添加数据到数据库的函数

        参数：
            无

        返回：
            无
        '''

        ### SQLite数据增加操作
        self.SQLiteManager.insert_data(self.data)
        print('Add data info well done!')



####### 存储管理类 ######################################################################################
########################################################################################################



### 模型存储管理
class ModelStoreManager(object):
    '''
    类介绍：

        这是一个模型存储管理类
    '''


    def __init__(self,connect_info=None,data_dict=None):
        '''
        属性功能：

            定义一个初始化属性的方法

        参数：
            connect_info (str): SQLite连接信息
            data_dict (dict): 数据字典

        返回：
            无
        '''

        self.data,self.SQLiteManager = self.gen_model_store(connect_info=connect_info,data_dict=data_dict)
        print("Model store connect well done!")


    @staticmethod
    def get_model_data(connect_info=None,**data_columns):
        '''
        方法功能：

            定义一个获取模型存储数据的方法

        参数：
            connnect_info (str): SQLite连接信息
            data_columns (dict): 条件查询的可选参数列表

        返回：
            tmp_model_data (bytes): 二进制模型数据对象
        '''

        ### 根据连接信息创建Base连接基类和SQLite连接管理器
        Base,tmp_SQLiteManager = sqlite_config(connect_info=connect_info)
        ### 具体数据ORM对象类
        class ModelStore(Base):
            '''
            类介绍：

                这是一个模型存储数据ORM对象类
            '''
            __tablename__='ModelStore'
            index = Column(Integer, autoincrement=True, primary_key=True)
            name = Column(Text)
            version = Column(Text)
            summary = Column(Text)
            config = Column(Text)
            remark = Column(Text)
            data = Column(LargeBinary)        
        tmp_model_data = tmp_SQLiteManager.query_data(data_table=ModelStore,**data_columns)

        return tmp_model_data


    def gen_model_store(self,connect_info=None,data_dict=None):
        '''
        方法功能：

            定义一个生成模型存储ORM对象和SQLite数据连接器的函数

        参数：
            connect_info (str): SQLite连接信息
            data_dict (dict): 数据字典        

        返回：
            data (Object): ORM对象 
            tmp_SQLiteManager (Object): SQLite连接器
        '''

        ### 根据连接信息创建Base连接基类和SQLite连接管理器
        Base,tmp_SQLiteManager = sqlite_config(connect_info=connect_info)
        ### 具体数据ORM对象类
        class ModelStore(Base):
            '''
            类介绍：

                这是一个模型存储数据ORM对象类
            '''
            __tablename__='ModelStore'
            index = Column(Integer, autoincrement=True, primary_key=True)
            name = Column(Text)
            version = Column(Text)
            summary = Column(Text)
            config = Column(Text)
            remark = Column(Text)
            data = Column(LargeBinary)
        ### 数据表预处理
        del_list = [ModelStore.__table__,]
        # Base.metadata.drop_all(tables=del_list)
        Base.metadata.create_all(tables=del_list)
        ### 根据数据字典创建具体数据表对象
        data = ModelStore(**data_dict)

        return data,tmp_SQLiteManager


    def add_data(self):
        '''
        方法功能：

            定义一个添加数据到数据库的函数

        参数：
            无

        返回：
            无
        '''

        ### SQLite数据增加操作
        self.SQLiteManager.insert_data(self.data)
        print('Add model store well done!')



##################################################################################################################################
##################################################################################################################################


