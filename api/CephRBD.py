# coding=utf-8

import rados
import rbd

cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
cluster.connect()

# copy from https://blog.csdn.net/xushuai110/article/details/53470998
# 统计ceph中rbd image的真实使用大小MB


def getUsedSize(pool_name, image_name):
    # 内部变量调用外部变量，必须使用一个class
    class ImageStorage:
        pass

    storage = ImageStorage()
    storage.used = 0

    def iterate_cb(offset, length, exists):
        storage.used += length

    with cluster.open_ioctx(pool_name) as ioctx:
        with rbd.Image(ioctx, image_name) as image:
            print 'image size: ', image.size()
            image.diff_iterate(0, image.size(), None, iterate_cb)

    return storage.used/1024**2
