#!/usr/bin/env python
# -*-coding:utf-8-*-
import requests
import json
import sys
import locale
import os
import codecs

orderIdServerUrl="http://172.18.10.73:9087/orderId"
#order接入的服务地址，需要包含工程名，不能以/结尾
orderAccessServerUrl="http://172.18.10.73:9087/orderGateway"
class ProcessResult(object):
    def __init__(self,retCode,retMsg):
        return {'retCode':retCode,'retMsg':retMsg}

    def __init__(self):
        return {'retCode':0, 'retMsg': ""}
    pass
#根据订单返回的对象获取返回数值，返回值为int
def getRetCode(processResult):
    try:
        return processResult['retCode']
    except Exception:
        return -1
#根据订单系统返回值获取responseInfo对象，返回的类型是dict
def getResponseInfo(processResult):
    try:
        responseInfo = processResult['responseInfo'];
        return json.loads(responseInfo)
    except Exception:
        return ""
def getContextValue(responseInfo,key):
    try:

        return responseInfo[key]
    except Exception:
        return ""
def getDbid(orderId):
    try:
        #print('getDbid:' + orderId + ' len='+str(len(orderId)))
        if len(orderId) >= 7:
            #print('return :' + orderId[-4:])
            return orderId[-4:]
        return ""
    except Exception:
        return ""
#定义创建的订单的上下文
class OrderMainContext(object):
    #初始化map为空
    contextDatas={}
    dbid="000000"
    def __init__(self, category, orderId, ownerKey):
        self.setOrderId(orderId)
        self.setCategory(category)
        self.setOwnerKey(ownerKey)
    def getCategory(self):
        return self.category
    def setCategory(self,category):
        self.category=category

    def getOrderId(self):
        return self.orderId

    def setOrderId(self, orderId):
        self.orderId = orderId
        if len(orderId)>=7:
            self.dbid=orderId[-4:]
    def setOwnerKey(self, ownerKey):
        self.ownerKey = ownerKey
    def getOwnerKey(self):
        return self.ownerKey

    def getContextDatas(self):
        return self.contextDatas
    def setContextDatas(self,contextDatas):
        self.contextDatas=contextDatas
    def getDbid(self):
        return self.dbid
    def setDbid(self,dbid):
        self.dbid = dbid
    pass

def _byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

'''
获取订单ID
'''
def getOrderId(category,ownerKey):
    #构造服务器地址
    serverUrl = '%s/%s/%s/createOrderId' % (orderIdServerUrl, category,ownerKey)
    #构造请求参数
    payload = {'requestTransId': '', 'requestTime': '', 'token': '', 'jsonString': ''}
    r = requests.post(url=serverUrl, json=payload)  # 带参数的GET请求
    r.encoding = 'utf-8'  # 这里添加一行
    response = json_loads_byteified(r.text)
    if response['retCode'] == 0:
        return(response['responseInfo'])
    else:
        print("get orderId Error:")
        print(response)
        print('\n')
    return ""

'''
创建订单
'''
def createOrder(orderMainContext):
    category = orderMainContext.getCategory()
    ownerKey = orderMainContext.getOwnerKey()
    dbId = orderMainContext.getDbid()
    orderId = orderMainContext.getOrderId()
    #构造服务器地址 /{category}/{dbId}/{orderId}/createOrder
    serverUrl = '%s/%s/%s/%s/createOrder' % (orderAccessServerUrl,category,dbId,orderId)
    #构造请求参数
    #print("orderMainContext:" + serverUrl +' len:' + str(len(orderMainContext.getContextDatas())))
    #orderMainContext.setContextDatas({'aaa':'dddd','eee':'fffff'})
    #print("orderMainContext:" + serverUrl + ' context:' + json.dumps((orderMainContext.getContextDatas())))
    if any(orderMainContext.getContextDatas()):
        payload = {'orderId': orderMainContext.getOrderId(), 'catetory': orderMainContext.getCategory(),
                   'ownerKey': orderMainContext.getOwnerKey(), 'contextDatas':orderMainContext.getContextDatas()}
    else:
        payload = {'orderId': orderMainContext.getOrderId(), 'catetory': orderMainContext.getCategory(),
                       'ownerKey': orderMainContext.getOwnerKey()}
    #payload = {'orderId':orderMainContext.getOrderId(),'catetory':orderMainContext.getCategory(),'ownerKey':orderMainContext.getOwnerKey()}
    print("create order :" + serverUrl +' payload:'+ json.dumps(payload))
    r = requests.post(url=serverUrl, json=payload)  # 带参数的GET请求
    r.encoding = 'utf-8'  # 这里添加一行
    response = json_loads_byteified(r.text)
    return response
