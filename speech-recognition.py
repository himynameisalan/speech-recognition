# Python program to translate
# speech to text and text to speech

import speech_recognition as sr
import pyttsx3
from kafka import KafkaProducer

user_name = input("Enter your name: ")
# Create Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Initialize the recognizer
r = sr.Recognizer()


# Function to convert text to
# speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


# Loop infinitely for user to
# speak

while 1:

    # Exception handling to handle
    # exceptions at the runtime
    try:

        # use the microphone as source for input.
        with sr.Microphone() as source:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source, duration=0.2)

            # listens for the user's input
            audio = r.listen(source)

            # Using google to recognize audio
            text = r.recognize_google(audio, language="zh-TW")
            # text = text.lower()

            # Keywords detection
            if '測試' in text:
                alert = '%s說了關鍵字' % user_name
                # Send message to Kafka
                producer.send('test_topic', bytes(alert, encoding='utf-8'))

            print(text)
            SpeakText(text)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")
