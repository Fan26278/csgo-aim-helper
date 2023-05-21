import time

from screen_inf import grab_screen_win32
import cv2
import win32gui
import win32con
from cs_model import load_modele
import torch
from utils.general import  non_max_suppression,scale_boxes,xyxy2xywh
from utils.augmentations import letterbox
import numpy as np
from mouse_controller import lock,shot
import pynput
import winsound
import os
import sys
from pynput.keyboard import Key,Listener



lock_mode = True

shot_enable = False



Police = False


# 模型路径
weights = r"D:\Games\yolov5\csgo-aim\models\csgo_v1.pt"


shot_times = 4

mouse = pynput.mouse.Controller()
def on_move(x, y):
    pass
def on_scroll(x, y, dx, dy):
    pass


def on_click(x, y, button, pressed):
    global lock_mode
    global Police
    if pressed and button == button.middle:
        lock_mode = not lock_mode
        print("lock mode" ,'on' if lock_mode else 'off')
        if lock_mode:
            winsound.Beep(50, 200)
            winsound.Beep(100, 200)
            winsound.Beep(200, 200)
        else:
            winsound.Beep(600,150)
    if pressed and button == button.x2:
        Police = not Police
        if Police:
            winsound.MessageBeep(1)
        else:
            winsound.Beep(50, 200)
            winsound.Beep(200, 200)

listener = pynput.mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
listener.start()
device = 'cuda'
x, y = (1920, 1440)
re_x , re_y = (1920,1440)
conf_thres = 0.4
iou_thres = 0.05
imgsz = 640


model = load_modele(weights)
stride = model.stride
names = model.names if hasattr(model,"module") else model.names
seen = 0



# 该循环： 新建一个窗口，实时在屏幕上方
while True:
    img0 = grab_screen_win32(region=(0, 0, x, y))
    img0 = cv2.resize(img0,(re_x,re_y))


    img = letterbox(img0,imgsz,stride=stride)[0]
    img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    img = np.ascontiguousarray(img)  # contiguous


    img = torch.from_numpy(img).to(model.device)
    img = img.half() if model.fp16 else img.float()
    img /= 255  # 0 - 255 to 0.0 - 1.0
    if len(img.shape) == 3:
        img = img[None]  # expand for batch dim
    pred = model(img, augment=False, visualize=False)[0]
    pred = non_max_suppression(pred, conf_thres,iou_thres, agnostic=False)


    aims = []
    for i ,det in enumerate(pred):
        seen += 1
        s = ''
        s += '%gx%g ' % img.shape[2:]  # print string
        gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]  # normalization gain whwh

        #annotator = Annotator(im0, line_width=line_thickness, example=str(names))

        if len(det):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()

            # Print results
            for c in det[:, 5].unique():
                n = (det[:, 5] == c).sum()  # detections per class
                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

            # Write results
            for *xyxy, conf, cls in reversed(det):
                xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                line = (cls, *xywh)  # label format
                aim= ('%g ' * len(line)).rstrip() % line
                aim = aim.split(' ')
                aims.append(aim)

        if len(aims):
            if lock_mode:
                lock(aims,mouse,x,y,Police)
                print("lock mode", "on" if lock_mode else "off")
            for i , det in enumerate(aims):
                _,x_center,y_center,width,height = det
                x_center, width = re_x * float(x_center),re_x *float(width)
                y_center,height = re_y * float(y_center),re_y * float(height)
                top_left = (int(x_center-width / 2.) , int(y_center - height / 2.))
                bottom_right = (int(x_center + width / 2.) , int(y_center + height / 2.))
                color = (0,255,0) # RGB
                cv2.rectangle(img0,top_left,bottom_right,color,4)


    cv2.namedWindow("csgo-detect", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('csgo-detect',re_x // 2,re_y // 2)
    # cv2.imshow('csgo-detect',img0)

    hwnd = win32gui.FindWindow(None,'csgo-detect')
    CVRECT = cv2.getWindowImageRect('csgo-detect')
    win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,0,0,win32con.SWP_NOMOVE|win32con.SWP_NOSIZE)

    # 按q键break窗口
    if cv2.waitKey(1) &  0xff == ord('q'):
        cv2.destroyAllWindows()
        break