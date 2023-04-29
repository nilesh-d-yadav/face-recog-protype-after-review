# This is the defalut Running Environment
import cv2
import os
from flask import Flask, render_template, request,redirect, url_for
from database import dataset

from datetime import date
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib

global_list=[]


#### Defining Flask App
app = Flask(__name__,template_folder="template")

#### Saving Date today in 2 different formats
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")


#### Initializing VideoCapture object to access WebCam
face_detector = cv2.CascadeClassifier('static/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)


#### If these directories don't exist, create them
if not os.path.isdir('Attendance'):
    os.makedirs('Attendance')
if not os.path.isdir('static/faces'):
    os.makedirs('static/faces')
if f'Attendance-{datetoday}.csv' not in os.listdir('Attendance'):
    with open(f'Attendance/Attendance-{datetoday}.csv','w') as f:
        f.write('Name,Roll,Time')


#### get a number of total registered users
def totalreg():
    return len(os.listdir('static/faces'))


#### extract the face from an image
def extract_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_points = face_detector.detectMultiScale(gray, 1.3, 5)
    return face_points


#### Identify face using ML model
def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)


#### A function which trains the model on all the faces available in faces folder
def train_model():
    faces = []
    labels = []
    userlist = os.listdir('static/faces')
    for user in userlist:
        for imgname in os.listdir(f'static/faces/{user}'):
            img = cv2.imread(f'static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces,labels)
    joblib.dump(knn,'static/face_recognition_model.pkl')


#### Extract info from today's attendance file in attendance folder
def extract_attendance():
    df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    names = df['Name']
    rolls = df['Roll']
    times = df['Time']
    l = len(df)
    return names,rolls,times,l


#### Add Attendance of a specific user
from addAttendance import add_attendance

################## ROUTING FUNCTIONS #########################

# My Edits $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@app.route("/")
def hello_world():
    return render_template("login2.html")


# dataset={'nachi':'123', 'nilesh':'456', 'suresh':'789'}


# Form pe submit hone ke baad iss route pe aayega
@app.route('/form_login', methods=['POST','GET'])
def login():
    name1= request.form['username']
    pwd= request.form['password']

    if name1 not in dataset:
        return render_template("login2.html", info='INVALID USERNAME')
    else:
        if dataset[name1] != pwd:
            return render_template("login2.html", info='INVALID PASSWORD')
        else:
            return redirect(url_for("logged_in"))

# My Edits Over$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#Main Page
@app.route('/first_run')
def home():
    names,rolls,times,l = extract_attendance()
    return render_template('home.html',names=names,rolls=rolls,times=times,l=l,totalreg=totalreg(),datetoday2=datetoday2)


#### This function will run when we click on Take Attendance Button
@app.route('/start',methods=['GET'])
def start():
    if 'face_recognition_model.pkl' not in os.listdir('static'):
        return render_template('home.html',totalreg=totalreg(),datetoday2=datetoday2,mess='There is no trained model in the static folder. Please add a new face to continue.') 

    cap = cv2.VideoCapture(0)
    ret = True
    while ret:
        ret,frame = cap.read()
        if extract_faces(frame)!=():
            (x,y,w,h) = extract_faces(frame)[0]
            cv2.rectangle(frame,(x, y), (x+w, y+h), (255, 0, 20), 2)
            face = cv2.resize(frame[y:y+h,x:x+w], (50, 50))
            identified_person = identify_face(face.reshape(1,-1))[0]
            add_attendance(identified_person)
            cv2.putText(frame,f'{identified_person}',(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 20),2,cv2.LINE_AA)
        cv2.imshow('Attendance',frame)
        if cv2.waitKey(1)==27:
            break
    cap.release()
    cv2.destroyAllWindows()
    names,rolls,times,l = extract_attendance()    
    return render_template('home.html',names=names,rolls=rolls,times=times,l=l,totalreg=totalreg(),datetoday2=datetoday2)


#### This function will run when we add a new user
@app.route('/add',methods=['GET','POST'])
def add():
    newusername = request.form['newusername']
    newuserid = request.form['newuserid']

    # -----------------------------------------------------------------------------------------------------
    newusermail= request.form['newusermail']
    paths='Email/'+str(newuserid)+','+str(newusername)+','+str(newusermail)
    if not  os.path.isdir(paths):
        os.makedirs(paths)
    # -----------------------------------------------------------------------------------------------------


    userimagefolder = 'static/faces/'+newusername+'_'+str(newuserid)
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)
    cap = cv2.VideoCapture(0)
    i,j = 0,0
    while 1:
        _,frame = cap.read()
        faces = extract_faces(frame)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x, y), (x+w, y+h), (255, 0, 20), 2)
            cv2.putText(frame,f'Images Captured: {i}/50',(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 20),2,cv2.LINE_AA)
            if j%10==0:
                name = newusername+'_'+str(i)+'.jpg'
                cv2.imwrite(userimagefolder+'/'+name,frame[y:y+h,x:x+w])
                i+=1
            j+=1
        if j==500:
            break
        cv2.imshow('Adding new User',frame)
        if cv2.waitKey(1)==27:
            break
    cap.release()
    cv2.destroyAllWindows()
    print('Training Model')
    train_model()
    names,rolls,times,l = extract_attendance()    
    return render_template('home.html',names=names,rolls=rolls,times=times,l=l,totalreg=totalreg(),datetoday2=datetoday2)


# After Admin Logs In
@app.route('/log-in',methods=['GET'])
def logged_in():
    return render_template('homes.html')


# Evaluating Moods
@app.route('/eval_moods', methods=['GET'])
def evaluate_mood():
    return render_template()

# Connecting deepFace Model1
@app.route("/deep-face2", methods=['GET'])
def deepface2():
    from DeepFace import deeper_face
    emotion_list, most_common_items,most_common_count, deep_face_data_list=deeper_face()
    # My Edits
    from twilio.rest import Client
    account_sid = 'AC3e70cc45a7ba4b693c00f8e74499c7bb'
    auth_token = '79464a8f3fce5468bc72cd5672ad13e1'
    client = Client(account_sid, auth_token)

    message = client.messages.create(to=("+91 8780214516"),
                                     body=f'\n\n! \n\n Student had the following emotions  {emotion_list} and the most common was {most_common_items}'
                                     ,

                                     from_='+16076526968'
                                     )
    print("Message sent from /deep-face2 route")
    # My Edits Ends
    return render_template('Emotion_Report_Students.html', my_list=emotion_list, most_common=most_common_items, common_number=most_common_count)

# Connecting deepFace Model1
@app.route("/deep-face1", methods=['GET'])
def deepface1():
    return render_template('Emotion_Report.html')

# Summarize Function
@app.route('/summarizes', methods=['GET'])
def run_summarize():
    from summarize import main_run
    text, author=main_run()
    return render_template('end.html', thought=text, author=author)

# System Information
@app.route('/system_details', methods=['GET'])
def get_system_details():
    return render_template('github.html')

# Email Routing
@app.route('/mailed',methods=['GET'])
def send_emails():
    from email_functionality import email_functionality
    email_functionality()
    return render_template('homes.html')


#### Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True, port=8000)
