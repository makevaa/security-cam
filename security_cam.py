import cv2
from PIL import ImageFont, ImageDraw
import time
import datetime



def main():

    cam = cv2.VideoCapture(0)
    window_name = 'Talos Security'
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

        # Using cv2.putText() method
        stamp = get_timestamp()
        cv2.putText(frame, 'TALOS SEC [CAM 1]', (5, 30), font, fontScale, color, thickness, cv2.LINE_AA)
        cv2.putText(frame, get_timestamp(), (5, 60), font, fontScale, color, thickness, cv2.LINE_AA)
        
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


if __name__ == "__main__":
    main()

