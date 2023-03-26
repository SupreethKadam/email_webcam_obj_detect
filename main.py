import cv2

# Capturing the video using web-camera.
# Pass the argument 0 if using main camera(integrated camera) or 1 - for external or USB camera.
video = cv2.VideoCapture(0)

first_frame = None

while True:
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
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    cv2.imshow("My video", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
