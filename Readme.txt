Install MasterThesis run on CPU, (WSL 20.04 Ubuntu, Ubuntu 20.04)

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
If WSL
	Install Xming X Server for windows
		start a server
		export DISPLAY=:0
		//Have to do this every time you close WSL
pip3 install imutils
pip3 install matplotlib
pip3 install scikit-image
pip3 install pandas
pip3 install
sudo apt-get install python3-tk -y
sudo apt-get install tk-dev libagg-dev

Download yolov4-tiny weight (20mb approx)

First testrun
	python3 objectdetection.py 10.MP4 v4-tiny 0 20 30
	python3 map.py

If error (ImportError: Cannot load backend 'TkAgg' which requires the 'tk' interactive framework, as 'headless' is currently running)
	Rerun python3 objectdetection.py 10.MP4 v4-tiny 0 20 30
	then python3 map.py
