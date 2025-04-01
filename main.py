from fastapi import FastAPI, HTTPException, Query
from instaloader import Instaloader, Post
from typing import List
import os

app = FastAPI()
L = Instaloader()

@app.get("/download")
async def download_instagram_video(url: str = Query(..., description="Instagram post URL")):
    """Downloads an Instagram video from the provided URL."""

    try:
        post = Post.from_permalink(L.context, url)
        if post.is_video:
            # Download the video and return the download link
            filename = L.download_post(post, target='.')
            if filename:
                video_url = f"/static/{filename[0]}.mp4" # adjust if needed
                return {"message": "Video downloaded successfully", "video_url": video_url}
            else:
                raise HTTPException(status_code=500, detail="Video download failed.")

        else:
            raise HTTPException(status_code=400, detail="URL does not point to a video post.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
