YouTube Negativity Manager
=======================================
A Python script to get rid of negative comments for your YouTube video.


-----

The program does the following:

1. Get my recent videos

2. List all comments for a video (include comment text and id)

3. For each comment, check positivity using chatgpt (return yes or no)

4. delete any negative comment using comment id.


You need the following two authentication methods:
1. An [API key](https://platform.openai.com/docs/quickstart?context=python) to authenticate to ChatGPT API.
2. A [client secrets json file](https://developers.google.com/youtube/v3/guides/authentication) to authenticate to YouTube API that uses OAuth 2.0.

To run the script:
```
python3 youtube.py
```
