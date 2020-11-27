# Master thesis
# Using UAVs as a redudant system safety at autnonomous site

Installation manual for MasterThesis; run on CPU, (tested WSL 20.04/18.04 Ubuntu, Ubuntu 20.04/18.04)

Read complete tutorial before install.

Install WSL is introduced in the lowest part of the readme-file.
	
Errors (see futher down)

	20.04
	All Errors solved
	
	18.04
	Not all errors solved

Run all command in linux terminal

Step 1 - Install to run object detection

	sudo apt update
	
	sudo apt-get update
	
	sudo apt upgrade
	
	sudo apt install cmake

	cmake --version

	sudo apt install libopencv-dev python3-opencv

	opencv_version
	
If opencv_version = 4.2.0, check error 3 after last sudo apt-get install, and run the commands. 

	sudo apt install libomp-dev

	sudo apt install make git g++

	sudo apt-get install python3-pip

	sudo apt update
	
	sudo apt-get update
	
	sudo apt upgrade
		
	pip3 install imutils

	pip3 install matplotlib

	pip3 install scikit-image

	pip3 install pandas

	sudo apt-get install python3-tk

	sudo apt-get install tk-dev libagg-dev


Step 2 - Download Latest release

	https://github.com/Theralley/MasterThesis/releases

Unzip the folder to a place of your choice 

	
Step 3 - Download yolov4-tiny (20mb approx)

	https://tinyurl.com/y3rzejv8
	
Add yolov4-tiny (or other downloaded yolo.weight-file) to the folder. Tried files: v3, v3-tiny, v4, v4-tiny.

Best result, high acc, slow speed: v4

Best result, low acc, fast speed: v4-tiny


Step 3.1 - (WSL - Windows subsystem linux)

	Install Xming X Server for windows
	
	https://sourceforge.net/projects/xming/

Step 3.2 - Start a server on windows
	
Search Xlaunch in windows

	next, next, next (just press next until its disapear)

command in WSL terminal in the correct folder of choice 

	Shift + Right-click
	
	Open Linux Shell here
	
		export DISPLAY=:0

Have to do this every time you close WSL or restart windows. Start Xlaunch when restart windows. export DISPLAY=:0 always when restart WSl or close Terminal. 


Step 3 - First testrun

	python3 objectdetection.py 10.mp4 v4-tiny 0 20 30
	
	python3 map.py
	

Step 3.1 - Test motion detection
	
	python3 motion_detector.py -v 10.mp4
	


Step 3.2 - Example commands
	
	python3 objectdetection.py 10.mp4 v4-tiny 0 20 30
	
	python3 objectdetection.py 5.mp4 v4 0 15 30
	
	python3 objectdetection.py 10.MP4 v3-tiny 0 20 60
	
	python3 objectdetection.py 5.mp4 v3 0 15 30
	
	python3 map.py
	
	python3 motion_detector.py -v 6.mp4

You can change video inputs, see 6.mp4 or other example. You can change weight-file (pre-defined to yolov3 and v4), see v4-tiny or v4. You can change start frame, see 0 in command. You can change height, see 20 or 15(m). You can change angle, see 30 or 60(degree). Height and angle is for distance calculation. Map.py uses data from objectdetection.py. Important to see if mp4 or MP4.


Error 1
	
	Error
	ImportError: Cannot load backend 'TkAgg' which requires the 'tk' interactive framework, as 'headless' is currently running

	Solution
	Rerun
		python3 objectdetection.py 10.MP4 v4-tiny 0 20 30
		python3 map.py
	
Error 2
	
	Error
	module cv2 has no attribute dnn
	
	Solution
	sudo pip3 install opencv-contrib-python
	
Error 3
	
	Error
	Videos plays, nothing gets found

	Solution
	pip3 install scikit-build
	pip3 install opencv-python -vvv
	
	Why
	Wrong OpenCV version, update to 4.4.0
	
Error 4
	
	Error
	cv2.error (Open 4.2.0) .... : mish in funcation 'ReadDarknetFromCfgStrem'

	Solution
	pip3 install scikit-build
	pip3 install opencv-python -vvv
	
	If not prev. work
	Unsolved
	
Experienced (or lazy) - all installations in on line (speed-install) (20.04)

	sudo apt update -y && sudo apt-get update -y && sudo apt upgrade -y && sudo apt install cmake -y && sudo apt install libopencv-dev python3-opencv -y && sudo apt install libomp-dev -y && sudo apt install make git g++ -y && sudo apt-get install python3-pip -y && sudo apt update -y && sudo apt-get update -y && sudo apt upgrade -y && pip3 install imutils && pip3 install matplotlib && pip3 install scikit-image && pip3 install pandas && sudo apt-get install python3-tk -y && sudo apt-get install tk-dev libagg-dev -y 

Experienced (or lazy) - all installations in on line (speed-install) (18.04)

	sudo apt update -y && sudo apt-get update -y && sudo apt upgrade -y && sudo apt install cmake -y && sudo apt install libopencv-dev python3-opencv -y && sudo apt install libomp-dev -y && sudo apt install make git g++ -y && sudo apt-get install python3-pip -y && sudo apt update -y && sudo apt-get update -y && sudo apt upgrade -y && pip3 install imutils && pip3 install matplotlib && pip3 install scikit-image && pip3 install pandas && sudo apt-get install python3-tk -y && sudo apt-get install tk-dev libagg-dev -y && pip3 install scikit-build -y && pip3 install opencv-python -vvv
	
Step 0.5 - Install WSL (Windows Subsystem Linux) if want to "run in windows", recommended Ubuntu 20.04 LTS

To install the Windows Subsystem for Linux using PowerShell, use these steps:

Open Start.
Search for PowerShell, right-click the top result, and select the Run as administrator option.

Type the following command to enable the Linux subsystem and press Enter:

    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

Enable Windows Subsystem for Linux using PowerShell
Source: Windows Central
Type Y and press Enter to confirm and restart your computer.

When Restared, open Microsoft store, search and install:
	
	Ubuntu 20.04
	
Later search as a normal app for Ubuntu 20.04, and open. Use the new terminal in step 1-3. 

You can later open linux-shell in any folder, such as Master Thesis folder when using this command
	
	Shift + Right-click
	
	Open Linux Shell here
