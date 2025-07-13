import cv2
from PIL import ImageFont, ImageDraw
import time
import datetime
import numpy as np

program_version = "1.0.0"


def main():
    print("Welcome to Citadel Security!")
    print(f"v{program_version}")
    print("")
    print("The program shows you a window with image from a connected webcam device.")
    print("Press ESC to exit program | SPACE to save an image from camera.")
    print("")

    camera_w = input("[Optional] Enter window width in pixels (leave empty for default 700): ")
    
    
    if camera_w == "":
        camera_w = 700
    else:
        camera_w = int(camera_w)


    capture_interval = input("[Optional] Enter image capture interval in seconds (leave empty to disable image capture): ")

    if capture_interval == "":
        capture_interval = 0
    else:
        capture_interval = int(capture_interval)


    cam = cv2.VideoCapture(0)
    window_name = f'CITADEL SECURITY v{program_version}'
    cv2.namedWindow(window_name)

    
    # Font stuff for overlay
    font = cv2.FONT_HERSHEY_SIMPLEX
    monospace = ImageFont.truetype("files/font/SourceCodePro-Regular.ttf",32)
    #font = monospace
    org = (50, 50) #text position
    fontScale = 0.8
    color = (0, 255, 0)
    thickness = 2

    start_time = time.monotonic()
    last_capture = start_time


    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        

        # image, width = None, height = None, inter = cv2.INTER_AREA):
        frame = image_resize(frame, width=camera_w)
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
            save_image(frame)

        #print(time.monotonic() )

        #time.sleep(60.0 - ((time.monotonic() - starttime) % 60.0))
        if ( capture_interval > 0 and time.monotonic() - last_capture >= capture_interval):
            last_capture = time.monotonic()
            save_image(frame)
        
           
        time.sleep(0.5)  

    cam.release()
    cv2.destroyAllWindows()

def save_image(frame):
    file_timestamp = get_file_name_timestamp()
    img_name = "out/CitadelSecurity {}.jpg".format(file_timestamp)
    cv2.imwrite(img_name, frame)
    print("{} written!".format(img_name))


def get_timestamp():
    ts = time.time()
    stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return stamp

def get_file_name_timestamp():
    stamp = get_timestamp()
    stamp = stamp.replace(":", ".")
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
