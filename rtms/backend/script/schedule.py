# -*-coding=utf-8
import json
import sys

import requests
import json
import sys
sys.path.append('..')
import webtoken_lib
import logging
import log
import manage_cookies
import time
from mysql_lib import *
import paramiko
from zk_operations import *
log.initLogging('/data/rx/log')




header = {
    'Connection': 'close',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip',
    'Cookie': webtoken_lib.get_webtoken()
}
header_audit = {
    'Connection': 'close',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip',
    'Cookie': 'JSESSIONID=%s' % manage_cookies.get_manager_cookies()
}

header_req = {
    'Connection':'close',
    'Content-Type': 'application/json',
    'Accept-Encoding': 'gzip'
}
body_req = {
    "androidVersion": "Android5.1",
    "appVersion": "4.2.8",
    "carrier": "China Mobie",
    "category": "8000",
    "channel": "OPPO",
    "clientIp": "113.105.67.99",
    "clientTime": int(time.time()),
    "contextTag": "[]",
    "count": 0,
    "dataType": "feeds-show",
    "down": 1,
    "imei": "868488029969471",
    "isDown":  True,
    "location": "",
    "model": "OPPO R9k",
    "moduleId": "8000",
    "networkId": "wifi",
    "openId": "0",
    "osVersion": "V3.0.0",
    "pageSize": 0,
    "pageStart": 0,
    "posIds": "1",
    "romVersion": "R9k_11_A.01_160418",
    "sdkVersion": "",
    "seqId": "",
    "sessionId": "",
    "supportSpecs": "1,2,3,4",
    "systemId": "2007",
    "ua": "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; OPPO R9k Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/38.0.0.0 Mobile Safari/537.36 OppoBrowser/4.2.8der uuid/f98f9ca5-f090-40c6-a686-a345f096dcdf",
    "up": 0
}


def add_schedule():
    time1=int(time.time())
    time2=time.strftime("%Y-%m-%d", time.localtime(time1))
    body = {
        "orderId": 309,
        "timeSet1": 0,
        "posSelect": 0,
        "timeSet": "3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3",
        "targetId": 0,
        "posId": 82,
        "daterange": "%s~2017-04-30" % time2,
        "beginTime": time1,
        "endTime": "1493567999",
        "cpm": 1,
        "totalCpm": 10000
    }
    try:
        url = 'http://e.oppo.cn/contract/schedule/add'
        resp = requests.post(url, data=body, headers=header)
        resp.close()
        if resp.status_code!=200:
            logging.error('add_schedule_fail')
            logging.info('add_schedule_code:'+str(resp.status_code))
            logging.info(resp.content)
            sys.exit(1)
        else:
            result = resp.json()
            result2 = json.dumps(result, ensure_ascii=False)
            print result2
            code=result['code']
            if code!=0:
                logging.error('add_schedule_codefail')
                logging.info('add_schedule_code:'+result2.encode('utf-8'))
                sys.exit(2)
            else:
                scheduleId = result['data']['scheduleId']
                return scheduleId
    except Exception as e:
        logging.error(Exception, 'add_schedule_Exception',e)
        sys.exit(3)

def submit_order():
    try:
        url = 'http://e.oppo.cn/contract/order/submit/309'
        resp = requests.post(url, headers=header)
        resp.close()
        if resp.status_code != 200:
            logging.error('submit_order_fail')
            logging.info('submit_order_code:'+str(resp.status_code))
            logging.info(resp.content)
            sys.exit(1)
        else:
            result = resp.json()
            result2 = json.dumps(result, ensure_ascii=False)
            code = result['code']
            print result2
            if code != 0:
                logging.error('submit_order_codefail')
                logging.info('submit_order_code:'+result2.encode('utf-8'))
                sys.exit(2)
            else:
                pass
    except Exception as e:
        logging.error(Exception, 'submit_order_Exception', e)
        exit(3)
def delete_schedule(scheduleId):
    try:
        url = 'http://e.oppo.cn/contract/schedule/%s/delete' %scheduleId
        resp = requests.post(url, headers=header)
        resp.close()
        if resp.status_code != 200:
            logging.error('delete_schedule_fail')
            logging.info('delete_schedule_code:'+str(resp.status_code))
            logging.info(resp.content)
            sys.exit(1)
        else:
            result = resp.json()
            result2 = json.dumps(result, ensure_ascii=False)
            code = result['code']
            print result2
            if code != 0:
                logging.error('delete_schedule_codefail')
                logging.info('delete_schedule_code:'+result2.encode('utf-8'))
                sys.exit(2)
            else:
                pass
    except Exception as e:
        logging.error(Exception, 'delete_schedule_Exception', e)
        exit(3)
