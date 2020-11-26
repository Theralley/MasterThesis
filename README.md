# Master thesis
# Using UAVs as a redudant system safety at autnonomous site

Installation manual for MasterThesis; run on CPU, (tested WSL 20.04 Ubuntu, Ubuntu 20.04/18.04)

Step 1 - install

	sudo apt update -y && sudo apt-get update -y && sudo apt upgrade -y 

	sudo apt install cmake -y

	cmake --version

	sudo apt install libopencv-dev python3-opencv -y 

	opencv_version

	sudo apt install libomp-dev -y 

	sudo apt install make git g++ -y 

	sudo apt-get install python3-pip -y

	sudo apt update -y && sudo apt-get update -y && sudo apt upgrade -y

	sudo apt-get install fish -y
		
	pip3 install imutils

	pip3 install matplotlib

	pip3 install scikit-image

	pip3 install pandas

	sudo apt-get install python3-tk -y

	sudo apt-get install tk-dev libagg-dev -y

Step 2 - Download yolov4

	Download yolov4-tiny weight (20mb approx) 
	
	https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjogZC5m6DtAhXjxIsKHRR1CccQFjAAegQIBRAC&url=https%3A%2F%2Fgithub.com%2FAlexeyAB%2Fdarknet%2Freleases%2Fdownload%2Fdarknet_yolo_v4_pre%2Fyolov4-tiny.weights&usg=AOvVaw0mQ6LZDwchkF37sFuwpNSi
	
	Add yolov4-tiny, or other yolo.weight to folder 

Step 2.1 (WSL - Windows subsystem linux)

If WSL

	Install Xming X Server for windows

Then start a server on windows
	
	Search Xlaunch

		next, next, next

	command
	
		export DISPLAY=:0

	Have to do this every time you close WSL

Step 3 - First testrun

	python3 objectdetection.py 10.mp4 v4-tiny 0 20 30
	
	python3 map.py
	
Step 3.1 - Test motion detection
	
	python3 motion_detector.py -v 10.mp4
	

Step 3.2 - Example commands
	
	python3 objectdetection.py 10.mp4 v4-tiny 0 20 30
	
	python3 objectdetection.py 5.mp4 v4 0 15 30
	
	python3 objectdetection.py 10.mp4 v3-tiny 0 20 60
	
	python3 objectdetection.py 5.mp4 v3 0 15 30
	
	python3 map.py
	
	python3 motion_detector.py -v 6.mp4

You can change video inputs, see 6.mp4 or other example. You can change weight-file (pre-defined to yolov3 and v4), see v4-tiny or v4. You can change start frame, see 0 in command. You can change height, see 20 or 15(m). You can change angle, see 30 or 60(degree). Height and angle is for distance calculation. Map.py uses data from objectdetection.py. 

If error (nr1)
	
	ImportError: Cannot load backend 'TkAgg' which requires the 'tk' interactive framework, as 'headless' is currently running
	
Fix error (nr1)

	Rerun python3 objectdetection.py 10.MP4 v4-tiny 0 20 30
	
	then python3 map.py
	
All install in on line (speed-install)

	sudo apt update -y && sudo apt-get update -y && sudo apt upgrade -y && sudo apt install cmake -y && sudo apt install libopencv-dev python3-opencv -y && sudo apt install libomp-dev -y && sudo apt install make git g++ -y && sudo apt-get install python3-pip -y && sudo apt update -y && sudo apt-get update -y && sudo apt upgrade -y && sudo apt-get install fish -y && pip3 install imutils && pip3 install matplotlib && pip3 install scikit-image && pip3 install pandas && sudo apt-get install python3-tk -y && sudo apt-get install tk-dev libagg-dev -y 
