# -*-coding=utf-8
import requests
import logging
import log
#log.initLogging('../../log/feeds_auto')
log.initLogging('/data/rx/log')
def get_manager_cookies():
    try:
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Cookie': 'org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=zh_CN; JSESSIONID=5D6A43FC46C868BF3F1FE68320254E49'
        }
        boby = {
            'username': '80122499',
            'password': '123',
            'vcode': '123',
            'submit': '登录',
            'lt': 'LT-4605-3dWZdvd1hNkyKmcsn90SSTqvb3okEH-cas01.example.org',
            'execution': '54513270-1c7a-471c-ae61-53397383c5ab_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',
            '_eventId': 'submit'
        }
        url = 'https://test.sso.basic.oppoer.me/login?service=http%3A%2F%2Fappex.oppo.cn%2F&locale=zh_CN'
        resp = requests.post(url, data=boby, headers=header, verify=False, allow_redirects=True)
        if resp.status_code!=200:
            logging.debug('manage_cookies_fail')
        else:
            redirects_resp = resp.history[1]
            cookie = redirects_resp.cookies.values()[0]
            return cookie
    except Exception as e:
        print Exception, 'delete_contracrAd_Exception', e





