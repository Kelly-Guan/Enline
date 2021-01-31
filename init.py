from flask import Flask, render_template, request, redirect, url_for
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Wu\Downloads\HackViolet\ServiceAccount.json"

app = Flask(__name__)

@app.route("/translate")
def translate():
    # speech-to-text portion
    def transcribe_gcs(gcs_uri):
        from google.cloud import speech
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=48000,
            language_code="en-US",
        )
        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=90)
        text = []
        for result in response.results:
            text.append(result.alternatives[0].transcript)
        return "".join(text)
    f = "gs://audiofiles-underthemoon/New Recording 2.flac" #replace this with the user's audio file
    text = transcribe_gcs(f)

    # translation portion
    from google.cloud import translate_v2 as translate
    translate_client = translate.Client()
    target = "zh"
    output = translate_client.translate(
        text,
        target_language = target
    )
    i = 0
    last = ""
    for key, value in output.items():
        if i == 0:
            last = value
        i += 1
    
    return last

if __name__ == "__main__":
    app.run()