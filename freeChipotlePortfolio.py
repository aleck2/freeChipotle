# USE PYTHON3

# Chipotle NBA finals contest. First n people to text them get a free entree
# This polls their twitter account and uses Twilio API to automatically text
# Chipotle the code they tweet out
# It also prints out the code and copies it to the clipboard if texting from
# computer

# For twitter:
#   Limited to 900 user requests per 15-minute window, 1500 for app requests
#   100,000 requests per day

# When configuring each twilio number, go to
# https://www.twilio.com/console/phone-numbers/ and select the no response handler
# to avoid sending back text responses to each chipotle text

import twitter
from twilio.rest import Client
import subprocess
import re
import time
from sys import argv    

account_sid='insert yours here'
auth_token='insert yours here'
to_number = 'put number here'

src_numbers = []
# src_numbers is a line delimited file of your twilio numbers
f = open("src_numbers.txt")
for line in f:
    src_numbers.append(line.strip("\n"))

client = Client(account_sid, auth_token)

CONSUMER_KEY = 'yours here'
CONSUMER_KEY_SECRET = 'yours here'
ACCESS_TOKEN = 'yours here'
ACCESS_TOKEN_SECRET = 'yours here'

################################################################################

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

def getopts(argv):
    opts = {}  
    while argv:
        if argv[0][0] == '-':  
            opts[argv[0]] = argv[1]  
        argv = argv[1:]  

    return opts

def sendTexts(code):
    for src_number in src_numbers:
        message = client.messages.create(body=code, from_=src_number, to=to_number)
        print(src_number, message.sid)


api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_KEY_SECRET,
access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

counter = 0
while (True):
    lastTweetId = getopts(argv)['-id']
    status = api.GetUserTimeline(screen_name='ChipotleTweets', since_id=str(lastTweetId), exclude_replies='true', include_rts='False', count='1') 
    counter += 1
    if (status):
        message = status[0].text

        code = re.search('[A-Z0-9]*FREE[A-Z0-9]*', message)
        #code = re.search('FREE[A-Za-z0-9]+', message)
        code = code.group(0)#.encode('utf-8')

        if (code):
            write_to_clipboard(code)
            print(message)
            #sendTexts(code)
            for i in range(1,10):
                print("***FOUND***")
            print("API calls used: ",counter)

            exit()

    time.sleep(.25)

