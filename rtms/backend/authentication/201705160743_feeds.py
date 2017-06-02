# -*- coding:utf-8 -*-
#
# 一个简单的HTTP请求脚本示例
#
from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from net.grinder.plugin.http import HTTPRequest
from net.grinder.plugin.http import TimeoutException
from net.grinder.plugin.http import HTTPPluginControl
from HTTPClient import NVPair
# 导入对JSON格式返回值的处理函数
from org.json import JSONObject
import random
from org.json import JSONArray

control = HTTPPluginControl.getConnectionDefaults()
# 请求重定向开关
control.followRedirects = 1
# 超时时间设置
control.timeout = 6000

test1 = Test(1, "Test1")
request1 = HTTPRequest()

# Make any method call on request1 increase TPS
test1.record(request1)


class TestRunner:
    # 初始化，仅执行一次
    def __init__(self):
        grinder.statistics.delayReports = True
        pass

    # 类似LR的action，压测时会多次执行
    # test method
    def __call__(self):

        # url地址
        url = 'http://183.131.22.111/feeds/com.oppo.os.ads.show.feed.service.IFeedListRankSvc'
        # headers信息
        headers = [NVPair("Content-Type", "application/json"),
                   NVPair("Accept-Encoding", "gzip")
                   ]
        # JSON格式的请求内容
        imei = "86" + str(random.randint(1000000000000, 99999999999999))
        submitdata = '{"methodName": "listFeedRank", "arguments": [{"parModuleId": "100", "posIds": "1", "networkId": "7", "openId": "sadlkalksjdasjd", "appVersion": "3.0.1", "clientTime": "", "contextTag": "[a,b,c],[e,f,g]", "location": "武汉", "pageStart": "0", "androidVersion": "4.4.4", "channel": "2", "category": "0", "dataType": "feed_show", "eventValue": "0", "imei": %s, "osVersion": "V2.1.0", "model": "X907", "moduleId": "8000", "sdkVersion": "", "ssoid": "11022", "romVersion": "000", "sessionId": "", "seqId": "", "systemId": "9", "clientIp": "222.248.000.000","carrier": "1","isDown": true,"down": 2,"up": 0}]}' % imei
        # URL请求
        try:
            result = request1.POST(url, submitdata, headers)
            retcode = result.getStatusCode()
            flag = False
            if retcode == 200:
                message = result.getText()
                json = JSONObject(message)
                if json.has("data") == True:
                    data = json.getJSONObject("data");
                    adlist = data.getJSONArray("adList");
                    for i in range(0, adlist.length()):
                        adId = adlist.getJSONObject(i)
                        value = adId.get("adId")
                        if value==336:
                                      flag = True
                        else:
                                      flag = False
                                      grinder.logger.info('imei1=' + imei)
                                      grinder.logger.info("result1=" + result.getText())
                else:
                    flag = False
                    grinder.logger.info('imei2=' + imei)
                    grinder.logger.info("result2=" + result.getText())
            else:
                flag = False
                grinder.logger.info("statusCode3=" + str(retcode))
                grinder.logger.info('imei3=' + imei)
                grinder.logger.info("result3=" + result.getText())

            # 打印输出URL请求返回内容
            # 返回结果检查，有返回特定字符，则判断请求成功
            if flag == True:
                grinder.statistics.forLastTest.success = 1

            else:
                grinder.statistics.forLastTest.success = 0

        except TimeoutException, e:
            grinder.statistics.forLastTest.success = 0
            grinder.logger.info("TimeoutException=" + str(e))
