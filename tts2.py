import json
import os
import sys
from os.path import join, dirname
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

sys.path.append('/home/pi')  # persistent import directory for K9 secrets
from k9secrets import IAMAuthenticatorString, ServiceURLString  # gets the node-RED websocket address

authenticator = IAMAuthenticator(IAMAuthenticatorString)

service = TextToSpeechV1(authenticator=authenticator)
service.set_service_url(ServiceURLString)

try:
    os.remove("./speech.wav")
except FileNotFoundError:
    pass

text = input("Say this: ")
print(text)

with open(join(dirname(__file__), './speech.wav'),
          'wb') as audio_file:
    response = service.synthesize(
        text, accept='audio/wav',
        voice="en-GB_JamesV3Voice").get_result()
    audio_file.write(response.content)

cmd = "play speech.wav pitch 650 band 1000 150 bass -110 50 tempo 0.80 vol 300 channels 2"
os.system(cmd)

