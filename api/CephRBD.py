# coding=utf-8
from CephMonitor.__init__ import cluster
import rados
import rbd
import Model
c = cluster

# copy from https://blog.csdn.net/xushuai110/article/details/53470998
# 统计ceph中rbd image的真实使用大小MB


def getUsedSize(pool_name, image_name):
    c.connect
    storage = Model.ImageStorage(0, 0)

    def iterate_cb(offset, length, exists):
        storage.used += length

    with cluster.open_ioctx(pool_name) as ioctx:
        with rbd.Image(ioctx, image_name) as image:
            storage.size = image.size()
            image.diff_iterate(0, image.size(), None, iterate_cb)
    
    return storage
