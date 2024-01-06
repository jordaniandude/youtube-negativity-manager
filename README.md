# YouTube Negativity Manager

A Python script to manage negative comments on your YouTube videos.

## Overview

This Python script leverages the YouTube API and OpenAI's ChatGPT to identify and remove negative comments from your YouTube videos. The process involves retrieving your recent videos, listing comments, evaluating their positivity, and deleting negative comments based on their IDs.

## Script Explanation

The script performs the following steps:

1. Retrieve your most recent videos.
2. List the top 100 comments for each video, including comment text and ID.
3. Evaluate the positivity of each comment using ChatGPT.
4. Delete any identified negative comments based on their IDs.

## Prerequisites

Before running the script, you need the following authentication methods:

1. **ChatGPT API Key:** Obtain an [API key](https://platform.openai.com/docs/quickstart?context=python) to authenticate to the ChatGPT API.
2. **YouTube API Authentication:** Obtain a [client secrets JSON file](https://developers.google.com/youtube/v3/guides/authentication) for OAuth 2.0 authentication.

## Dependencies

- `google_auth_oauthlib`
- `googleapiclient`
- `openai`

## Usage

1. Clone this repository:

    ```bash
    git clone https://github.com/jordaniandude/youtube-negativity-manager.git
    cd youtube-negativity-manager
    ```

2. Run the script:

    ```bash
    python3 youtube.py
    ```

## Disclaimer

Please use this script responsibly, as deleting comments can impact community engagement. Make sure to review the negative comments and adjust the script accordingly before enabling comment deletion.

Feel free to customize the script or provide feedback to enhance its functionality.
