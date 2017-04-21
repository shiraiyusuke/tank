import flask
from log import get_logger, logging_args
import argparse
from tank_rust_caffe import ImagenetClassifier
from api_util import start_from_terminal
import time
from PIL import Image
import numpy as np
import cStringIO as StringIO
import json
from flask import render_template

app = flask.Flask(__name__)

WK_DIR = '/data3/work/shirai/bike/diagnosis/tank_rust/'
MODEL_DEF = WK_DIR + 'model/deploy.prototxt'
MODEL = WK_DIR + 'model/tank_net_iter_98000.caffemodel'
MEAN_FILE = WK_DIR + 'model/mean_train.npy'
IMAGE_DIM = 227
RAW_SCALE = 255.
GPU_MODE = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tank_rust_recognition', methods=['POST'])
def tank_rust_recognition():
    start_time = time.time()
    
    image_file = flask.request.files['imagefile']
    string_buffer = StringIO.StringIO(image_file.read())
    image = Image.open(string_buffer)
    img = np.asarray(image).astype(np.float32) / 255.
    if img.ndim == 2:
        img = img[:, :, np.newaxis]
        img = np.tile(img, (1, 1, 3))
    elif img.shape[2] == 4:
        img = img[:, :, :3]
    image = img
    result_tuple = app.clf.classify_image(image)
    result_dict = {}
    if result_tuple[0] == 0:
        result_dict = {"result": "not rust", "prediction": result_tuple[1]}
    else:
        result_dict = {"result": "rust", "prediction": result_tuple[1]}
    result_json = json.dumps(result_dict)
    return result_json

def parse_args():
    parser = argparse.ArgumentParser(description=u'car type API')
    parser.add_argument(
        '-d', '--debug',
        action='store_true', default=False, help=u'debug mode')
    parser.add_argument(
        '--port',
        type=int, dest='port', default=6001, help=u'port number')
    parser.add_argument(
        '--proc',
        type=int, dest='proc', default=1, help=u'process number')
    parser.add_argument(
        '--log-file',
        type=str, dest='log_file', default='/data/image_processing/car_type/app/log/analysis_result.log', help=u'log file')
    parser.add_argument(
        '--log-level',
        type=str, dest='log_level', default='info', help=u'log level')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    logger = get_logger(__name__, args.log_level, args.log_file, args.log_level)
    logging_args(logger, args)
    app.clf = ImagenetClassifier(MODEL_DEF, MODEL, MEAN_FILE, RAW_SCALE, IMAGE_DIM, GPU_MODE, logger)
    start_from_terminal(app, args.port, args.proc, args.debug)
