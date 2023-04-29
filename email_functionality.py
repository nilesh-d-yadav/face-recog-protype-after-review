import csv
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
from email.mime.text import MIMEText
import pandas
import os
from datetime import date

def email_functionality():

    datetoday=date.today().strftime("%m_%d_%y")

    # //Reading csv attendance file :-
    attendanceList=[]
    with open(f'Attendance/Attendance-{datetoday}.csv','r') as f:
        reader=csv.reader(f)
        for d in reader:
            attendanceList.append(d)

    attendance_list = [[lst[1],lst[0], lst[2]] for lst in attendanceList[1:]]
    # print(attendance_list) #-- [['1', 'Nilesh Yadav'], ['2', 'John Wick'], ['3', 'Anu Yadav']]

    # Fetching Directory Emails: ['1,Nilesh Yadav,nileshy152@gmail.com', '2,John Wick,wick@gmail.com']
    directory_path="./Email"
    subdirectories=[]

    # //Append items to 'subdirectories list
    for subdir in os.listdir(directory_path):
        if os.path.isdir(os.path.join(directory_path,subdir)):
            subdirectories.append(subdir)

    email_list=[[lst.split(',')[0], lst.split(',')[2]] for lst in subdirectories];

    # print(email_list)             #[['1', 'nileshy152@gmail.com'], ['2', 'wick@gmail.com']]


    # Mail Code

    import smtplib
    server= smtplib.SMTP('smtp.gmail.com','587')
    server.starttls()
    user='190770107300@socet.edu.in'
    server.login(user,'EI447B83')




    for element in attendance_list:
        attendance_id = element[0]
        attendance_name = element[1]
        attendance_time=element[2]
        print(f"{attendance_id} {attendance_name} {attendance_time}")

        for sublist in email_list:
            if attendance_id in sublist:
                email_to_be_sent = sublist[1]
                msg = MIMEText(f"{attendance_name}'s Attendance Has Been Taken at {attendance_time}")
                msg['Subject'] = f"Attendance Report for {date.today()}"
                server.sendmail('190770107300@socet.edu.in', str(email_to_be_sent),
                                msg.as_string())

                print(f"Mail sent to {email_to_be_sent}")

    # A csv file record for admin for everyday's attendance
    dir_path='./Admin_attendance_record/'

    filename=f"{dir_path}{date.today().strftime('%Y-%m-%d')}.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(attendance_list)

    # send csv file to admin
    body=f"Please find attached the CSV file for {date.today()} attendance"
    subject1="Attendance File"
    message = MIMEMultipart()
    message.attach(MIMEText(body))

    with open(filename,"rb") as file:
        attachment = MIMEApplication(file.read(), _subtype='csv')
        attachment.add_header('Content-Disposition', 'attachment', filename=filename.split("/")[-1])
        message.attach(attachment)
        server.sendmail('190770107300@socet.edu.in','nileshdjangoboy@gmail.com',message.as_string())
        print("Admin got the Mail")
