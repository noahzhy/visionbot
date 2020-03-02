from collections import deque
import multiprocessing as mp
import _thread as thr
import numpy as np
import os, time
import cv2

import prediction as pre
import get_video as video
import upload_video as upload
import get_mac as mac
import get_mark as gm
from tkinter import Message, Tk
import tkinter


FLAG_FALL = False
VIDEO_GETTING = False
FLAG_RUNNING_STATUS = False

camera_ip_l = []
sec_timer = 30

def image_put(q, ip, channel=1):
    cap_ip = "rtsp://{}:554/user=admin&password=muan&channel=1&stream=0.sdp?".format(ip)
    cap = cv2.VideoCapture(cap_ip)
    cap.set(cv2.CAP_PROP_FPS, 5)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    while True:
        q.put(cap.read()[1])
        q.get() if q.qsize() > 1 else time.sleep(0.01)


def do_analysis(frame):
    # global FLAG_RUNNING_STATUS
    data = deque(maxlen=50)
    frames = deque(maxlen=50)

    frameNum = 0
    x, y, w, h = 0, 0, 0, 0
    a, area, motion_speed, tempY = 0, 0, 0, 0
    fall_cancel = 0.4
    fall_count = 0

    # cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)

    def fall_or_not():
        global FLAG_FALL
        global VIDEO_GETTING
        if (frameNum % 5 == 0):
            if (x == 0) or (y == 0) or (x+w == 320):
                pass
            else:
                res = pre.prediction(data)
                if (res[0] == 0 and res[1] > 0.92):
                    FLAG_FALL = True
                    # print(window_name, 'fall: {}'.format(res[1]))
                    if not VIDEO_GETTING:
                        VIDEO_GETTING = True

                        try:
                            path_to_file = video.get_video(list(frames), 'output')
                            if upload.upload(path_to_file) == 200:
                                print('upload success!')
                            else:
                                print('upload error!')
                        except Exception as e:
                            print(e)
                            pass

                elif (res[0] == 2 and res[1] > fall_cancel):
                    FLAG_FALL = False
                    VIDEO_GETTING = False
                    # print(window_name, 'normal: {}'.format(res[1]))

    frames.append(frame)
    frameNum += 1

    tempframe = frame.copy()
    if (frameNum == 1):
        previousframe = cv2.cvtColor(tempframe, cv2.COLOR_BGR2GRAY)
    if (frameNum >= 2):
        currentframe = cv2.cvtColor(tempframe, cv2.COLOR_BGR2GRAY)
        currentframe = cv2.absdiff(currentframe, previousframe)
        currentframe = cv2.dilate(currentframe, None, iterations=3)
        currentframe = cv2.erode(currentframe, None, iterations=2)
        ret, threshold_frame = cv2.threshold(currentframe, 20, 255, cv2.THRESH_BINARY)
        _, cnts, hierarchy = cv2.findContours(threshold_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            if cv2.contourArea(c) < 1300 or cv2.contourArea(c) > 19200:
                continue

            (x, y, w, h) = cv2.boundingRect(c)  # update the rectangle
            hull = cv2.convexHull(c)
            area = cv2.contourArea(hull)

        if (w*h == 0):
            pass

        ys = y-tempY
        ys = ys if (ys < 16) else 1
        tempY = y
        motion_speed = area/500*ys
        motion_speed = 0 if (abs(motion_speed) >= 120) else motion_speed
        data.append([y-30, (w/h-0.5)*100, motion_speed])

        if len(data) >= 50:
            try:
                thr.start_new_thread(fall_or_not, ())
            except:
                print("Error: cannot start the thread")

    previousframe = cv2.cvtColor(tempframe, cv2.COLOR_BGR2GRAY)


def image_get(q, window_name):
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    while True:
        frame = q.get()
        frame = cv2.resize(frame, (320, 240))
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)
        # key
        do_analysis(frame)


def check_cameras():
    global camera_ip_l
    while True:
        try:
            camera_ip_l = mac.get_mac()
            if len(camera_ip_l) <= 0:
                upload.error_report()
                
                top = Tk()
                top.title('Device Status')
                Message(top, text='No camera!', padx=20, pady=20).pack()
                top.after(sec_timer*1000, top.destroy)

                top.mainloop()
                top.withdraw()

            else:
                upload.online_report()
                break

        except Exception as e:
            print(e)

    return camera_ip_l


def run_multi_camera():
    camera_ip_l = check_cameras()
    print(camera_ip_l)

    mp.set_start_method(method='spawn')  # init
    queues = [mp.Queue(maxsize=2) for _ in camera_ip_l]

    processes = []
    for queue, camera_ip in zip(queues, camera_ip_l):
        processes.append(mp.Process(target=image_put, args=(queue, camera_ip)))
        processes.append(mp.Process(target=image_get, args=(queue, camera_ip)))

    for process in processes:
        process.daemon = True
        process.start()
    for process in processes:
        process.join()


def run():
    run_multi_camera()


if __name__ == '__main__':
    run()