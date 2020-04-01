undivid
=======

Undistort videos using OpenCV.

This undistorts video using a given set of camera parameters and distortion coefficients. You can get these for your camera using one of these packages:

    http://www.vision.caltech.edu/bouguetj/calib_doc/
    http://agisoft.ru/products/lens

# Dependencies
In order to write out the undistorted video, your version of OpenCV will need to be compiled with ffmpeg support. OpenCV is now included in the excellent `opencv-python` on which this depends. You should have a working copy after

`pip install opencv-python`

## Fallback
Previously, on OSX the easiest way to do this is with [Homebrew](http://brew.sh). I had already installed ffmpeg and OpenCV so this is the sequence I used which got everything working for me: 
 
    brew uninstall opencv
    brew uninstall ffmpeg
    brew install ffmpeg
    brew install opencv --with-ffmpeg

If Python has trouble finding OpenCV after this, you may need to do an
un/reinstallation of Python before the rest of the homebrew preparations. This is undeniably a pain, but the good news is that your OpenCV install will be a whole lot more useful afterwards.


