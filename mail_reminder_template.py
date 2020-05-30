import os
import smtplib
from email.message import EmailMessage
import datetime as dt
import time
from typing import Tuple
import imghdr

# Global constants
# Match statelist elements w/ critical times
STATES_LIST = ['sample_reminder_1', 'sample_reminder_2']
CRITICAL_TIMES = ['2020-05-29 05:22', '2020-07-04 00:01']
current_state = 'STATIONARY'


#Email Constants
# If 2 step verification is enabled, use your app password!
# EMAIL_PASSWORD = input("Enter pw: ")
EMAIL_ADDRESS = os.environ.get('USER_EMAIL')
EMAIL_PASSWORD = os.environ.get('USER_APP_PW')

#Update current state based on dates
def update_current_state(curr_date_and_time: str) -> str:
    the_state = 'STATIONARY'
    for i in range (0, len(CRITICAL_TIMES)):
        # if current time matches a critical time, then update current state
        if(curr_date_and_time == CRITICAL_TIMES[i]):
            # print('going thru here')
            the_state = STATES_LIST[i]
            return the_state
    return the_state

# Set up fields based on current state before sending email
def set_message_fields() -> Tuple[str, str, str]:
    # Default state
    msg_subject = 'Default'
    msg_to = 'your.email@gmail.com'
    msg_body = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.' + \
               '  Integer malesuada nunc vel risus commodo viverra. Massa tincidunt nunc pulvinar sapien et ligula. Vulputate enim nulla aliquet porttitor lacus luctus.' + \
               '  Scelerisque eu ultrices vitae auctor. Vitae aliquet nec ullamcorper sit amet risus nullam eget. Semper viverra nam libero justo laoreet sit amet cursus.' + \
               '  Ultrices sagittis orci a scelerisque purus semper eget duis at. Pretium nibh ipsum consequat nisl vel pretium lectus quam. In iaculis nunc sed augue lacus viverra vitae congue.' + \
               '\n\n\nAutomated By' + \
               '\n-Automater'

    # Matching first element in states list
    if(current_state == STATES_LIST[0]):
        msg_subject = 'Sample Reminder 1'
        msg_to = 'your.email@gmail.com, second.email@gmail.com'
        msg_body = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.' + \
                   '  Integer malesuada nunc vel risus commodo viverra. Massa tincidunt nunc pulvinar sapien et ligula. Vulputate enim nulla aliquet porttitor lacus luctus.' + \
                   '  Scelerisque eu ultrices vitae auctor. Vitae aliquet nec ullamcorper sit amet risus nullam eget. Semper viverra nam libero justo laoreet sit amet cursus.' + \
                   '  Ultrices sagittis orci a scelerisque purus semper eget duis at. Pretium nibh ipsum consequat nisl vel pretium lectus quam. In iaculis nunc sed augue lacus viverra vitae congue.' + \
                   '\n\n\nAutomated By' + \
                   '\n-Automater'

    # Matching second element in states list 
    if (current_state == STATES_LIST[1]):
        msg_subject = 'Happy Independence Day! :)'
        msg_to = 'your.email@gmail.com'
        msg_body = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.' + \
                   '  Integer malesuada nunc vel risus commodo viverra. Massa tincidunt nunc pulvinar sapien et ligula. Vulputate enim nulla aliquet porttitor lacus luctus.' + \
                   '  Scelerisque eu ultrices vitae auctor. Vitae aliquet nec ullamcorper sit amet risus nullam eget. Semper viverra nam libero justo laoreet sit amet cursus.' + \
                   '  Ultrices sagittis orci a scelerisque purus semper eget duis at. Pretium nibh ipsum consequat nisl vel pretium lectus quam. In iaculis nunc sed augue lacus viverra vitae congue.' + \
                   '\n\n\nAutomated By' + \
                   '\n-Automater'
    return msg_subject, msg_to, msg_body

def send_email() -> None:
    # Add message fields before sending email
    the_msg_sub, the_msg_to, the_msg_body = set_message_fields()

    msg = EmailMessage()
    msg['Subject'] = the_msg_sub
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = the_msg_to
    msg.set_content(the_msg_body)

    # # Image or doc attach template
    # files = ['CS161SoInspirational.pdf']
    # for file in files:
    #     with open(file, 'rb') as f:
    #         file_data = f.read()
    #         # # use if its an image otherwise comment out
    #         # file_type = imghdr.what(f.name)
    #         file_name = f.name
    #
    #     # # add image to attachment
    #     # msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    #
    #     # add a pdf or doc to attachment
    #     msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)


    # with smtplib.SMTP('localhost', 1025) as smtp:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        #login
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Send email. Parameters: sendmail(Use email you logged in with, receiving email, message)
        smtp.send_message(msg)
        print("Email successfully sent!")


if(__name__ == '__main__'):
    prev_state = ''
    while True:
        # Get the current time
        current_date_and_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M')

        # Update the current state based on the time
        current_state = update_current_state(current_date_and_time)
        print(current_state)
        print(f'current time is: {current_date_and_time}')

        if current_state == 'STATIONARY':
            # reset previous state
            prev_state = ''

        # If current state isn't stationary, send email
        else:
            # if the previous state doesn't match current state (addresses timer issues)
            if prev_state != current_state:
                prev_state = current_state
                print('Proceeding to send email')
                send_email()
            else:
                print('Email(s) has already been sent')

        # Wait 30 seconds before running script again
        time.sleep(30)
