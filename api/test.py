import caffe
import numpy as np
from PIL import Image

# ng images
# im_path='rust1.jpg'
# im_path = 'pic_vol02_14.jpg'
# ok images
im_path='not_rust.jpg'

im = Image.open(im_path)
img = np.asarray(im).astype(np.float32) / 255.
if img.ndim == 2:
    img = img[:, :, np.newaxis]
    img = np.tile(img, (1, 1, 3))
elif img.shape[2] == 4:
    img = img[:, :, :3]

net = caffe.Classifier('deploy.prototxt', 'tank_net_iter_98000.caffemodel', image_dims=(227, 227), raw_scale=255., mean=np.load('mean_train.npy'), channel_swap=(2, 1, 0), gpu=False)
score = net.predict([img], oversample=True)
print score
score1 = net.predict([img], oversample=True).flatten()
print score1
