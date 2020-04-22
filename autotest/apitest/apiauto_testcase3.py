import requests,time,sys,re
import urllib,zlib
import pymysql
import os
from trace import CoverageResults
import json
from idlelib.rpc import response_queue
from time import sleep
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import unittest
from apitest.connect_db import OperationMysql
import json
from HTMLTestRunner import HTMLTestRunner
HOSTNAME = '127.0.0.1'
class ApiFow(unittest.TestCase):
    def setUp(self):
        time.sleep(1)
    def test_readSQLcase(self):
        sql = "SELECT id,`apiname`,apiurl,apimethod,apiparamvalue,`apistatus` " \
              "from apitest_apistep " \
              "where apitest_apistep.Apitest_id=3"
        coon = pymysql.connect(user='root',passwd='123456',db='autotest',port=3306,host='127.0.0.1',charset='utf8')
        cursor = coon.cursor()
        aa = cursor.execute(sql)
        info = cursor.fetchmany(aa)
        for ii in info:
            case_list = []
            case_list.append(ii)
            print(case_list)
           # CredentialId()
            interfaceTest(case_list)
        coon.commit()
        cursor.close()
        coon.close()
    def tearDown(self):
        time.sleep(1)
def interfaceTest(case_list):
    res_flags = []
    requests_urls = []
    response = []
    # strinfo = re.compile('{TaskId}')
    # strinfo1 = re.compile('{AssertId}')
    # strinfo2 = re.compile('{PointId}')
    # assetinfo = re.compile('{assetno}')
    # tasknoinfo = re.compile('{taskno}')
    # schemainfo = re.compile('{schema}')
    for case in case_list:
        try:
            case_id = case[0]
            interface_name = case[1]
            method = case[4]
            url = case[2]
            param = case[3]
            res_check = case[5]
        except Exception as e:
            return '测试用例格式不正确%s'%e

        if method.upper() == 'GET':
            headers = {'Authorization':'','Content-Type':'application/json'}
            print('request is get ' + url + ' body is ' +urlParam(param))
            data = None
            results = requests.get(url=url,data=data,headers=headers,method="GET",verify=False)
            print('response is get')
            print(results)
            res = readRes(results,res_check)
            if 'pass' == res:
                writeResult(case_id,'pass')
                res_flags.append('pass')
                caseWriteResult(case_id,'1')

            else:
                res_flags.append('fail')
                writeResult(case_id,'fail')
                writeBug(case_id, interface_name, url, results, res_check)
                caseWriteResult(case_id, '0')
        if method.upper() == 'PUT':
            headers = {'Authorization':'','Content-Type':'application/json',\
                       'Host':HOSTNAME,'Credential':id}
            body_data = param
            results = requests.put(url=url,data=json.dumps(body_data),headers=headers)
            response.append(results)
            res = readRes(results, res_check)
            if 'pass' == res:
                writeResult(case_id, 'pass')
                res_flags.append('pass')
            else:
                res_flags.append('fail')
                writeResult(case_id, 'fail')
                writeBug(case_id,interface_name,url,results,res_check)
            try:
                preOrderSN(results)
            except:
                print('OK')
        if method.upper() == 'POST':
            headers = {'Authorization':'','Content-Type':'application/json',\
                       'Host':HOSTNAME,'Credential':id}
            results = requests.post(url=url,data=json.dumps(param1),headers=headers)
            response.append(results)
            res = readRes(results, res_check)
            if 'pass' == res:
                writeResult(case_id, 'pass')
                res_flags.append('pass')
            else:
                res_flags.append('fail')
                writeResult(case_id, 'fail')
                writeBug(case_id, interface_name, url, results, res_check)
            try:
                TaskId(results)
            except:
                print('ok1')



def readRes(res,res_check):
    res = res.decode().replace('":"',"=").replace('":',"-")
    res_check = res_check.split(';')
    for s in res_check:
        if s in res:
            pass
        else:
            return  '错误，返回参数和期望结果不一致'+s
def urlParam(param):
    param1 = param.encode('utf-8')
    param1 = param.replace('&quto;','"')
    return param1
def CredentialId():
    global  id
    url = 'http://' + 'api.test.com.cn' + '/api/Security/Authentication/Signin/web'
    body_data = json.dumps({"Identity":'test',"Password":'test'})
    headers = {'Connection':'keep-alive','Content-Type':'application/json'}
    response = requests.post(url=url,data=body_data,headers=headers)
    data = response.text
    regx = '.*"CredentialId":"(.*)","Scene"'
    pm = re.search(regx,data)
    id = pm.group(1)
def preOrderSN(results):
    global preOrderSN
    regx = '.*"preOrderSN":"(.*)","toHome"'
    pm = re.search(regx,results)
    if pm:
        preOrderSN = pm.group(1).encode('utf-8')
        return preOrderSN
    return False
def TaskId(results):
    global TaskId
    regx = '.*"TaskId":(.*),"PlanId"'
    pm = re.search(regx,results)
    if pm :
        TaskId = pm.group(1).encode('utf-8')
        return TaskId
    return False
def taskno(param):
    global  taskno
    a = int(time.time())
    taskno = 'task_' + str(a)
    return taskno
def writeResult(case_id,result):
    result = result.encode('utf-8')
    now = time.strftime("%Y-%m-%d %H:%M:%S" )
    sql = "UPDATE apitest_apistep set apitest_apistep.apistatus=%s where apitest_apistep=%s;"
    param = (result,case_id)
    print('api autotest result is ' +result.decode())
    op_mysql = OperationMysql()
    op_mysql.update_data(sql)
    op_mysql.close()
def writeBug(bug_id,interface_name,request,response,res_check):
    interface_name = interface_name.encode('utf-8')
    res_check = res_check.encode('utf-8')
    request = request.decode('utf-8')
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    bugname = str(bug_id) + '_' + interface_name.encode() + '_出错了'
    bugdetail = '[请求数据<br/>]' + request.decode() + '<br/>' + '[预期结果<br/>]'\
                + res_check.encode() + '<br/>' + '<br/>' + '[相应数据<br/>]' + response.decode()
    print(bugdetail)
    sql = "INSERT INTO `bug_bug`(`bugname`,`bugdetail`,`bugstatus`,`buglevel`,`bugcreater`\
          `bugassign`, `created_time`,`Product_id`)\
            VALUES('%s','%s','1','1','leixiaofang','leixiaofang','%s');" %(bugname,pymysql.escape_string(bugdetail),now)
    op_mysql = OperationMysql()
    op_mysql.add_one(sql)
    op_mysql.close()
def caseWriteResult(case_id,result):
    result = result.encode('utf-8')
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    sql = "UPDATE apitest_apitest set apitest_apitest.apitestresult=%s,apitest.create_time" \
    "=%s where apitest_apitest.id=%s;"
    param = (result,now,case_id)
    print('api autotest result is '+ result.decode())
    op_mysql = OperationMysql()
    op_mysql.add_one(sql)
    op_mysql.close()

if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d %H:%M:%S","time.localtime(time.time())")
    testunit = unittest.TestSuite()
    testunit.addTest(ApiFow("test_readAQLcase"))
    filename = r'D:\python\autotestplat\autotest\apitest\templates\'' + 'apitest_report.html'
    fp = open(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=u'流程接口测试报告',description=u'流程场景接口')
    runner.run(testunit)
    print('Done')
    time.sleep(1)







