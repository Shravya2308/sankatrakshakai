import json
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db

# from firebase_admin import firestore

# cred = credentials.Certificate("/Users/shubhammojidra/Desktop/operatorai/sankatrakshakai-firebase-adminsdk-145w3-6366ed8c8c.json")
# firebase_admin = firebase_admin.initialize_app(cred, {'databaseURL': 'https://sankatrakshakai-default-rtdb.firebaseio.com'})

import os
credential_path = "/Users/shrav/OneDrive/Desktop/major-project/auth.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def transcribe_file(speech_file, lang_code):
    """Transcribe the given audio file."""
    # from google.cloud import speech
    from google.cloud import speech_v1p1beta1 as speech
    import io

    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code=lang_code,
    )

    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print("")
        return result.alternatives[0].transcript

# text = transcribe_file("anwesha_marathi.mp3","mr-IN")



def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result["translatedText"]

# translation = translate_text("en-US",text)
