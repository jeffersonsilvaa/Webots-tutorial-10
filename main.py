# **************************************************************
# Project 10 - Disciplina de robótica Móvel UFC / IFCE / LAPISCO
#       Simulação 10 com Drone Mavic 2 Pro - Webots R2020a
#       Veículo BMW X5 - controles básicos, Lidar e Câmera
#        Python 3.5 na IDE Pycharm - controller <extern>
#                By: Jefferson Silva Almeida
#                       Data: 24/03/2020
# **************************************************************

from vehicle import Driver
from controller import Camera
from controller import Lidar
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import math

TIME_STEP = 64 # ms
MAX_SPEED = 100 # km/h

driver = Driver()

speedFoward = 0.1 * MAX_SPEED  # km/h
speedBrake = 0 # km/h
cont = 0
plot = 10

cameraRGB = driver.getCamera('camera')
Camera.enable(cameraRGB, TIME_STEP)

lms291 = driver.getLidar('Sick LMS 291')
print(lms291)
Lidar.enable(lms291, TIME_STEP)
lms291_width = Lidar.getHorizontalResolution(lms291)
print(lms291_width)

fig = plt.figure(figsize=(3, 3))

while driver.step() != -1:

    if cont < 1000:
        driver.setDippedBeams(True) # farol ligado
        driver.setIndicator(0) # 0 -> OFF  1 -> Right   2 -> Left
        driver.setCruisingSpeed(speedFoward) # acelerador (velocidade)
        driver.setSteeringAngle(0.0) # volante (giro)
    elif cont > 1000 and cont < 1500:
        driver.setCruisingSpeed(speedBrake)
        driver.setBrakeIntensity(1.0) # intensidade (0.0 a 1.0)
    elif cont > 1500 and cont < 2500:
        driver.setCruisingSpeed(-speedFoward) # acelerador (velocidade)
        driver.setSteeringAngle(0.0) # volante (giro)
    elif cont > 2500:
        cont = 0

    # print('speed (km/h) %0.2f' % driver.getCurrentSpeed())

    cont += 1

    # ler a camera
    Camera.getImage(cameraRGB)
    Camera.saveImage(cameraRGB, 'color.png', 1)
    frameColor = cv.imread('color.png')
    cv.imshow('color', frameColor)
    cv.waitKey(1)

    # ler o Lidar
    lms291_values = []
    lms291_values = Lidar.getRangeImage(lms291)

    # plotar o mapa
    if plot == 10:
        y = lms291_values
        x = np.linspace(math.pi, 0, np.size(y))
        plt.polar(x, y)
        plt.pause(0.0001)
        plt.clf()
        plot = 0

    plot += 1

plt.show()
# plt.savefig('mapa.png')
