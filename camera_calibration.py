#!/usr/bin/python

# General imports
import numpy as np
import cv2
import json
import glob

# MACROS
CAMERA_ID = 0
H_CENTERS = 12
V_CENTERS = 18
SCALE = 1

def fill_data(images, objpoints, imgpoints, debug=True, hcenters=H_CENTERS, vcenters=V_CENTERS):
    # This function fills the objpoints and imgpoints list. 
    # The objpoints elements will be overwritten in the future.

    # Termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((hcenters * vcenters, 3), np.float32)
    objp[:, :2] = np.mgrid[0:hcenters, 0:vcenters].T.reshape(-1, 2)

    for fname in images:
        frame = cv2.imread(fname)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Find the chessboard centers
        corners_were_found, corners = cv2.findChessboardCorners(gray, (hcenters, vcenters), None)

        if corners_were_found:
            objpoints.append(objp)
            # Refine the corner locations
            cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)

            if debug:
                cv2.drawChessboardCorners(frame, (hcenters, vcenters), corners, corners_were_found)

        if debug:
            cv2.imshow('window', frame)
            cv2.waitKey(100)

    if debug:
        cv2.destroyWindow('window')

def store_matrices(mat_x, mat_y, file_name):
    file = cv2.FileStorage(file_name, cv2.FILE_STORAGE_WRITE)
    file.write("matrix_x", np.asarray(mat_x))
    file.write("matrix_y", np.asarray(mat_y))
    file.release()

def get_error(objp, imgpoints, rvecs, tvecs, mtx, distortion_vector):
    mean_error = 0
    for i in range(len(objp)):
        imgpoints2, _ = cv2.projectPoints(objp[i], rvecs[i], tvecs[i], mtx, distortion_vector)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        mean_error += error
    return mean_error / len(objp)

def show_result(mapx, mapy, cam_id=CAMERA_ID):
    cap = cv2.VideoCapture(cam_id)
    ret, frame = cap.read()

    while ret:
        ret, frame = cap.read()
        # Apply the undistortion
        u_frame = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
        cv2.imshow('Undistorted', u_frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyWindow('Undistorted')

if __name__ == "__main__":

    # Lists to store object points and image points from all the images.
    objpoints = []  # 3D points in real-world space
    imgpoints = []  # 2D points in the image plane.

    images = glob.glob('../img/*.jpg')
    gray = cv2.cvtColor(cv2.imread(images[0]), cv2.COLOR_BGR2GRAY)

    fill_data(images, objpoints, imgpoints)

    print("Calculating correction matrices")
    ret, mtx, distortion_vector, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    h, w = gray.shape
    # Output image size after the lens correction
    nh, nw = int(SCALE * h), int(SCALE * w)

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, distortion_vector, (w, h), 1, (nw, nh))
    # Get undistortion maps
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, distortion_vector, None, newcameramtx, (nw, nh), 5)

    store_matrices(mapx, mapy, "camera_matrices.xml")

    print("STD Error:", get_error(objpoints, imgpoints, rvecs, tvecs, mtx, distortion_vector))

    print("Showing the result")
    show_result(mapx, mapy)
