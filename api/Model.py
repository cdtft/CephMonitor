# coding=utf-8
from flask import jsonify


class ImageInfo:
    def __init__(self, poolName, imageName, size, usage):
        self.poolName = poolName
        self.imageName = imageName
        self.size = size
        self.usage = usage

    @property
    def getPoolName(self):
        return self.poolName


class ImageStorage:
    def __init__(self, used, size):
        self.used = used
        self.size = size


# 统一返回json结构
def buildResponse(code, message, data):
    return jsonify({'code': code, 'message': message, 'data': data})


def buildSuccessResponse(message, data):
    return jsonify({'code': 200, 'message': message, 'data': data})


def buildErrorResponse(message, data):
    return jsonify({'code': 200, 'message': message, 'data': data})
