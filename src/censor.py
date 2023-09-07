from src.get_detector import get_model

import cv2
import requests
import numpy as np
from PIL import Image
from src.setup import Setup

class Censor():
    def __init__(self) -> None:
        Setup().model_downloader()
        self.model = get_model()
        self.classes = self.model.names
    
    def detect(self, image_path, is_local=False):
        if not is_local:
            image = Image.open(requests.get(image_path, stream=True).raw).convert("RGB")
        else:
            image = Image.open(image_path).convert("RGB")
        results = self.model(image)
        texts = []
        boxes = []
        for result in results.xyxy[0]:
            result = map(float, result)
            x1, y1, x2, y2, score, class_idx = result
            text = f"{self.classes[int(class_idx)]} {score:0.2f}"
            boxes.append([x1, y1, x2, y2])
            texts.append(text)
        return np.array(image), texts, boxes
    
    def visualize(self, image, texts, boxes):
        image = np.array(image)
        img = image.copy()
        for box, text in zip(boxes, texts):
            x1, y1, x2, y2 = box
            h = y2 - y1
            img = cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            img = cv2.putText(img, text, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, h/500, (255,0,0), 1)
        return img