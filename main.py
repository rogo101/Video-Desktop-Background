# Written by Raghav Verma with the assistance of Keshav Verma
# Code not for open source use. Is proprietary.

import os
import time
import cv2
import ctypes

VIDEO_NAME = ''
SAVE_LOC = ''

IMAGE_NAME = 'new_background'

for f in os.listdir(SAVE_LOC):
    if IMAGE_NAME in f:
        os.remove(os.path.join(SAVE_LOC, f))
# exit()
minDelay = 0.01
updateInterval = 5

vidcap = cv2.VideoCapture(VIDEO_NAME)
fps = vidcap.get(cv2.CAP_PROP_FPS)
print('Video fps', fps)
delay = 1 / fps
totalCount = 0
origTime = time.time()
try:
    while True:
        count = 0
        startTime = time.time()
        # Every 30 seconds update the delay so that the actual fps matches the video fps
        while time.time() - startTime < updateInterval:
            success,image = vidcap.read()
            imgExtension = '.bmp'
            saveFile = f'{SAVE_LOC}{IMAGE_NAME}{count}{imgExtension}'
            try:
                cv2.imwrite(saveFile, image)
            except:
                # Need to restart video
                print('Finished video. Restarting')
                vidcap = cv2.VideoCapture(VIDEO_NAME)
                continue

            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, saveFile, 0)

            count += 1
            time.sleep(delay if delay > minDelay else minDelay)

        actualFps = count/(time.time() - startTime)
        print('Actual fps', actualFps)
        delayScale = actualFps / fps
        delay *= delayScale
        totalCount += count
except KeyboardInterrupt:
    print('Done!')
    print('Frames rendered', totalCount)
    print('Actual fps', totalCount/(time.time() - origTime))
