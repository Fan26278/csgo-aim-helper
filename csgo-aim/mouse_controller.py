import winsound

import pynput
from pynput.mouse import Button
import time


def lock(aims,mouse,x,y,Police):
    mouse = pynput.mouse.Controller()
    mouse_pos_x, mouse_pos_y = mouse.position
    dist_list = []

    for det in aims:
        _,x_c,y_c,_,_ = det
        dist = (x * float(x_c) - mouse_pos_x )**2  + (y * float(y_c) - mouse_pos_y) **2
        dist_list.append(dist)

    #det = dist_list[1] if dist_list[0]>dist_list[1] else dist_list[0]
    det = aims[dist_list.index(min(dist_list))]

    tag, x_center,y_center,width,height = det
    tag = int(tag)
    x_center , width = x * float(x_center), x * float(width)
    y_center,height = y * float(y_center), y * float(height)
    """
    0:CT_HEAD
    1:CT_BODY
    2:T_HEAD
    3:T_BODY
    """
    # 如果是警察瞄准匪的头和身子
    # if Police:
    #     if tag == 2:  # 瞄准匪的头
    #         mouse.position = (x_center, y_center)
    #     if tag == 3 :  # 瞄准匪的身子
    #         mouse.position = (x_center, y_center - 1 / 6 * height)
    # elif  not Police:
    #     if tag == 0:  # 瞄准警的头
    #         mouse.position = (x_center, y_center)
    #     if tag == 1 :  # 瞄警的身子
    #         mouse.position = (x_center, y_center - 1 / 6 * height)
    # else:
    #     pass
    if tag == 0 or tag ==2:
        #mouse.position = (x_center,y_center - 3  + 1/2 * height  )
        mouse.position = (x_center, y_center + 1 / 2 * height)

    elif tag == 1 or tag ==3:   # -1/3
        #mouse.position = (x_center,y_center -3 -  1/4 * height)
        mouse.position = (x_center, y_center - 1 / 6 * height)

def shot(mouse,flag,times):
    if flag:
        #mouse.click(Button.left,times)
        mouse.press(Button.left)
        time.sleep(0.3)
        mouse.release(Button.left)
        time.sleep(0.2)
    else:
        pass
