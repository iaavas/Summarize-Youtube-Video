from flask import Flask, jsonify, request, Response
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS


def summarize_my_video(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    available_languages = [trans.language_code for trans in transcript_list]

    english_dialects = [
        lang for lang in available_languages if lang.startswith('en')]

    transcript = transcript_list.find_manually_created_transcript(
        english_dialects)

    transcript_entries = transcript.fetch()

    transcript_text = ' '.join([entry['text'] for entry in transcript_entries])

    url = "https://api.meaningcloud.com/summarization-1.0"

    payload = {
        'key': '5839bdeacab27ff1c1a4035576b7c805',
        'txt': transcript_text,
        'sentences': 10
    }

    response = requests.post(url, data=payload)

    summary = response.json()['summary']

    return [summary, transcript_text]


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
    [summary, subtitles] = summarize_my_video(video_id)

    return jsonify({"en-Captions": subtitles, "summary": summary})


if __name__ == '__main__':
    app.run()
