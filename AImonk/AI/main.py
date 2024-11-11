from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import torch
# from PIL import Image
# import io
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt

app = FastAPI()

import cv2
from ultralytics import YOLO
import numpy
# Load a model
model = YOLO("./yolo/yolov8n.pt")
coco_cls=[" person"," bicycle"," car"," motorcycle"," airplane"," bus"," train"," truck"," boat"," traffic light"," fire hydrant"," stop sign"," parking meter"," bench"," bird"," cat"," dog"," horse"," sheep"," cow"," elephant"," bear"," zebra"," giraffe"," backpack"," umbrella"," handbag"," tie"," suitcase"," frisbee"," skis"," snowboard"," sports ball"," kite"," baseball bat"," baseball glove"," skateboard"," surfboard"," tennis racket"," bottle"," wine glass"," cup"," fork"," knife"," spoon"," bowl"," banana"," apple"," sandwich"," orange"," broccoli"," carrot"," hot dog"," pizza"," donut"," cake"," chair"," couch"," potted plant"," bed"," dining table"," toilet"," tv"," laptop"," mouse"," remote"," keyboard"," cell phone"," microwave"," oven"," toaster"," sink"," refrigerator"," book"," clock"," vase"," scissors"," teddy bear"," hair drier"," toothbrush"]
  
# Response model for object detection results
class ImagePathRequest(BaseModel):
    image: str

@app.get("/")
def index():
    return {"details":"test pass!!"}

@app.post("/detect")
# async def detect_objects(image: UploadFile = File(...)):
async def detect_objects(request: ImagePathRequest):
 
    image_file=request.image
    # Perform inference
    results = model.predict(source=image_file)    
    # Prepare response with detected objects
    response = []
    img = cv2.imread(image_file)
    cmap = plt.get_cmap('tab20b')
    colors_ = [cmap(i)[:3] for i in np.linspace(0,1,20)]
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    # fontScale
    FONT_SCALE = 2e-3  # Adjust for larger font size in all images
    # Line thickness
    thickness = 1
    for result in results:
        for box in result.boxes.cpu().numpy():
            if box.conf <=.40:
                continue
            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
            _,_,width,height=box.xywh[0]
            color = colors_[int(x1) % len(colors_)]
            color = [i * 255 for i in color]    
            img = cv2.rectangle(img,(x1,y1),(x2,y2),color,2)
            name=coco_cls[int(box.cls)]
            fontScale=min(width, height) * FONT_SCALE
            fontScale=1
            img = cv2.putText(img,name,(x1,y1),font,fontScale, color, thickness, cv2.LINE_AA)    
            response.append({
                "label": name ,
                "confidence": float(box.conf),
                "bbox": [x1,y1,x2,y2]
            })

    file_name=os.path.basename(image_file) # get file name
    cv2.imwrite(f"/home/files/p_{file_name}",img)
    return {"objects": response,"p_image":f"/home/files/p_{file_name}"}