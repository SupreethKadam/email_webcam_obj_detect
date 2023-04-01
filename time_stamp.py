import cv2
import datetime


def time_stamp(obj_img):
    date_time_now = datetime.datetime.now()
    day = date_time_now.strftime("%A")
    current_time = date_time_now.strftime("%H:%M:%S")
    cv2.putText(img=obj_img, text=f"{day}", org=(30, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
    cv2.putText(img=obj_img, text=f"{current_time}", org=(30, 60), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5, color=(255, 255, 0), thickness=1, lineType=cv2.LINE_AA)
    return obj_img
