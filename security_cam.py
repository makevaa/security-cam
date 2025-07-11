import cv2
from PIL import ImageFont, ImageDraw
import time
import datetime
import numpy as np



def main():

    cam = cv2.VideoCapture(0)
    window_name = 'CITADEL SECURITY'
    cv2.namedWindow(window_name)

    img_counter = 0
    
    # Font stuff for overlay
    font = cv2.FONT_HERSHEY_SIMPLEX
    monospace = ImageFont.truetype("files/font/SourceCodePro-Regular.ttf",32)
    #font = monospace
    org = (50, 50) #text position
    fontScale = 0.8
    color = (0, 255, 0)
    thickness = 2


    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        

        # image, width = None, height = None, inter = cv2.INTER_AREA):
        frame = image_resize(frame, width=700)
        #frame = cv2.resize(frame, width=None, height=None, dst=None, fx=None, fy=None, interpolation=cv2.INTER_LINEAR)

        frame_h, frame_w, frame_channel = frame.shape

        logo_image = cv2.imread('files/logo.png')
        logo_image_w = 60
        logo_image = image_resize(logo_image, width=logo_image_w)
        logo_padding = 5
 

        logo_pos_x = frame_w - logo_image_w - logo_padding
        logo_pos_y = logo_padding
 
        # Put logo image on top-right of frame
        # replace values at coordinates (100, 100) to (399, 399) of img3 with region of img2
        frame[logo_pos_y:logo_image_w+logo_padding, logo_pos_x:logo_pos_x+logo_image_w, :] = logo_image[0:logo_image_w, 0:logo_image_w, :]

        alpha = 0.5
        #img3 = np.uint8(frame*alpha + logo_image*(1-alpha))

        #alpha = 0.5
        #img3 = np.uint8(img1*alpha + img2*(1-alpha))

        # Text overlays
        # Draw text border with higher thickness
        text_x = frame_w-425
        text_y = 30
        timestamp = get_timestamp()
       
        cv2.putText(frame, 'CITADEL SECURITY [CAM 1]', (text_x, text_y), font, fontScale, (0, 0, 0), thickness+5, cv2.LINE_AA) #border
        cv2.putText(frame, 'CITADEL SECURITY [CAM 1]', (text_x, text_y), font, fontScale, color, thickness, cv2.LINE_AA)
        cv2.putText(frame, timestamp, (text_x+45, text_y+30), font, fontScale, (0, 0, 0), thickness+5, cv2.LINE_AA) #border
        cv2.putText(frame, timestamp, (text_x+45, text_y+30), font, fontScale, color, thickness, cv2.LINE_AA)
        

        	
        

        cv2.imshow(window_name, frame)

        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "out/opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

        time.sleep(0.3)  

    cam.release()
    cv2.destroyAllWindows()



def get_timestamp():
    ts = time.time()
    stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return stamp


# https://stackoverflow.com/a/44659589
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

if __name__ == "__main__":
    main()