'''
启动订单
'''
def startOrder(category,orderId):
    dbId = getDbid(orderId)
    if dbId.strip():
        processResult = ProcessResult(-1,'dbid is null')
        return processResult
    #构造服务器地址 /{category}/{dbId}/{orderId}/startOrder
    serverUrl = '%s/%s/%s/%s/startOrder' % (orderAccessServerUrl,category,dbId,orderId)
    r = requests.get(url=serverUrl)  # 带参数的GET请求
    r.encoding = 'utf-8'  # 这里添加一行
    response = json_loads_byteified(r.text)
    return response

'''
获取订单系统中的上下文
'''
def getOrderContext(category,orderId,keyList):
    dbId = getDbid(orderId)
    #构造服务器地址 /{category}/{dbId}/{orderId}/getContextData
    serverUrl = '%s/%s/%s/%s/getContextData' % (orderAccessServerUrl,category,dbId,orderId)
    #构造请求参数
    payload ={'jsonString':json.dumps(keyList)}
    r = requests.post(url=serverUrl, json=payload)  # 带参数的GET请求
    r.encoding = 'utf-8'  # 这里添加一行
    response = json_loads_byteified(r.text)
    return response
'''
保存上下文到订单系统中
'''
def putOrderContext(category,orderId,contextMap):
    dbId = getDbid(orderId)
    #构造服务器地址 /{category}/{dbId}/{orderId}/getContextData
    serverUrl = '%s/%s/%s/%s/putContextData' % (orderAccessServerUrl,category,dbId,orderId)
    #构造请求参数
    orderMainContext = OrderMainContext(category,orderId,'')
    orderMainContext.setContextDatas(contextMap)
    if any(orderMainContext.getContextDatas()):
        payload = {'orderId': orderMainContext.getOrderId(), 'catetory': orderMainContext.getCategory(),
                   'ownerKey': orderMainContext.getOwnerKey(), 'contextDatas': orderMainContext.getContextDatas()}
    else:
        payload = {'orderId': orderMainContext.getOrderId(), 'catetory': orderMainContext.getCategory(),
                   'ownerKey': orderMainContext.getOwnerKey()}
    print("putOrderContext  :" + serverUrl + ' payload:' + json.dumps(payload))

    r = requests.post(url=serverUrl, json=payload)  # 带参数的GET请求
    r.encoding = 'utf-8'  # 这里添加一行
    response = json_loads_byteified(r.text)
    return response
'''



reload(sys)
sys.setdefaultencoding('utf8')
category='coojisu_playing'
#orderId = getOrderId(category,'121212')
orderId = '62382880070002'
print('getorderId:' + orderId)
orderMainContext = OrderMainContext(category,orderId,'33333')


processResult = createOrder(orderMainContext)
print("createOrder return:" + json.dumps(processResult))

contextMap={'testkey1':'testkeyValue1','testKey2':'testKeyValue2'}
processResult = putOrderContext(category,orderId,contextMap)
if processResult['retCode']==0:
    print("put orderContext Success")
print("putOrderContext return:" + json.dumps(processResult))

keyList = []
keyList.append('testkey1')
keyList.append('testKey2')
processResult = getOrderContext(category,orderId,keyList)
print("getOrderContext return:" + json.dumps(processResult))
if processResult['retCode']==0:
    responseInfo = getResponseInfo(processResult)
    print(type(responseInfo))
    print(getContextValue(responseInfo,'testkey1'))
'''
'''
print sys.stdout.encoding + " - sys.stdout.encoding:"
sys.stdout = codecs.getwriter('utf8')(sys.stdout) 
print sys.stdout.encoding + " - sys.stdout.encoding:"
'''
