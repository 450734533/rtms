# -*-coding=utf-8
import urllib2
import cookielib
import urllib
from PIL import Image
from pytesser import pytesser
def get_webtoken():
    CaptchaUrl = "http://e.oppo.cn/loginCaptcha"
    LoginUrl = "http://e.oppo.cn/login"
    # 验证码地址和post地址
    while True:
        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        # urllib2.install_opener(opener)
        # 将cookies绑定到一个opener cookie由cookielib自动管理
        while True:
            picture = opener.open(CaptchaUrl)  # 用openr访问验证码地址,获取cookie
            local = open('/data/rx/image/image.jpg', 'wb')
            local.write(picture.read())
            local.close()
            im = Image.open('/data/rx/image/image.jpg')
            text = pytesser.image_to_string(im).strip()
         #   text = pytesser.image_file_to_string(im,graceful_errors=True).strip()
            flag = len(text)
         #   print 'authCode=%s,lens=%s' % (text, flag)
         #   print len(text)
            if flag == 4:
                break
        boby = {
            'name': '扣费',
            'passwd': '123456',
            'captcha': text
        }
        data = urllib.urlencode(boby)
        request = urllib2.Request(url=LoginUrl, data=data)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        opener.open(request)  #response
        cookies = cookie.__str__().split(' ')[1]
      #  print 'cookies=%s' % cookies
        if cookies.find('WEBTOKEN') == 0:
            break
    return cookies
            # fout1 = open("tt1.html", "w")
            # fout1.write(response.read())
if __name__=='__main__':
    a = get_webtoken()
    print a









