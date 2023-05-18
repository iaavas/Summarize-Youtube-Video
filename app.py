from flask import Flask, jsonify, request, Response
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS
from config import API_KEY



def summarize_my_video(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    available_languages = [trans.language_code for trans in transcript_list]

    english_dialects = [
        lang for lang in available_languages if lang.startswith('en')]

    transcript = transcript_list.find_manually_created_transcript(
        english_dialects)

    transcript_entries = transcript.fetch()

    transcript_text = ' '.join([entry['text'] for entry in transcript_entries])

    

    url = "https://gpt-summarization.p.rapidapi.com/summarize"

    payload = {
        "text": transcript_text,
        "num_sentences": 7
    }
    headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": API_KEY,
	"X-RapidAPI-Host": "gpt-summarization.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    summary = response.json()
    

    return summary


def get_youtube_video_id(link):
    video_id = None

    video_id = link.split('=')[1]

    return video_id


app = Flask(__name__)
cors = CORS(app)


@ app.route('/', methods=['POST'])
def summarize():

    data = request.get_json()
    youtube_link = data['link']

    video_id = get_youtube_video_id(youtube_link)
    summary = summarize_my_video(video_id)

    return jsonify(summary)


if __name__ == '__main__':
    app.run()
