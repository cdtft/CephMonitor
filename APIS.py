# coding=utf-8
from flask import Flask, request, jsonify
import CephRBD
import Model
import json


app = Flask(__name__)


# 查询 image
@app.route('/api/v1/ceph/rbd/<poolName>/image/<imageName>', methods=['GET'])
def getImageUsageSizeByImageName(poolName, imageName):
    storage = CephRBD.getUsedSize(poolName, imageName)
    data = Model.ImageInfo(poolName, imageName, storage.size/1024**3,
                           storage.used/1024**2)
    return Model.buildSuccessResponse("查询成功", data.__dict__)

# 批量查询 image
@app.route('/api/v1/ceph/rbd/<poolName>/images', methods=['GET'])
def getImageUsageSizeListByImageNameList(poolName):
    imageNames = json.loads(request.get_data())
    return Model.buildSuccessResponse("OK", CephRBD.getUsedSizeList(poolName, imageNames))

# 创建 image
@app.route('/api/v1/ceph/rbd/<poolName>/image', methods=['POST'])
def createImage(poolName):
    images = json.loads(request.get_data())
    CephRBD.createImage(poolName, images)
    return Model.buildSuccessResponse("OK", None)

# 删除 image
@app.route('/api/v1/ceph/rbd/<poolName>/image', methods=['DELETE'])
def deleteImage(poolName):
    deleteImageNames = json.loads(request.get_data())
    CephRBD.deleteImage(poolName, deleteImageNames)
    return Model.buildSuccessResponse("删除成功", None)

# 更新 image
@app.route('/api/v1/ceph/rbd/<poolName>/image', methods=['PUT'])
def updateImageSize(poolName):
    imageSizeList = json.loads(request.get_data())
    CephRBD.resizeImage(poolName, imageSizeList)
    return Model.buildSuccessResponse("resize success!", None)


if __name__ == '__main__':
    app.debug = True
    app.run(
        host='0.0.0.0',
        port='10086'
    )
