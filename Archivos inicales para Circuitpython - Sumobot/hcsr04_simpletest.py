from hcsr04 import HCSR04
import board
import time

sonar = HCSR04(board.IO26,board.IO25)

while True:
    dist = sonar.dist_cm()
    print(dist)
    time.sleep(0.2)