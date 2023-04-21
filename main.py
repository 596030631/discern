import argparse
import os

from yolo.engine.model import YOLO

import cv2


class DetectModel:

    def __init__(self, args):
        cfg = args.cfg  # 'models/v8/yolov8.yaml'
        weights = args.weights  # 'weights/yolov8n.pt'
        print(cfg)
        print(weights)
        self.model = YOLO(cfg).load(weights)  # build from YAML and transfer weights

    def predict(self, img):
        print(img)
        # file_path = 'D:\\PycharmProj\\ultralytics\\ultralytics\\assets\\bus.jpg'
        ret = self.model.predict(source=img)
        print(ret[0].boxes.data)
        dets = ret[0].boxes.data
        im = cv2.imread(img)
        conf = 0.3

        result = {}
        result['img'] = f'http://127.0.0.1:5000/download?file_name={os.path.basename(img)}'
        result['bbox'] = []

        for det in dets:
            print(det)
            det = det.numpy()
            if conf > det[4]:
                continue
            xmin, ymin, xmax, ymax = int(det[0]), int(det[1]), int(det[2]), int(det[3])
            print(type(xmin))
            print(xmin)
            result['bbox'].append({'xmin':xmin, 'ymin':ymin, 'xmax':xmax, 'ymax':ymax, 'id':int(det[5]), 'conf':float(det[4])})
            cv2.rectangle(im, (xmin, ymin), (xmax, ymax), (255, 0, 255), 1)
        cv2.imwrite(img, im)
        return result


def load_model(args):
    detect_model = DetectModel(args)
    return detect_model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', default='ultralytics/models/v8/yolov8.yaml', help='Input your onnx model.')
    parser.add_argument('--weights', default=str('ultralytics/weights/yolov8n.pt'), help='Path to input weights.')
    args = parser.parse_args()
    detect_model = DetectModel(args)
    detect_model.predict("dddddddddddd")
