# coding=utf-8
from flask import Flask, request, jsonify
import CephRBD
import Model
import json

app = Flask(__name__)


# 获取image的使用大小
# request param
# path param:
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

# 批量获取image使用率
# request param
# path param:
# poolName                          string
# request body:
# ["nameA", "nameB", "nameC"]
@app.route('/api/v1/ceph/rbd/<poolName>/usages', methods=['GET'])
def getImageUsageSizeListByImageNameList(poolName):
    requestBody = request.get_data()
    names = json.loads(requestBody)
    imageInfoList = list()
    for i in names:
        print i
        data = Model.ImageInfo(poolName, i, 10,
                               CephRBD.getUsedSize(poolName, i))
        imageInfoList.append(data.__dict__)
    return Model.buildSuccessResponse("OK", imageInfoList)


if __name__ == '__main__':
    app.debug = True
    app.run(
        host='0.0.0.0',
        port='10086'
    )
