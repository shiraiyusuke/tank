import caffe
import numpy as np

class ImagenetClassifier():
    def __init__(self, model_def, model, mean_file, raw_scale, image_dim, gpu_mode, logger):
        self.logger = logger

        self.net = caffe.Classifier(
            model_def, model, image_dims=(image_dim, image_dim), raw_scale=raw_scale,
            mean=np.load(mean_file), channel_swap=(2, 1, 0), gpu=gpu_mode
        )

    def classify_image(self, image):
        w = image.shape[0]
        h = image.shape[1]
        
        scores = self.net.predict([image], oversample=True).flatten()


        indices = (-scores).argsort()
        predictions = scores[indices]
        pred = float('%.05f' % predictions[0])
        if not pred >= 0:
            pred = float('%05f' % 0)

        if scores[0] >= scores[1]:
            return (0, pred)
        else:
            return (1, pred)

