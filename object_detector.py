# object_detector.py

import torch

class ObjectDetector:
    def __init__(self, model_path='yolov5s.pt'):
        self.model = torch.hub.load('yolov5', 'custom', path=model_path, source='local')
        self.model.conf = 0.4  # 設定置信門檻值

    def detect(self, frame):
        results = self.model(frame)
        return results
