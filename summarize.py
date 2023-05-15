import os
import datetime
import csv

import twilio as twilio


def count_subdirectories(directory):
    count = 0
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            count += 1
    return count


def present_students():
    today = datetime.date.today().strftime('%Y-%m-%d')
    filename=f"{today}.csv"
    # open the CSV file
    count=0
    with open(f"./Admin_attendance_record/{filename}", 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            count+=1
    return count


# to fetch emotion value
# from DeepFace import deep_face_data_list
# a=deep_face_data_list

# pushbullet
from twilio.rest import Client
account_sid = 'AC3e70cc45a7ba4b693c00f8e74499c7bb'
auth_token = 'key-value to be inserted here'
client = Client(account_sid, auth_token)


def main_run():
    today_present_student = present_students()
    registered_users = count_subdirectories('./static/faces')
    message = client.messages.create(to=("+91 8780214516"),
    body=f'\n\nHello from Face Recognition console. ! \n\n No. Of Students present today are: {today_present_student}\n\n'
         f'No. Of Registered Students are: {registered_users}\n\n Have a great day!'
                                     ,

                                     from_='+16076526968'
                                     )

    # Thoughts
    import requests
    category = 'happiness'
    api_url = 'https://api.api-ninjas.com/v1/quotes?limit=1?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': 'key-value to be inserted here'})

    if response.status_code == requests.codes.ok:
        quote_data= response.json()

        quote_text = quote_data[0]['quote']
        quote_author = quote_data[0]['author']
        return quote_text, quote_author
    else:
        print('Some Issues With The Internet:', response.status_code)
