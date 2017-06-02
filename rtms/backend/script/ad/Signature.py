#/usr/bin/env python
# -*- coding:utf-8 -*-
import time
#from hashlib import md5
import hashlib
import base64
'''
 :Description:    鉴权加密
 :author          80155463
 :@version         V1.0
 :@Date            2016年7月7日
'''


class Signature(object):
    '''
     * md5加盐
     * 生成token
    '''
    #def __init__(self,signKey,reqBytes,times):
    def __init__(self,*args):
        '''
        #* @param
        非一点资讯所需参数
        args[0] = signKey 加密字符串
        args[1] = reqBytes 加盐字符串
        args[2] = times 当前时间戳
        一点资讯所需参数
        args[0] = agency 用户帐号id，通常与app_id一致
        args[1] = apiId API授权接入方唯一身份标识，目前为申请API接入的帐号id
        args[2] = apiKey 开通API授权后获得的私钥，在开通授权邮件中会与app_id一块提供
        args[3] = timestamp 当前时间戳
        '''

        if len(args) == 3:
            self.signKey = args[0] #signKey
            self.reqBytes = args[1] #reqBytes
            self.times = args[2]  #str(time.time() * 1000)
              #str(times)
        elif len(args) == 4:
            self.agency = args[0]
            self.apiId = args[1]
            self.apiKey = args[2]
            #self.timestamp = str(int(time.time()))
            self.timestamp = args[3]
        else:
            raise ValueError('args Error,please follow as show below:\n'+''''
        非一点资讯所需参数
        args[0] = signKey 加密字符串
        args[1] = reqBytes 加盐字符串   json转python的数据 type=str
        args[2] = times 当前时间戳
        一点资讯所需参数
        args[0] = agency 用户帐号id，通常与app_id一致
        args[1] = apiId API授权接入方唯一身份标识，目前为申请API接入的帐号id
        args[2] = apiKey 开通API授权后获得的私钥，在开通授权邮件中会与app_id一块提供
        args[3] = timestamp 当前时间戳
        ''')

    def create_sign_md5(self):
        '''
        * @ return md5
       '''
        #所有加密字符串转换成2进制  为什么需要转化成2进制

        signKey_byte = bytearray(self.signKey)    #type=bytearray
        reqBytes_byte = bytearray(self.reqBytes)
        times_byte = bytearray(self.times)



        signData = reqBytes_byte + times_byte

        md5_obj = hashlib.md5()  #用hashlib里的md5()生成一个md5 hash对象
        md5_obj.update(signData + signKey_byte)  #生成hash对象后，就可以用update方法对字符串进行md5加密的更新处理
        sign_md5 = md5_obj.hexdigest()     #type=str
        return  sign_md5


    #如果只需对一条字符串进行加密处理，也可以用一条语句的方式：   md5经常用来做用户密码的存储。而sha1则经常用作数字签名
    # hashlib.new("md5", "Nobody inspects the spammish repetition").hexdigest()

    def create_token_base64(self):
        '''
        :return: base64 token
        '''
        #sign = sha1(api_id + api_key + time_stamp)，采用sha1加密算法生成签名串
        signStr = self.apiId + self.apiKey + self.timestamp
        sign = hashlib.sha1(signStr).hexdigest()
        #base64(agent_id + “, ” + api_id + “, ” + time_stamp + “, ” + sign)
        #所有内容使用半角逗号（, ）按顺序拼接起来，再经过Base64编码
        tokenStr = self.agency + "," + self.apiId + "," + self.timestamp + "," + sign
        token = base64.b64encode(tokenStr)   #字符串转2进制
        return token

    def decode_base64(self,token):
        '''
        :param token:
        :return: decode token
        '''
        try:
            decodetoken = base64.b64decode(token)
            return decodetoken
        except Exception as e:
            print 'decode base64 exception:%s' % str(e)
            return False


if __name__ == "__main__":

    signKey = 'e0u6fnlag06lc3pl'
    reqBytes = 'abcdef'
    # times = time.time()*1000
    times = '1465030224694'
    signature = Signature(signKey,reqBytes)
    sign_md5 = signature.create_sign_md5()
    print  sign_md5

