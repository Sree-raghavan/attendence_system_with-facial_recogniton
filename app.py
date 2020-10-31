
from tkinter import *  
import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import sys
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
############################################################### PLACE MENT OF LABELS #########################################################################
window = tk.Tk()

window.title("FACE RECOGNISED ATTENDENCE SYSTEM")

canvas=Canvas(window,width=1600,height=900)
image=ImageTk.PhotoImage(Image.open("background.jpg"))

canvas.create_image(0,0,anchor=NW,image=image)
canvas.pack()
#window.geometry('1280x720')
window.configure(background='white')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

message = tk.Label(window, text="ATTENDENCE SYSTEM USING FACE RECOGNITION" ,bg="BLACK"  ,fg="red"  ,width=50  ,height=3,font=('times', 30, ' bold')) 

message.place(x=100, y=20)



lbl = tk.Label(window, text="Enter  USER ID",width=20  ,height=2  ,fg="BLACK"  ,bg="red" ,font=('times', 15, ' bold ') ) 
lbl.place(x=200, y=200)

txt = tk.Entry(window,width=30  ,bg="red" ,fg="BLACK",font=('times', 15, ' bold '))
txt.place(x=575, y=215)



lbl2 = tk.Label(window, text="Enter  USER Name",width=20  ,fg="BLACK"  ,bg="red"    ,height=2 ,font=('times', 15, ' bold ')) 
lbl2.place(x=200, y=300)

txt2 = tk.Entry(window,width=30,bg="red"  ,fg="BLACK",font=('times', 15, ' bold ')  )
txt2.place(x=575, y=315)



lbl3 = tk.Label(window, text="ALERT : ",width=20  ,fg="BLACK"  ,bg="red"  ,height=2 ,font=('times', 15, ' bold underline ')) 
lbl3.place(x=200, y=400)

message = tk.Label(window, text="" ,bg="red"  ,fg="BLACK"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold ')) 
message.place(x=550, y=400)




lbl3 = tk.Label(window, text="RECORD: ",width=20  ,fg="BLACK"  ,bg="red"  ,height=2 ,font=('times', 15, ' bold  underline')) 
lbl3.place(x=300, y=620)


message2 = tk.Label(window, text="" ,fg="BLACK"   ,bg="red",activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold ')) 
message2.place(x=650, y=620)
 

###########################################################################################################################################################

def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage/ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(200) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>100:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('dataset/Details.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Image Trained"
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #create empty face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the imagei
        Id=nt(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)   
    df=pd.read_csv("dataset/Details.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)
    prev=None
    t=True 
    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                k=str(Id)
                
                tt=str(Id)+"-"+aa
                row=[Id, aa, date, timeStamp]
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
                if t == True or prev!=k:
                    with open('Attendance/attendence.csv','a+') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow(row)
                    csvFile.close()
                    t = False
                    prev=k
            else:   
                Id='Unknown'                
                tt=str(Id)
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown/Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    
    cam.release()
    cv2.destroyAllWindows()
    
    res=attendance
    message2.configure(text= res)


##########################################################################################################################################################
####################################################       PLACEMENT OF BUTTON       ######################################################################
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="BLACK"  ,bg="red"  ,width=20  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=200)

clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="BLACK"  ,bg="red"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=950, y=300) 

takeImg = tk.Button(window, text="CAPTURE", command=TakeImages  ,fg="BLACK"  ,bg="red"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=250, y=500)

trainImg = tk.Button(window, text="TRAIN", command=TrainImages  ,fg="BLACK"  ,bg="red"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=600, y=500)

trackImg = tk.Button(window, text="DETECT AND RECOGNISE", command=TrackImages  ,fg="BLACK"  ,bg="red"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=900, y=500)

quitWindow = tk.Button(window, text="EXIT", command=window.destroy  ,fg="BLACK"  ,bg="red"  ,width=5  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=1190, y=120)

####################################################################################################################################################
 
window.mainloop()
                