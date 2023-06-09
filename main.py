import argparse
import os

import cv2

from yolo.engine.model import YOLO


class DetectModel:

    def __init__(self, args):
        cfg = args.cfg  # 'models/v8/yolov8.yaml'
        weights = args.weights  # 'weights/yolov8n.pt'
        print(cfg)
        print(weights)
        self.model = YOLO(cfg).load(weights)  # build from YAML and transfer weights
        self.category = []
        self.labels = []

        with open('labels/categroy.txt', 'r', encoding='utf-8') as f:
            l = f.readlines()
            for i in l:
                self.category.append(i.split(',')[1].replace('\n', ''))
        print(self.category)

        with open('labels/labels.txt', 'r', encoding='utf-8') as f:
            l = f.readlines()
            for i in l:
                ls = i.split(',')
                self.labels.append(
                    {'id': int(ls[0]), 'en': ls[1], 'cn': ls[2], 'category_id': int(ls[3]),
                     'category': self.category[int(ls[3])]})

        print(self.labels)

    def predict(self, img, category):
        print(img)
        print(category)
        # file_path = 'D:\\PycharmProj\\ultralytics\\ultralytics\\assets\\bus.jpg'
        ret = self.model.predict(source=img)
        print(ret[0].boxes.data)
        dets = ret[0].boxes.data
        im = cv2.imread(img)
        conf = 0.3

        result = {}
        result['url'] = f'http://127.0.0.1:5000/download?file_name={os.path.basename(img)}'
        result['bbox'] = []

        for det in dets:
            print(det)
            det = det.numpy()
            if conf > det[4]:
                continue
            if not category:
                result['bbox'].append({'id': int(det[5]),
                                       'info': self.labels[int(det[5])], 'conf': float(det[4])})
                continue

            if self.labels[int(det[5])]['category'] == category:
                xmin, ymin, xmax, ymax = int(det[0]), int(det[1]), int(det[2]), int(det[3])
                print(type(xmin))
                print(xmin)
                result['bbox'].append({'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax, 'id': int(det[5]),
                                       'info': self.labels[int(det[5])], 'conf': float(det[4])})
                cv2.rectangle(im, (xmin, ymin), (xmax, ymax), (255, 0, 255), 1)
        cv2.imwrite(img, im)
        print(result)
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
