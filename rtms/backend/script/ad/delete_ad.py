# -*-coding=utf-8
import json
import requests
from Signature import *
import sys
sys.path.append('..')
import log
import logging
log.initLogging('/data/rx/log')

sign = Signature('19', '1113', '9798384b2ccb4f2aa372520758b5b8f8',str(int(time.time())))
token = sign.create_token_base64()
decode = sign.decode_base64(token)
contentType = 'application/x-www-form-urlencoded'  # form数据封装到http body中，然后发送到server  name=test&gender=male&email=iefreer@live.cn
header = {
    'Content-Type': contentType,
    'Authorization': 'Bearer %s' % token
}

def delete_ad(feedId):
    boby = {
        "biz": 2,
        "ownerId": 137,
        "adId": feedId,
    }
    try:
        url = 'http://183.131.22.111/v1/ad/delete'
        resp = requests.post(url, data=boby, headers=header)
        resp.close()
        if resp.status_code != 200:
            logging.error('delete_ad_fail')
            logging.info('delete_ad_code:' + str(resp.status_code))
            logging.info(resp.content)
            sys.exit(1)
        else:
            result = resp.json()
            result2 = json.dumps(result, ensure_ascii=False)
            print result2
            code = result['code']
            if code != 0:
                logging.error('delete_ad_codefail')
                logging.info('delete_ad_code:' + result2.encode('utf-8'))
                sys.exit(2)
            else:
                 pass
    except Exception as e:
        logging.error(Exception, 'delete_ad_Exception', e)
        sys.exit(3)
if __name__ == '__main__':
    delete_ad(6271)