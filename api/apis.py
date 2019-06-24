# coding=utf-8
from flask import Flask
from ceph import ceph_rbd

app = Flask(__name__)

# 获取image的使用大小
@app.route('/api/v1/ceph/rdb/<poolName>/<imageName>/usage', methods=['GET'])
def getImageUsageSizeByImageName(poolName, imageName):

    return ceph_rbd.getUsedSize(poolName, imageName)


if __name__ == '__main__':
    app.run()
