# coding=utf-8

import rados
import rbd
import Model

cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
cluster.connect()


# copy from https://blog.csdn.net/xushuai110/article/details/53470998 统计ceph中rbd image的真实使用大小MB
def getUsedSize(pool_name, image_name):
    storage = Model.ImageStorage(0, 0)

    def iterate_cb(offset, length, exists):
        storage.used += length

    with cluster.open_ioctx(pool_name) as ioctx:
        with rbd.Image(ioctx, image_name) as image:
            storage.size = image.size()
            image.diff_iterate(0, image.size(), None, iterate_cb)
    return storage


def getUsedSizeList(poolName, imageNames):
    imageList = list()
    ioctx = cluster.open_ioctx(poolName)

    for imageName in imageNames:
        imageInfo = Model.ImageInfo(poolName, imageName, 0, 0)
        image = rbd.Image(ioctx, imageName)

        def iterate_cb(offset, length, exists):
            imageInfo.usage += length
        image.diff_iterate(0, image.size(), None, iterate_cb)
        image.close
        imageList.append(imageInfo.__dict__)
    ioctx.close()
    return imageList


def createImage(poolName, images):
    ctx = cluster.open_ioctx(poolName)
    for image in images:
        rbd.RBD().create(ctx, image['name'], image['size']*(1024**3))
    ctx.close()


def deleteImage(poolName, imageNames):
    ctx = cluster.open_ioctx(poolName)
    for imageName in imageNames:
        rbd.RBD().remove(ctx, imageName)
    ctx.close()


def resizeImage(poolName, image):
    ctx = cluster.open_ioctx(poolName)
    rbdImage = rbd.Image(ctx, image['name'])
    rbdImage.resize(image['size']*(1024**3))
    rbdImage.close()
    ctx.close()

