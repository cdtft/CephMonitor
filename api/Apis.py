# coding=utf-8
from flask import Flask, jsonify
import CephRBD
import Model

app = Flask(__name__)


# 获取image的使用大小
# request param:
# poolName                          string
# imageName                         string
#
# response json data:
# {
#     "poolName": "k8s",            string
#     "imageName": "45.45",         string
#     "size": "10GB",               string
#     "usage": "326MB"              string
# }
@app.route('/api/v1/ceph/rbd/<poolName>/<imageName>/usage', methods=['GET'])
def getImageUsageSizeByImageName(poolName, imageName):
    data = Model.ImageInfo(poolName, imageName, 10,
                           CephRBD.getUsedSize(poolName, imageName))
    return Model.buildSuccessResponse("查询成功", data.__dict__)


@app.route('/api/v1/ceph/rbd/', methods=['GET'])
def getImageUsageSizeListByImageNameList():

    pass


if __name__ == '__main__':
    app.debug = True
    app.run(
        host='0.0.0.0',
        port='10086'
    )
