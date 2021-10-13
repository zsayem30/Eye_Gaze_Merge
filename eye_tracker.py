#!/usr/bin/env python

import glob
import os
import time
import pandas as pd 
import tkinter as tk
from tkinter import filedialog
import numpy as np

#Get the data for the eye gaze

# file_path_read_EyeGaze = filedialog.askopenfilename()
read_file_EyeGaze = pd.read_csv(r'/home/fizzer/Desktop/gazelog_21-07-2021_18-46-49.txt')
eye_gaze_df = pd.DataFrame(read_file_EyeGaze)
eye_gaze_header = list(eye_gaze_df.columns)[:-1]

Eye_Gaze = eye_gaze_df.to_numpy()[:, :-1]
Eye_Gaze[:, 0] = Eye_Gaze[:, 0]*10**-6

#Get the data for the kinematic logger

# file_path_read_KinematicLogger = filedialog.askopenfilename()
read_file_KinematicLogger = pd.read_excel(r'/home/fizzer/Downloads/dvrk_kinematic_logger_Epoch.xls')
KinematicLogger_df = pd.DataFrame(read_file_KinematicLogger)

KinematicLogger_header = list(KinematicLogger_df.columns)[:-5]
KinematicLogger = KinematicLogger_df.to_numpy()[:, :-5]

#Trim the kinematic data based on the eye gaze. The kinematic logger records data before the eye gaze is recorded and also after the recording of eye gaze is terminated 
lower_bound = Eye_Gaze[0, 0]
upper_bound = Eye_Gaze[-1, 0]

indexes = np.where((lower_bound < KinematicLogger[:,0]) & (upper_bound > KinematicLogger[:,0]))
Kinematic_Logger_Trimmed = KinematicLogger[indexes[0],:]
print(Eye_Gaze[0,0])

Kinematic_Logger_Trimmed[:,2] = [i for i in range(len(Kinematic_Logger_Trimmed))]
Kinematic_Logger_Trimmed[:,1] = Kinematic_Logger_Trimmed[:,1] - Kinematic_Logger_Trimmed[0,1]
Eye_Gaze[:, 2] = [i for i in range(len(Eye_Gaze))]

print('Length of Kinematic logger is', len(Kinematic_Logger_Trimmed))
print('Length of Eye_Gaze is', len(Eye_Gaze))

data_list = []

for i in range(len(Eye_Gaze) - 1):

	indexes = np.where((Eye_Gaze[i, 0] < Kinematic_Logger_Trimmed[:,0]) & (Eye_Gaze[i + 1, 0] > Kinematic_Logger_Trimmed[:,0]))
	kinematic_logger_array = Kinematic_Logger_Trimmed[indexes[0], :]
	gaze_array = np.tile(Eye_Gaze[i, :], (len(indexes[0]), 1))
	combined_array = np.concatenate((kinematic_logger_array, gaze_array), axis = 1)
	data_list.append(combined_array)

# Column_headers = KinematicLogger_header.append(eye_gaze_header)
all_Data = KinematicLogger_header + eye_gaze_header
Merged_data = [array for arraylist in data_list for array in arraylist]
Merged_Kinematic_Gaze_Data = np.vstack(Merged_data)
Merged_Kinematic_Gaze_Df = pd.DataFrame(Merged_Kinematic_Gaze_Data, columns = all_Data)
filepath = 'merged_kinematic_eyegaze_data.xlsx'
Merged_Kinematic_Gaze_Df.to_excel(filepath, index = False)
