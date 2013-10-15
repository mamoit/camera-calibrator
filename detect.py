#!/usr/bin/python
import cv2 as cv
import sys

##Extracts frames capturing chess patterns from video file to image file
#video ------- filename of the video
#folder_path - folder to put the output on
#file_name --- name of the output files (to distinguish several runs)
#chess_dim --- tupple with the number of inner corners of the pattern
def extract_patterns_video(video, folder_path, file_name, chess_dim):
	capture = cv.VideoCapture(video)
	files_gray = []
	files_patt = []
	Nframes = 0
	while True:
		rval, frame = capture.read()
		
		if rval:
			gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
			
			found_all, corners = cv.findChessboardCorners( gray, chess_dim )
			
			if found_all:
				cv.drawChessboardCorners(frame, chess_dim, corners, found_all)
				
				name_gray = folder_path+file_name+"-gray-"+str(Nframes)+".png"
				name_patt = folder_path+file_name+"-patt-"+str(Nframes)+".png"
				cv.imwrite(name_gray,gray)
				cv.imwrite(name_patt,frame)
				files_gray.append(name_gray)
				files_patt.append(name_patt)
				Nframes += 1
		else:
			break
	return (files_gray, files_patt)

def extract_patterns_images(frame_list, folder_path, file_name, chess_dim):
	files_gray = []
	files_patt = []
	Nframes = 0
	
	for frame_name in frame_list:
		frame = cv.imread(frame_name)
		gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
		
		found_all, corners = cv.findChessboardCorners( gray, chess_dim )
		
		if found_all:
				cv.drawChessboardCorners(frame, chess_dim, corners, found_all)
				
				name_gray = folder_path+file_name+"-gray-"+str(Nframes)+".png"
				name_patt = folder_path+file_name+"-patt-"+str(Nframes)+".png"
				cv.imwrite(name_gray,gray)
				cv.imwrite(name_patt,frame)
				files_gray.append(name_gray)
				files_patt.append(name_patt)
				Nframes += 1
	return (files_gray, files_patt)

#extract_patterns_images(frame_list, "/tmp","eraseme", (7, 5))

#extract_patterns_video(sys.argv[1],"/tmp/","eraseme", (7, 5))
