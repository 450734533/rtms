# -*- coding:utf-8 -*-
from kazoo.client import KazooClient


class ZkClient(object):
    def __init__(self, host, port, timeout):
        try:
            zk = KazooClient(hosts=host+':'+port, timeout=timeout)
            zk.start()  # 启动zk连接
            self.zk = zk
        except Exception as e:
            raise ValueError("connect zk failed -- host:%s, port:%s, error:%s" % (host, port, str(e)))

    def get_nodes(self, path):
        """获取path下的节点"""
        if self.zk.exists(path):
            try:
                result = self.zk.get_children(path)
                return result
            except Exception as e:
                self.close_conn()
                raise ValueError("get_nodes falied: path -- '%s' , error -- %s" % (path, str(e)))
        else:
            raise ValueError("node path - '%s' not exist." % path)

    def get_nodes_content(self, path):
        """获取path节点下的值"""
        if self.zk.exists(path):
            try:
                result = self.zk.get(path)
                return result
            except Exception as e:
                self.close_conn()
                raise ValueError("get_nodes_content falied: path -- '%s' , error -- %s" % (path, str(e)))
        else:
            raise ValueError("node path - '%s' not exist." % path)

    def set_nodes(self, path, value=b''):
        """设置节点值，如果节点不存在则新建该节点"""
        if self.zk.exists(path):
            try:
                result = self.zk.set(path, str(value))
                print "set node success -- node path:'%s', value:%s" % (str(path), str(value))
            except Exception as e:
                self.close_conn()
                raise ValueError("set_nodes falied: path -- '%s' , error -- %s" % (path, str(e)))
        else:
            print "node '%s' is not exist, now it will create." % path
            try:
                create_zk = self.zk.create(path, str(value))
                print "create node success -- path:'%s', value:%s" % (str(path), str(value))
                result = self.zk.set(path, str(value))
                print "set node success -- node path:'%s', value:%s" % (str(path), str(value))
            except Exception as e:
                self.close_conn()
                raise ValueError("set_nodes falied: path -- '%s' , error -- %s" % (path, str(e)))
        return result

    def delete_node(self, path):
        if self.zk.exists(path):
            try:
                del_r = self.zk.delete(path)
                print "delete node success -- node path:'%s'" % str(path)
            except Exception as e:
                self.close_conn()
                raise ValueError("delete_node falied: path -- '%s' , error -- %s" % (path, str(e)))
        else:
            raise ValueError("node path - '%s' not exist." % path)

    def close_conn(self):
        self.zk.stop()


def test_zk(cmd,path,value, host='172.30.248.231', port='2181', timeout=10.0):
    zk_cli = ZkClient(host, port, timeout)
    if cmd == 'ls':
        result = zk_cli.get_nodes(path)
    elif cmd == 'get':
        result = zk_cli.get_nodes_content(path)
    elif cmd == 'set':
        result = zk_cli.set_nodes(path, value=value)
    elif cmd == 'delete':
        result = zk_cli.delete_node(path)
    else:
        zk_cli.close_conn()
        raise ValueError("command error, cmd must in [ls, get, set, delete]")
    zk_cli.close_conn()
    return result

if __name__ == '__main__':
    result = test_zk('set','/BIZ/CONFIG/feeds/show_user_data_cache_expire_seconds','10001')
    print result
