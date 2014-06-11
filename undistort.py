#!/usr/bin/env python
# encoding: utf-8
"""
undistort.py

This undistorts video using a given set of camera parameters and distortion
coefficients. You can get these for your camera using one of these packages:
    http://www.vision.caltech.edu/bouguetj/calib_doc/
    http://agisoft.ru/products/lens

In order to write out the undistorted video, your version of OpenCV will need
to be compiled with ffmpeg support. On OSX the easiest way to do this is with
homebrew (http://brew.sh). I had already installed ffmpeg and OpenCV so this is
the sequence I used which got everything working for me: 
    brew uninstall opencv
    brew uninstall ffmpeg
    brew install ffmpeg
    brew install opencv --with-ffmpeg

If Python has trouble finding OpenCV after this, you may need to do an
un/reinstallation of Python before the rest of the homebrew preparations. This
is undeniably a pain, but the good news is that your OpenCV install will be a
whole lot more useful afterwards.

Created by Dave Williams on 2014-06-11.
"""

import sys
import cv2
import numpy as np

# Set parameters
FILENAME_IN = "GOPR9444.MP4"
FILENAME_OUT = "undistorted.mp4"
CODEC = 'mp4v' #'IYUV' 
FC = [582.741, 580.065]  # focal lengths for GoPro Hero3+ Black
CC = [635.154, 371.917]  # principle points for same
KC = [-0.228, 0.0469, 0.0003, -0.0005, 0.0000]  # distortion coeffs for same



def create_matrix_profile(fc, cc, kc):
    """Create the camera matrix and distortion profile.

    Take in the focal lengths, principle points, and distortion coefficients
    and return the camera matrix and distortion coefficients in the form
    OpenCV needs.
    Takes:
        fc - the x and y focal lengths [focallength_x, focallength_y]
        cc - the x and y principle points [point_x, point_y]
        kc - the distortion coefficients [k1, k2, p1, p2, k3]
    Gives:
        cam_matrix - the camera matrix for the video
        distortion_profile - the distortion profile for the video
    """
    fx, fy = fc
    cx, cy = cc
    cam_matrix = np.array([[fx,  0, cx],
                           [ 0, fy, cy],
                           [ 0,  0,  1]], dtype='float32')
    distortion_profile = np.array(kc, dtype='float32')
    return cam_matrix, distortion_profile

def undistort_image(img, cam_matrix, distortion_profile):
    """Apply a distortion profile to an image.

    Takes:
        img - the image to undistort
        cam_matrix - the camera matrix for the camera
        distortion_profile - the lens' distortion
    Gives:
        undis_img - the image, undistorted
    """
    return cv2.undistort(img, cam_matrix, distortion_profile)

def log_it(message):
    """Print message to sys.stdout, without new line."""
    sys.stdout.write(message + "\r")
    sys.stdout.flush()

def imshow(img):
    cv2.namedWindow('disp')
    cv2.imshow('disp', img)
    cv2.waitKey(5000)
    cv2.destroyWindow('disp')

def main():
    cam_matrix, profile = create_matrix_profile(FC, CC, KC)
    # Load video
    video = cv2.VideoCapture(FILENAME_IN)
    fourcc = cv2.cv.FOURCC(*list(CODEC))
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS) 
    frame_count = video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
    size = (int(video.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
            int(video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
    writer = cv2.VideoWriter(FILENAME_OUT, fourcc, fps, size)
    while video.grab() is True:
        log_it("On frame %i of %i."%(video.get(cv2.cv.CV_CAP_PROP_POS_FRAMES), 
                                    frame_count))
        frame =  cv2.undistort(video.retrieve()[1], cam_matrix, profile)
        writer.write(frame)
    video.release()
    writer.release()

if __name__ == '__main__':
	main()
