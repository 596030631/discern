import argparse

import cv2


class DetectModel:

    def __init__(self, args):
        from yolo.engine.model import YOLO
        cfg = args.cfg  # 'models/v8/yolov8.yaml'
        weights = args.weights  # 'weights/yolov8n.pt'
        print(cfg)
        print(weights)
        self.model = YOLO(cfg).load(weights)  # build from YAML and transfer weights

    def predict(self, img):
        print(img)
        file_path = 'D:\\PycharmProj\\ultralytics\\ultralytics\\assets\\bus.jpg'
        ret = self.model.predict(source=file_path)
        print(ret[0].boxes.data)
        dets = ret[0].boxes.data
        im = cv2.imread(file_path)
        conf = 0.3
        for det in dets:
            print(det)
            det = det.numpy()
            if conf > det[4]:
                continue
            xmin, ymin, xmax, ymax = int(det[0]), int(det[1]), int(det[2]), int(det[3])
            print(type(xmin))
            print(xmin)
            cv2.rectangle(im, (xmin, ymin), (xmax, ymax), (255, 0, 255), 1)
        while True:
            cv2.imshow('im', im)
            cv2.waitKey(300)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', default='models/v8/yolov8.yaml', help='Input your onnx model.')
    parser.add_argument('--weights', default=str('weights/yolov8n.pt'), help='Path to input weights.')
    args = parser.parse_args()
    detect_model = DetectModel(args)
    detect_model.predict("dddddddddddd")
