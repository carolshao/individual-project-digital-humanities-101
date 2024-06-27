import os
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

API_KEY = 'AIzaSyABXGQgDBfJppRO1uJWN3tT_DkefFhhvU8'
VIDEO_ID = 'cQ54GDm1eL0'

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_comments(video_id, max_comments=200):
    try:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100
        ).execute()

        comments_data = []
        total_fetched = 0

        while response and total_fetched < max_comments:
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comment_details = {
                    'username': comment['authorDisplayName'],
                    'comment': comment['textDisplay'],
                    'date': comment['publishedAt'],
                    'like_count': comment['likeCount'],
                }
                comments_data.append(comment_details)
                total_fetched += 1

                if total_fetched >= max_comments:
                    break

            if 'nextPageToken' in response and total_fetched < max_comments:
                response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    pageToken=response['nextPageToken'],
                    textFormat='plainText',
                    maxResults=100
                ).execute()
            else:
                break

        return comments_data
    except HttpError as e:
        print(f'An error occurred: {e}')
        return None

comments_data = get_video_comments(VIDEO_ID, max_comments=200)
if comments_data:
    df = pd.DataFrame(comments_data)
    df.to_csv('youtube_comments.csv', index=False)
    print("Comments saved to 'youtube_comments.csv'")
else:
    print("No comments found or an error occurred.")
