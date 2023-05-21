import torch
from models.experimental import attempt_load
from utils.torch_utils import select_device, smart_inference_mode
from models.common import DetectMultiBackend

data = 'data/coco128.yaml'


device = 'cuda' if torch.cuda.is_available() else 'cpu'
half = device != 'cpu'
imgsz = 640



def load_modele(weights):
    device = select_device("")
    model = DetectMultiBackend(weights, device=device, dnn=False, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    return model
