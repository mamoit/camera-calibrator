#!/usr/bin/python
import cv2 as cv
import sys
import numpy as np
import detect as de

# Number of inner corners of the chess pattern
chess_dim = (7, 5)

if __name__ == "__main__":
	laplace = None
	colorlaplace = None
	planes = [ None, None, None ]
	capture = None
	
	# Direct capture from webcam
	if len(sys.argv) == 1:
#		capture = cv.VideoCapture(0)
		print "operation disabled"
		exit(1)
	
	# Capture from video file
	elif len(sys.argv) == 2:
		capture = cv.VideoCapture(sys.argv[1])
		grays, frames = de.extract_patterns_video(sys.argv[1], "/tmp/","eraseme",chess_dim)
	
	# Capture from list of image files
	elif len(sys.argv) >= 3:
		frames = sys.argv[1:]
		grays, frames = de.extract_patterns_images(frames, "/tmp/","eraseme",chess_dim)
	
	else:
		print "error in the arguments"
		exit(1)
	
#	if not capture:
#		print "Could not initialize capturing..."
#		sys.exit(-1)
	
	cv.namedWindow("Chessboard")
	
	single_chess = np.array([[[i, j, 0] for j in range(chess_dim[1]) for i in range(chess_dim[0])]])
	
	all_chess = []
	all_corners = []
	
	Nframes = 0
	
	for gray_name in grays:
		gray = cv.imread(gray_name)
		
		if Nframes == 0:
			imsize = (gray.shape[0], gray.shape[1])
		
		found_all, corners = cv.findChessboardCorners( gray, chess_dim )
		
		if found_all:
			gray = cv.cvtColor(gray,cv.COLOR_BGR2GRAY)
			corners = np.asarray([np.vstack((corners[i][0] for i in range(len(corners))))])
			cv.cornerSubPix(gray, corners, (5,5), (-1,-1), (cv.TERM_CRITERIA_MAX_ITER | cv.TERM_CRITERIA_EPS, 10, 0.01))
			
			cv.drawChessboardCorners( gray, chess_dim, corners, found_all )
			
			all_chess.append(single_chess[0])
			all_corners.append(corners[0])
			
			Nframes += 1
			
		cv.imshow("Chessboard", gray)
	
	all_chess = np.asarray(all_chess)
	all_corners = np.asarray(all_corners)
	retval, cameraMatrix, distCoeffs, rvecs, tvecs =\
	  cv.calibrateCamera(all_chess.astype('float32'),all_corners.astype('float32'),imsize)
	print cameraMatrix
	
	cv.waitKey()
	
	for frame_name in frames:
		frame = imread(frame_name)
		frame = cv.undistort(frame, cameraMatrix, distCoeffs)
		cv.imshow("Chessboard", frame)
		
		if cv.waitKey(10) != -1:
			break
		
	cv.waitKey()
	cv.destroyWindow("Chessboard")
