import cv2
import glob
import numpy as np
import math

cbraw = 6
cbcol = 7


def cam_calibrate():

    objp = np.zeros((cbraw * cbcol, 3), np.float32)

    objp[:, :2] = np.mgrid[0:cbraw, 0:cbcol].T.reshape(-1, 2)
    print(objp)

    objpoints = []
    imgpoints = []

    images = glob.glob("./img/*.jpg")
    for fname in images:
      
        img = cv2.imread(fname)
        #img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (6, 7), None)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        objpoints.append(objp)
        imgpoints.append(corners2)
        img = cv2.drawChessboardCorners(gray, (cbraw, cbcol), corners2, ret)
        cv2.imshow('img', img)
        #cv2.waitKey(5000)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None,)

    print("ret:", ret)
    print("内参数矩阵mtx:\n", mtx) 
    print("dist:\n", dist)
    print("rvecs:\n", rvecs)
    print("tvecs:\n", tvecs)


if __name__ == '__main__':
     cam_calibrate()
