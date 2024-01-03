import time
import os
from datetime import datetime

import secret

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from openai import OpenAI


# This code is to authenticate using an API KEY, but that won't work for deleting a comment.
#youtube = build('youtube', 'v3', developerKey=secret.youtube_api_key)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_desktop.json", ["https://www.googleapis.com/auth/youtube.force-ssl"])
credentials = flow.run_local_server(port=0)

# In order to delete a comment, we need to build the youtube API object using an OAuth 2.0 secret client JSON file.
yt = build("youtube", "v3", credentials=credentials)

client = OpenAI(
    api_key=secret.chatgpt_api_key,
)

def log(msg):
    formatted_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{formatted_timestamp} | INFO | {msg}\n")

def get_my_videos():
    uploads_playlist_request = yt.channels().list(
        part='contentDetails',
        id=secret.channel_id
    )

    uploads_playlist_response = uploads_playlist_request.execute()
    uploads_playlist_id = uploads_playlist_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    log("List my most recent 10 videos.")
    playlist_items_request = yt.playlistItems().list(
        part='contentDetails',
        playlistId=uploads_playlist_id,
        maxResults=10
    )

    videos = []

    playlist_items_response = playlist_items_request.execute()

    for item in playlist_items_response['items']:
        videos.append(item['contentDetails']['videoId'])

    log(videos)
    time.sleep(3)
    
    return videos

def check_latest_comments(video_id):
    log(f"List the most recent 50 comments for video {video_id}")
    time.sleep(2)
    comments_request = yt.commentThreads().list(
        part='snippet',
        videoId=video_id,
        order='time',  # Order by time to get the latest comments first
        maxResults=50   # Adjust as needed
    )

    comments_response = comments_request.execute()

    i = 1
    for item in comments_response['items']:
        comment_id = item['id']
        comment_snippet = item['snippet']['topLevelComment']['snippet']
        text = comment_snippet['textDisplay']
        log(f"Comment {i}: comment id: {comment_id} | {text}")
        log("Checking if the comment is negative...")
        if is_negative(text):
            log("Comment is negative. Deleting it...")
            delete_comment(comment_id)
        else:
            log("Comment is ok, moving on.")
        i+=1

def delete_comment(comment_id):
    time.sleep(3)

    try:
        yt.comments().delete(id=comment_id).execute()
        print("Comment deleted successfully.")
    except Exception as e:
        log("Error deleting comment: {}".format(e))

def is_negative(comment):
    prompt = "Does this sentence have negative, aggressive, hateful or discouraging language? Say yes or no: \n"
    prompt += comment
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.lower().strip() == "yes"

def main():
    """
    1- Get my recent videos
    2- List all comments for a video (include comment text and id)
    3- For each comment, check positivity using chatgpt (return Positive, Negative or Neutral)
    4- delete any negative comment using comment id.
    """
    time.sleep(3)
    videos = get_my_videos()
    for video_id in videos:
        check_latest_comments(video_id)


if __name__ == "__main__":
    main()