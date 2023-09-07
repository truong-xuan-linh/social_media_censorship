import torch
from urllib.request import urlopen
import os

def get_model():
    censor_model = torch.hub.load("./storage", 'custom', path="./storage/best.pt", source="local", verbose=False) 
    censor_model.conf = 0.25  # NMS confidence threshold
    censor_model.iou = 0.15  # NMS IoU threshold
    censor_model.agnostic = False  # NMS class-agnostic
    censor_model.multi_label = True 
    censor_model.max_det = 100000
    
    return censor_model