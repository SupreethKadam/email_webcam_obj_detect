import cv2
import glob
from emailing import send_email
from clean_folder import clean_folder
from time_stamp import time_stamp
from threading import Thread

# Capturing the video using web-camera.
# Pass the argument 0 if using main camera(integrated camera) or 1 - for external or USB camera.
video = cv2.VideoCapture(0)

first_frame = None
status_list = []
count = 1


while True:
    status = 0
    check, frame = video.read()
    # convert the color frame to grayscale.
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # blur the grayscale frame image. GaussianBlur is an algo which takes
    # frame, amount to gray, and std deviation as argument
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

# capturing the first frame and assigning it to a variable
    if first_frame is None:
        first_frame = gray_frame_gau

# check the difference between first frame and current frame. save it in a variable
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

# applying a threshold value: 60, whichever has the value 60 will be replaced by 255
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
# to remove the noise
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            captured_img = time_stamp(frame)
            # capturing the image frame
            cv2.imwrite(f"images/{count}.png", captured_img)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            img_with_obj = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(img_with_obj, ))
        email_thread.daemon = True
        email_thread.start()

    print(status_list)

    cv2.imshow("My video", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True
        clean_thread.start()
        break

video.release()
