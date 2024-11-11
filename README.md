# AIMonk

AIMonk Technical Assessment -Poomagal Nanmaran
Follow steps below to upload image in UI and display processed image:
1.	Unzip the AImonk_poomagal.zip
2.	Navigate to AI folder, do bash build_docker.sh to build AI docker image.
3.	Do bash run_ai.sh to start ai docker.
4.	In new CLI, get the gateway ip of docker network with command “docker inspect -f '{{.NetworkSettings.Gateway}}' ai”
5.	Navigate to UI folder, do bash build_docker.sh to build UI docker image.
6.	Enter the gateway ip in main.py (AI_URL).Do bash run_ui.sh to start ui docker.
7.	In browser, type localhost:5000, upload image of choice by pressing button “Choose File”.
8.	Click on button “Process Image”.
Below is an example
    
Prerequisites that are met are docker, Flask, Fastapi and Yolov8 (object detection model)