def create_contractAd(scheduleId):
    body = {
    "posId":"82",
    "scheduleId":  scheduleId,
    "orderId":309,
    "adDates": "20170309,20170310,20170311,20170312,20170313,20170314,20170315,20170316,20170317,20170318,20170319,20170320,20170321,20170322,20170323,20170324,20170325,20170326,20170327,20170328,20170329,20170330,20170331,20170401,20170402,20170403,20170404,20170405,20170406,20170407,20170408,20170409,20170410,20170411,20170412,20170413,20170414,20170415,20170416,20170417,20170418,20170419,20170420,20170421,20170422,20170423,20170424,20170425,20170426,20170427,20170428,20170429,20170430",
    "name": "新建信息流合约",
    "commercialType": 21,
    "targetUrl": "https://www.baidu.com",
    "creativeTypeId": 87,
    "creativeDetail.creativeTitle": "新建信息流合约",
    "creativeDetail.creativeDesc":   "新建信息流合约",
    "creativeDetail.showTime": 2000,
    "limitCircles": 1,
    "limitCircle": 0,
    "limitTimes": 0,
    "materialsJson": '[{"materialUrl":"contract/mat_pic/201703/10/114_1489131297.jpg","materialMd5":"ad4d46af0e5010a3e2532ea3c6fc7e87","materialSize":398158,"materialType":1}]'
    }
    try:
        url = 'http://e.oppo.cn/contract/ad/add'
        resp = requests.post(url, data=body, headers=header)
        resp.close()
        if resp.status_code != 200:
            logging.error('create_contractAd_fail')
            logging.info('create_contractAd_code:'+str(resp.status_code))
            logging.info(resp.content)
            sys.exit(1)
        else:
            result = resp.json()
            result2 = json.dumps(result, ensure_ascii=False)
            code = result['code']
            print result2
            if code != 0:
                logging.error('create_contractAd_codefail')
                logging.info('create_contractAd_code:'+result2.encode('utf-8'))
                sys.exit(2)
            else:
                adId = result['adId']
                return adId
    except Exception as e:
        logging.error(Exception, 'create_contractAd_Exception', e)
        exit(3)
def delete_contracrAd(contractAdId):
    body = {
        'adId': contractAdId
    }
    try:
        url = 'http://e.oppo.cn/contract/ad/delete'
        resp = requests.post(url, data=body, headers=header)
        resp.close()
        if resp.status_code != 200:
            logging.error('delete_contracrAd_fail')
            logging.info('delete_contracrAd_code:'+str(resp.status_code))
            logging.info(resp.content)
            sys.exit(1)
        else:
            result = resp.json()
            result2 = json.dumps(result, ensure_ascii=False)
            code = result['code']
            print result2
            if code != 0:
                logging.error('delete_contracrAd_codefail')
                logging.info('delete_contracrAd_code:'+result2.encode('utf-8'))
                sys.exit(2)
            else:
                pass
    except Exception as e:
        logging.error(Exception, 'delete_contracrAd_Exception', e)
        exit(3)
def audit_order():
    body = {
        'orderId': 309,
        'status':1,
        'auditDesc':'aaa'
    }
    try:
        url = 'http://appex.oppo.cn/adsOrder/orderAudit'
        resp = requests.post(url, data=body, headers=header_audit)
        resp.close()
        if resp.status_code != 200:
            logging.error('audit_order_fail')
            logging.info('audit_order_code:' + str(resp.status_code))
            logging.info(resp.content)
            exit(1)
        else:
            result = resp.json()
            result2 = json.dumps(result, ensure_ascii=False)
            print result2
            code = result['code']
            if code != 1001:
                logging.error('audit_order_codefail')
                logging.info('audit_order_code:'+result2.encode('utf-8'))
                sys.exit(2)
            else:
                pass
    except Exception as e:
        logging.error(Exception, 'audit_order_Ad_Exception', e)
        exit(3)

def audit_contractAd(contractAdid):
    body = {
        'audiId': '%s,'%contractAdid
    }
    try:
        url = 'http://appex.oppo.cn/adsContractAudit/audiYesAll'
        resp = requests.post(url, data=body, headers=header_audit)
        resp.close()
        if resp.status_code != 200:
            logging.error('audit_contractAd_fail')
            logging.info('audit_contractAd_code:' + str(resp.status_code))
            logging.info(resp.content)
            exit(1)
        else:
            result = resp.json()
            result2 = json.dumps(result, ensure_ascii=False)
            print result2
            code = result['code']
            if code != 1001:
                logging.error('audit_contractAd_fail')
                logging.info('audit_contractAd_code:'+result2.encode('utf-8'))
                sys.exit(2)
            else:
                pass
    except Exception as e:
        logging.error(Exception, 'audit_contractAd_Exception', e)
        exit(3)
