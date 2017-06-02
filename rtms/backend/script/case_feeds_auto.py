# -*-coding=utf-8
import unittest
import time
from schedule import *
from ad.create_ad_feeds import *
from ad.create_yidian_ad_feeds import *
from ad.delete_ad import *
from ad.delete_yidian_ad import *


class feeds_auto(unittest.TestCase):
    def test_0(self):
        id = add_schedule()
        adId = create_contractAd(id)
        submit_order()
        audit_contractAd(adId)
        audit_order()
        set_zk(0)
        set_zk(1)
        time.sleep(300)
        feeds_req(adId)
        delete_contracrAd(adId)
        mysql_delete_schedule()
        mysql_delete_contractAd()
        adId=create_ad_feeds()
        yidian_adId=create_yidian_ad_feeds()
        audit_feedAd(adId)
        audit_feedAd(yidian_adId)
        delete_ad(adId)
        delete_yidian_ad(yidian_adId)

if __name__ == '__main__':
    unittest.main()









