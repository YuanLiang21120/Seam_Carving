import numpy as np
import cv2
from src import forward_energy, seam_carving
import skvideo
import skvideo.io


cut = ["vertical", 30]
input_file = "pouncesmall.mp4"


cap = cv2.VideoCapture(input_file)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

print('fps = ' + str(fps))
print('number of frames = ' + str(frame_count))
print('duration (S) = ' + str(duration))
minutes = int(duration / 60)
seconds = duration % 60
print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))

vid_out = skvideo.io.FFmpegWriter("output.mp4",
                                  outputdict={'-vcodec': 'libx264',
                                              '-pix_fmt': 'yuv420p',
                                              '-r': str(fps)})

i = 1

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        print("Carve frame: " + str(i) + "/" + str(frame_count))
        img, eimg = seam_carving(frame, forward_energy, cut[1], cut[0])
        img = (img*255).astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        vid_out.writeFrame(img)
        cv2.imshow('frame', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        cv2.waitKey(int(fps))
    else:
        break
    i += 1

cap.release()
vid_out.close()
cv2.destroyAllWindows()