def audit_feedAd(feedadId):
    body = {
        'audiId': '%s'%feedadId
    }
    try:
        url = 'http://appex.oppo.cn/adsfeedsauditing/audiYes'
        resp = requests.post(url, data=body, headers=header_audit)
        resp.close()
        if resp.status_code != 200:
            logging.error('audit_feedAd_fail')
            logging.info('audit_feedAd_code:' + str(resp.status_code))
            logging.info(resp.content)
            exit(1)
        else:
            result = resp.json()
            result2 = json.dumps(result, ensure_ascii=False)
            print result2
            code = result['code']
            if code != 1001:
                logging.error('audit_feedAd_fail')
                logging.info('audit_feedAd_code:'+result2.encode('utf-8'))
                sys.exit(2)
            else:
                pass
    except Exception as e:
        logging.error(Exception, 'audit_feedAd_Exception', e)
        exit(3)


def paramiko_delete_schedule():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('183.131.22.111', port=1028, username='advert', password='advert1234', look_for_keys=False,
                allow_agent=False)
    channel = ssh.invoke_shell()
    channel.send('mysql -h172.30.248.231 -umysql -p123456 -A\n')
    while not channel.recv_ready():
        time.sleep(1)
    channel.send('use ads_contract\n')
    while not channel.recv_ready():
        time.sleep(1)
    channel.send('delete from ads_contract_schedule where owner_id=114;\n')
    while not channel.recv_ready():
        time.sleep(1)
    if 'Query OK' in channel.recv(1024):
        logging.info('delete schedule ok')
    else:
        logging.error('delete schedule fail')
    ssh.close()

def reaf_config(i):
    with open("/data/rx/feeds_auto/config", 'r') as f:
        return f.readlines()[i]

def mysql_delete_schedule():
    mysql_cmd('172.30.248.231', 'mysql', '123456',
              sqls='use ads_contract;delete from ads_contract_schedule where order_id=309;')
def mysql_delete_contractAd():
    mysql_cmd('172.30.248.231', 'mysql', '123456',
              sqls='use ads_contract;delete from ads_contract_ad where order_id=309;')

def set_zk(i):
    test_zk(reaf_config(i).split('-')[0], reaf_config(i).split('-')[1], reaf_config(i).split('-')[2])

def feeds_req(adId):
    url = 'http://183.131.22.111/feeds/com.oppo.os.ads.show.feed.service.IFeedListRankSvc'
    try:
        resp = requests.post(url, json=body_req, headers=header_req)
        resp.close()
        if resp.status_code != 200:
            logging.error('feeds_req1_fail')
            logging.info('feeds_req1_code:' + str(resp.status_code))
            logging.info(resp.content)
            exit(1)
        else:
            result = resp.json()
            result2 = json.dumps(result, ensure_ascii=False)
            adid = result['data']['adList'][0]['transparent'].split(',')[0]
            transparent = result['data']['adList'][0]['transparent'].split(',')[12].split('-')[0]
            print result2
            if (adid!=adId)&(transparent!='2_1_1'):
                logging.error('feeds_req1_fail')
                logging.info('feeds_req1_code:' + result2.encode('utf-8'))
                exit(2)
            else:
                pass
    except Exception as e:
        print Exception, '====', e
        exit(3)
    try:
        resp = requests.post(url, json=body_req, headers=header_req)
        resp.close()
        if resp.status_code != 200:
            logging.error('feeds_req2_fail')
            logging.info('feeds_req2_code:' + str(resp.status_code))
            logging.info(resp.content)
            exit(1)
        else:
            result = resp.json()
            result2 = json.dumps(result, ensure_ascii=False)
            adList = result['data']['adList']
            print result2
            if adList!=[]:
                logging.error('feeds_req2_fail')
                logging.info('feeds_req2_code:' + result2.encode('utf-8'))
                exit(2)
            else:
                pass
    except Exception as e:
        print Exception, '====', e
        exit(3)


if __name__ == '__main__':
   # feeds_req(895)
   # id= add_schedule()
   # adId=create_contractAd(id)
   # submit_order()
   # audit_contractAd(adId)
   # audit_order()
   # feeds_req()
   # delete_schedule(id)
 #   paramiko_delete_schedule()
    delete_contracrAd(902)



