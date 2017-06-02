# -*-coding=utf-8
import json
import requests
from Signature import *
import sys
sys.path.append('..')
import log
import logging
# log.initLogging('/data/rx/log')

sign = Signature('19', '1113', '9798384b2ccb4f2aa372520758b5b8f8',str(int(time.time())))
token = sign.create_token_base64()
decode = sign.decode_base64(token)
contentType = 'application/x-www-form-urlencoded'  # form数据封装到http body中，然后发送到server  name=test&gender=male&email=iefreer@live.cn
header = {
    'Content-Type': contentType,
    'Authorization': 'Bearer %s' % token
}
boby = {
    "biz":2,
    "name":"自动化内部广告",
    "specId":2,
    "adType":12,
    "brandName":"自动化内部广告",
    "copywriter":"aaa",
    "tags":"自动化内部广告",
    "targetUrl":"http://www.baidu.com",
    'materialUrls':'["http://www.vivibride.cn/uploads/allimg/130306/16-130306161552619.jpg"]',
    "price":1000,
    "billingType":2,
    "ownerId":137,
    "planId":3961

}
def create_ad_feeds():
    try:
        url = 'http://183.131.22.111/v1/ad/create'
        resp = requests.post(url, data=boby, headers=header)
        resp.close()
        if resp.status_code != 200:
            logging.error('create_ad_feeds_fail')
            logging.info('create_ad_feeds_code:' + str(resp.status_code))
            logging.info(resp.content)
            sys.exit(1)
        else:
            result = resp.json()
            result2 = json.dumps(result, ensure_ascii=False)
            print result2
            code = result['code']
            if code != 0:
                logging.error('create_ad_feeds_codefail')
                logging.info('create_ad_feeds_code:' + result2.encode('utf-8'))
                sys.exit(2)
            else:
                feedId = result['data']['adId']
                return feedId
    except Exception as e:
        logging.error(Exception, 'create_ad_feeds_Exception', e)
        sys.exit(3)
if __name__ == '__main__':
    create_ad_feeds()
