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
file_path = join(dirname(__file__), "./speech.mp3")

class MySynthesizeCallback(SynthesizeCallback):
    def __init__(self):
        SynthesizeCallback.__init__(self)
        self.fd = open(file_path, 'ab')

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_content_type(self, content_type):
        print('Content type: {}'.format(content_type))

    def on_timing_information(self, timing_information):
        print(timing_information)

    def on_audio_stream(self, audio_stream):
        self.fd.write(audio_stream)

    def on_close(self):
        self.fd.close()
        print('Done synthesizing. Closing the connection')

def speak(text):
    try:
        os.remove("./speech.mp3")
    except FileNotFoundError:
        pass
    my_callback = MySynthesizeCallback()
    print(text)
    service.synthesize_using_websocket(text,
                                    my_callback,
                                    accept='audio/mp3',
                                    voice='en-GB_JamesV3Voice'
                                    )
    cmd = "play speech.mp3 pitch 800 band 1000 150 bass -110 50 tempo 0.80 vol 300 channels 2"
    os.system(cmd)