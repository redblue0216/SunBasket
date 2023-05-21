from sunbasket.data import AlgorithmInfoManager,ModelInfoManager,ParameterInfoManager,ApplicationInfoManager,DataInfoManager,ModelStoreManager,serialize_data,deserialize_data



### 连接数据库 
connect_info = 'sqlite:///E:\\workspace\\SunBasket\\Demo\\test.db'
### 算法信息管理
algorithm_info_data_dict = {
    'name': 'test',
    'version': 'v001',
    'summary': 'test summary',
    'config': 'test config',
    'remark': 'test remark',
    'homepage': 'test homepage',
    'author': 'shihua',
    'authoremail': 'xxxxx@xxx.com',
    'license': 'MIT',
    'requires': 'numpy,pandas',
    'requiredby': 'xxxx'
}
algorithm_info = AlgorithmInfoManager(connect_info=connect_info,data_dict=algorithm_info_data_dict)
algorithm_info.add_data()


### 模型信息管理
model_info_data_dict = {
    'name': 'test',
    'version': 'v001',
    'summary': 'test summary',
    'config': 'test config',
    'remark': 'test remark',
    'requires': 'numpy,pandas',
    'data': 'test data',
    'algorithm': 'test algorithm'
}
model_info = ModelInfoManager(connect_info=connect_info,data_dict=model_info_data_dict)
model_info.add_data()


### 参数信息管理
parameter_info_data_dict = {
    'name': 'test',
    'version': 'v001',
    'summary': 'test summary',
    'config': 'test config',
    'remark': 'test remark',
    'datatype': 'test datatype',
    'requiredby': 'xxxx'
}
parameter_info = ParameterInfoManager(connect_info=connect_info,data_dict=parameter_info_data_dict)
parameter_info.add_data()


### 应用信息管理
application_info_data_dict = {
    'name': 'test',
    'version': 'v001',
    'summary': 'test summary',
    'config': 'test config',
    'remark': 'test remark',
    'requires': 'test requires',
    'project': 'xxxx'
}
application_info = ApplicationInfoManager(connect_info=connect_info,data_dict=application_info_data_dict)
application_info.add_data()


### 数据信息管理
data_info_data_dict = {
    'name': 'test',
    'version': 'v001',
    'summary': 'test summary',
    'config': 'test config',
    'remark': 'test remark',
    'requireby': 'test requiredby',
    'datatype': 'test datatype',
    'project': 'xxxx'
}
data_info = DataInfoManager(connect_info=connect_info,data_dict=data_info_data_dict)
data_info.add_data()


### 模型存储管理
class TestModel(object):

    def __init__(self,name):
        self.name = name
        self.arg = 150

    def add(self,a,b):
        return a+b
test_model = TestModel(name='testmodel')
### 序列化数据对象
serialized_data = serialize_data(data=test_model) 
model_store_data_dict = {
    'name': 'test',
    'version': 'v001',
    'summary': 'test summary',
    'config': 'test config',
    'remark': 'test remark',
    'data': serialized_data
}
model_store = ModelStoreManager(connect_info=connect_info,data_dict=model_store_data_dict)
model_store.add_data()


### 读取目标模型
tmp_model = model_store.get_model_data(connect_info=connect_info,name='test',version='v001')
### 反序列化数据对象
tmp_model_data = deserialize_data(serialized_data=tmp_model.data)
print(tmp_model_data.name,tmp_model_data.arg,tmp_model_data.add(1,2))


