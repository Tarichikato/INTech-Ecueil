import imageio
import time
import cv2
import numpy as np
import copy
from matplotlib import pyplot as plt
from fonctions import *

cap = cv2.VideoCapture(1)

# Check whether user selected camera is opened successfully.

if not (cap.isOpened()):

    print('Could not open video device')



else:

    while True:
        ret, color = cap.read()
        color_image_rgb = np.array(cv2.cvtColor(color, cv2.COLOR_BGR2RGB))
        print(get_sequence(color_image_rgb, 'Y'))

    cap.release()

    cv2.destroyAllWindows()