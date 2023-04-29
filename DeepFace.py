import cv2
from flask import Flask, render_template, request,redirect, url_for
import io
import base64
from flask import Flask, render_template
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import messagebox
from deepface import DeepFace
from datetime import datetime

deep_face_data_list=[]

emotion_list = []
# # Create a folder to store the photos
if not os.path.exists("photos"):
    os.mkdir("photos")
#

# directory path
directory="./photos"
today = datetime.now().strftime('%Y-%m-%d')
new_folder_name = os.path.join(directory, today) #./photos/'2023-04-17'

if not os.path.exists(new_folder_name):
    os.makedirs(new_folder_name)


def deeper_face():
# Set up the webcam
    cap = cv2.VideoCapture(0)
    # # # Set up the counter for the photo filenames
    count = 0
    # # # Set up the dialog box
    root = tk.Tk()
    root.withdraw()
    # #
    while True:
    # #     # Capture a frame from the webcam
        ret, frame = cap.read()
    # #     # Show the live feed with the photo count
        cv2.putText(frame, "Photo count: {}".format(count), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Webcam", frame)
    # #
    # #     # Wait for a key press
        key = cv2.waitKey(1)
    # #
    # #     # Take a photo if the spacebar is pressed
        if key == ord(" "):
    #         # Increment the photo count
            count += 1
    # #
    # #         # Save the photo to a file #./photos/'2023-04-17'
            filename = os.path.join(new_folder_name, "photo{}.jpg".format(count))
            cv2.imwrite(filename, frame)
    # #
    # #         # Show a dialog box to confirm the photo was taken
            messagebox.showinfo("Photo taken", "Photo {} taken".format(count))
    #
    # #         Using deep face to analyze image and store it in a list
            image = cv2.imread(f"{new_folder_name}/photo{count}.jpg")
            result_emotion = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
            emotion_list.append(result_emotion[0]['dominant_emotion'])
            print(emotion_list)

    #         Most common emotion , thanks to ChatGPT for this


            from collections import Counter
            my_list = [1, 2, 3, 2, 1, 3, 3, 3, 3]
            # Count the occurrences of each element in the list
            counter = Counter(emotion_list)
            # Get the most common element(s)
            most_common = counter.most_common()
            most_common_count=most_common[0][1]
            most_common_items = [item for item, count in most_common if count == most_common_count]
            deep_face_data_list=most_common
#
    # #     # Exit the loop if the escape key is pressed
        elif key == 27:

            break
    # #
    # # # Release the webcam and close the windows
    cap.release()
    cv2.destroyAllWindows()
    return emotion_list,most_common_items,most_common_count, deep_face_data_list
    # return render_template('Emotion_Report_Students.html', my_list=emotion_list, most_common=most_common, common_number=common_number)

