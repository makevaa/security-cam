import cv2
from PIL import ImageFont
import time
import datetime
import numpy as np
import os


def main():
    program_version = "1.0.1"
    window_name = f'Citadel Security preview'

    print("Welcome to Citadel Security!")
    print(f"v{program_version}\n")
    print("The program shows user a window with image from a connected webcam device.\nThe optional image capture feature saves images to \"out\" folder at specified intervals.")
    print("Press ESC to exit program | Press SPACE to save an image from camera.")


    camera_w = input("\n[Optional] Enter image width in pixels (leave empty for camera default): ").strip()
    camera_w = camera_w.strip()
    
    if camera_w != "":
        print(f"--> Set image width to {camera_w}px")
        camera_w = int(camera_w)
    else:
        print(f"--> Set image width to camera default")
        camera_w = 0
 


    capture_interval = input("\n[Optional] Enter image capture interval in seconds (leave empty to disable image capture): ").strip()
 
    if capture_interval == "":
        capture_interval = 0
        print(f"--> Disabled image capture")
    else:
        print(f"--> Set capture interval to {capture_interval} seconds")
        capture_interval = int(capture_interval)

  

    preview_disabled = False
    preview_disabled_input = input('\n[Optional] Disable video preview window? (preview is on by default, enter "y" to disable it): ').strip()
    if (preview_disabled_input.lower() == "y"):
        preview_disabled = True
        print(f"--> Video preview disabled")
    else:
        print(f"--> Video preview enabled")
        cv2.namedWindow(window_name)


    cam = cv2.VideoCapture(0)

   
    # Font stuff for overlay
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.8
    color = (0, 255, 0)
    thickness = 2
    text_overlay_title = "CITADEL SECURITY [CAM 1]"

    # Logo stuff for overlay
    logo_image = cv2.imread('logo.png', cv2.IMREAD_UNCHANGED)
    logo_image_w = 60
    logo_image = image_resize(logo_image, width=logo_image_w)
    logo_padding_x = 10
    logo_padding_y = 5 
    logo_pos_y = logo_padding_y


    # Create "out" folder if it doesn't exists
    directory = "out"
    os.makedirs(directory, exist_ok = True)
    
    last_capture = 0

    print("\nMonitoring...")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        
        if (camera_w > 0):
            frame = image_resize(frame, width=camera_w)
      
        frame_h, frame_w, frame_channel = frame.shape

    
        # Put logo image on top-right of frame
        logo_pos_x = frame_w - logo_image_w - logo_padding_x
        add_transparent_image(frame, logo_image, logo_pos_x, logo_pos_y)


        # Text overlays
        # Draw text border using 2nd texts with higher thickness and black color
     
        text_x = frame_w-425
        text_y = 30
        timestamp = get_timestamp()
       
        cv2.putText(frame, text_overlay_title, (text_x, text_y), font, fontScale, (0, 0, 0), thickness+3, cv2.LINE_AA) #border
        cv2.putText(frame, text_overlay_title, (text_x, text_y), font, fontScale, color, thickness, cv2.LINE_AA)
        cv2.putText(frame, timestamp, (text_x+45, text_y+30), font, fontScale, (0, 0, 0), thickness+3, cv2.LINE_AA) #border
        cv2.putText(frame, timestamp, (text_x+45, text_y+30), font, fontScale, color, thickness, cv2.LINE_AA)
        
        if preview_disabled == False:
            cv2.imshow(window_name, frame)

        key = cv2.waitKey(1)

        if key%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif key%256 == 32:
            # SPACE pressed
            save_image(frame)

        # Save images periodically if capture is enabled
        if (capture_interval > 0 and time.monotonic() - last_capture >= capture_interval):
            last_capture = time.monotonic()
            save_image(frame)
        
           
        time.sleep(0.5)  

    cam.release()
    cv2.destroyAllWindows()


def save_image(frame):
    file_timestamp = get_file_name_timestamp()
    img_name = "out/CitadelSecurity {}.jpg".format(file_timestamp)
    cv2.imwrite(img_name, frame)
    print("{} written".format(img_name))


def get_timestamp():
    ts = time.time()
    stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return stamp


def get_file_name_timestamp():
    stamp = get_timestamp()
    stamp = stamp.replace(":", ".")
    return stamp


# image_resize function by thewaywewere: https://stackoverflow.com/a/44659589
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


# add_transparent_image function by Ben: https://stackoverflow.com/a/71701023
def add_transparent_image(background, foreground, x_offset=None, y_offset=None):
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
    assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'

    # center by default
    if x_offset is None: x_offset = (bg_w - fg_w) // 2
    if y_offset is None: y_offset = (bg_h - fg_h) // 2

    w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
    h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

    if w < 1 or h < 1: return

    # clip foreground and background images to the overlapping regions
    bg_x = max(0, x_offset)
    bg_y = max(0, y_offset)
    fg_x = max(0, x_offset * -1)
    fg_y = max(0, y_offset * -1)
    foreground = foreground[fg_y:fg_y + h, fg_x:fg_x + w]
    background_subsection = background[bg_y:bg_y + h, bg_x:bg_x + w]

    # separate alpha and color channels from the foreground image
    foreground_colors = foreground[:, :, :3]
    alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

    # construct an alpha_mask that matches the image shape
    alpha_mask = alpha_channel[:, :, np.newaxis]

    # combine the background with the overlay image weighted by alpha
    composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

    # overwrite the section of the background image that has been updated
    background[bg_y:bg_y + h, bg_x:bg_x + w] = composite

if __name__ == "__main__":
    main()
