import time
import os
from datetime import datetime
import logging

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

logging.basicConfig(filename='youtube.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

negative_comments = []
negativity_check_counter = 0

def get_my_videos():
    logging.info("List my most recent 5 videos.")

    try:
        response = yt.search().list(
            part='snippet',
            type='video',
            order='date',
            maxResults=5,
            channelId=secret.channel_id
        ).execute()
    except Exception as e:
        logging.error("Error listing the most recent videos: {}".format(e))

    videos = response.get('items', [])

    videos_list = []
    for video in videos:
        video_id = video['id']['videoId']
        video_title = video['snippet']['title']
        videos_list.append([video_id, video_title])
    
    logging.info(videos_list)
    time.sleep(3)
    return videos_list

def check_latest_comments(video_item):
    global negative_comments
    logging.info(f"List the most recent 100 comments for video {video_item[0]}")
    time.sleep(2)
    comments_request = yt.commentThreads().list(
        part='snippet',
        videoId=video_item[0],
        order='time',
        maxResults=100
    )

    try:
        comments_response = comments_request.execute()
    except Exception as e:
        logging.error("Error listing the latest comments: {}".format(e))

    i = 1
    for item in comments_response['items']:
        comment_id = item['id']
        comment_snippet = item['snippet']['topLevelComment']['snippet']
        text = comment_snippet['textDisplay']
        logging.info(f"Comment {i}: comment id: {comment_id} | {text}")
        logging.info("Checking if the comment is negative...")
        if is_negative(text):
            negative_comments.append([video_item[1], text])
            logging.warning("Comment is negative. Deleting it...")
            # TODO uncomment the following line if you are sure of deleting the negative comments
            #delete_comment(comment_id)
        else:
            logging.info("Comment is ok, moving on.")
        i+=1

def delete_comment(comment_id):
    time.sleep(3)

    try:
        yt.comments().delete(id=comment_id).execute()
        logging.info("Comment deleted successfully.")
    except Exception as e:
        logging.error("Error deleting comment: {}".format(e))

def is_negative(comment):
    global negativity_check_counter
    prompt = "Does this sentence have negative, aggressive, hateful or discouraging language? Say yes or no: \n"
    prompt += comment
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    negativity_check_counter = negativity_check_counter + 1
    return response.choices[0].message.content.lower().strip() == "yes"

def generate_report():
    logging.info(f"\n\n--------------REPORT--------------")
    logging.info(f"Checked {negativity_check_counter} comment and found {len(negative_comments)} negative comments.\n")
    for comment in negative_comments:
        logging.info(f"Video: {comment[0]} | Comment: {comment[1]}")
    logging.info(f"\n\n--------------END REPORT--------------")

def main():
    """
    1- Get my recent videos
    2- List all comments for a video (include comment text and id)
    3- For each comment, check positivity using chatgpt (return yes or no)
    4- delete any negative comment using comment id.
    """
    time.sleep(3)
    videos = get_my_videos()
    for video_item in videos:
        check_latest_comments(video_item)
    
    generate_report()


if __name__ == "__main__":
    main()