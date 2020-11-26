# Master thesis
# Using UAVs as a redudant system safety at autnonomous site

Installation manual for MasterThesis; run on CPU, (tested WSL 20.04 Ubuntu, Ubuntu 20.04/18.04)

1 sudo apt update -y && sudo apt-get update -y && sudo apt upgrade -y 

2 sudo apt install cmake -y

3 cmake --version

4 sudo apt install libopencv-dev python3-opencv -y 

5 opencv_version

6 sudo apt install libomp-dev -y 

7 sudo apt install make git g++ -y 

8 sudo apt-get install python3-pip -y

9 sudo apt update -y && sudo apt-get update -y && sudo apt upgrade -y

10 sudo apt-get install fish -y

10.1 If WSL, Install Xming X Server for windows
	
		start a server on windows
			
			Xlaunch, next, next, next
		
		command: export DISPLAY=:0
		
		//Have to do this every time you close WSL
		
11 pip3 install imutils

12 pip3 install matplotlib

13 pip3 install scikit-image

14 pip3 install pandas

15 sudo apt-get install python3-tk -y

16 sudo apt-get install tk-dev libagg-dev -y

17 Download yolov4-tiny weight (20mb approx) 
	
	https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjogZC5m6DtAhXjxIsKHRR1CccQFjAAegQIBRAC&url=https%3A%2F%2Fgithub.com%2FAlexeyAB%2Fdarknet%2Freleases%2Fdownload%2Fdarknet_yolo_v4_pre%2Fyolov4-tiny.weights&usg=AOvVaw0mQ6LZDwchkF37sFuwpNSi
	
	Add it to folder 

First testrun

	python3 objectdetection.py 10.mp4 v4-tiny 0 20 30
	
	python3 map.py
	
	also
	
	python3 motion_detector.py -v 10.mp4
	

If error (ImportError: Cannot load backend 'TkAgg' which requires the 'tk' interactive framework, as 'headless' is currently running)

	Rerun python3 objectdetection.py 10.MP4 v4-tiny 0 20 30
	
	then python3 map.py
	
All in on line

	sudo apt update -y && sudo apt-get update -y && sudo apt upgrade -y && sudo apt install cmake -y && sudo apt install libopencv-dev python3-opencv -y && sudo apt install libomp-dev -y && sudo apt install make git g++ -y && sudo apt-get install python3-pip -y && sudo apt update -y && sudo apt-get update -y && sudo apt upgrade -y && sudo apt-get install fish -y && pip3 install imutils && pip3 install matplotlib && pip3 install scikit-image && pip3 install pandas && sudo apt-get install python3-tk -y && sudo apt-get install tk-dev libagg-dev -y 
