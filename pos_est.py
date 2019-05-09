import cv2
import glob
import numpy as np
import math

cbraw = 6
cbcol = 7


def add_id():
    fname = './1meter.jpg'
    img = cv2.imread(fname) 

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

    # 寻找角点，存入corners，ret是找到角点的flag
    ret, corners = cv2.findChessboardCorners(gray, (6, 7), None)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

    count = 0
    for corner in corners2:
        a, b = corner[0]
        a = int(a)
        b = int(b)

        cv2.putText(img, '(%s)' % (count), (a, b), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
        print('id={}:({},{})'.format(count, a, b))
        count += 1

        img = cv2.drawChessboardCorners(img, (cbraw, cbcol), corners2, ret)
        cv2.imshow('img', img)
        #cv2.waitKey(50000)
        cv2.imwrite('1meter_id.jpg', img)


def pos_estimate():
    # 1meter1.jpg 中： 单位：格子（一个格子34mm）       对应像素坐标和id
    # 左上：0，0                id = 5:(578,266)
    # 左下：0，5              id = 0:(568,502)
    # 右上：6，0              id = 41:(858,265)
    # 右下：6，5            id = 36:(857,500)

    # camX = 240
    # camY = 315

    object_3d_points = np.array(([0, 0, 0],
                                 [0, 5, 0],
                                 [6, 0, 0],
                                 [6, 5, 0]), dtype=np.double)
    object_2d_point = np.array(([578, 266],
                                [568, 502],
                                [858, 265],
                                [857, 500]), dtype=np.double)
    '''
    object_2d_point = np.array(([603, 219],
                                [576, 731],
                                [1343, 317],
                                [1341, 727]), dtype=np.double)
    '''
    dist_coefs = np.array([-0.00595347, 0.33683137, 0.00135723, 0.0026877 - 1.31780392],
                          dtype=np.double)
    camera_matrix = np.array((
        [1.45513349e+03, 0.00000000e+00, 9.49073700e+02],
        [0.00000000e+00, 1.49815619e+03, 5.94063862e+02],
        [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]), dtype=np.double)
    # 求解相机位姿
    found, rvec, tvec = cv2.solvePnP(object_3d_points, object_2d_point, camera_matrix, dist_coefs)

    print('found', found)
    print('rvec', rvec)
    print('tvec', tvec)

    rotM = cv2.Rodrigues(rvec)[0]
    camera_postion = -np.matrix(rotM).T * np.matrix(tvec)
    print(camera_postion.T)
   
    thetaZ = math.atan2(rotM[1, 0], rotM[0, 0]) * 180.0 / math.pi
    thetaY = math.atan2(-1.0 * rotM[2, 0], math.sqrt(rotM[2, 1] ** 2 + rotM[2, 2] ** 2)) * 180.0 / math.pi
    thetaX = math.atan2(rotM[2, 1], rotM[2, 2]) * 180.0 / math.pi
    
    x = tvec[0] * 34
    y = tvec[1] * 34
    z = tvec[2] * 34
    print('=' * 30)
    print(thetaX, thetaY, thetaZ)
    print("camPos:", x, y, z)


if __name__ == '__main__':
     add_id()
     pos_estimate()
