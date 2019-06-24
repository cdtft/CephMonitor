from flask import Flask
from ceph import ceph_rbd

app = Flask(__name__)


@app.route('/api/v1/ceph/rdb/image/size', methods=['GET'])
def getImageUsageSizeByImageName():
    print "hello"
    return ceph_rbd.get_image_size("k8s", "45.5")


if __name__ == '__main__':
    app.run()
