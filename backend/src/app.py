from fastapi import FastAPI, HTTPException, Query,File, Response
from pydantic import BaseModel, HttpUrl
from typing import List
import uvicorn
import os
import re
import sys
import urllib.request

from fastapi.responses import FileResponse
import os

import ffmpeg
from pytube import YouTube
from pytube.innertube import _default_clients
from main import *
from utils import Transcriber
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",  
    "http://127.0.0.1:3000"   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#find a way to make this work in any pc later
#for now it needs to be changed manually
#change it to your_base_directory/sub-forger/backend/src/downloads
VIDEO_DIRECTORY = "/home/samuel/sub-forger/backend/src/downloads"

@app.get("/downloads/{video_name}")
async def get_video(video_name: str):

    video_path = os.path.join(VIDEO_DIRECTORY, video_name, "burned_video.mp4")
    if not os.path.exists(video_path):
        return {"error": "Video not found"}
  
    return FileResponse(video_path, media_type="video/mp4")

class GenerateCommandsRequest(BaseModel):
    url: HttpUrl
    language_code: str = Query(..., min_length=2, max_length=2)  
    model_name: str

@app.post("/generate_commands/")
def generate_commands_endpoint(request: GenerateCommandsRequest):
    url = request.url
    language_code = request.language_code
    model_name = request.model_name

    try:
        
        commands = generate_commands(url, language_code, model_name)
        yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
        for command in commands:
            command.execute(yt=yt)
        
        
        return {"status": "success", "message": "Commands executed successfully", "output_path":commands[-1].output_path}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def generate_commands(url, language_code, model_name):
    yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
    yt_title = yt.title
    yt_length = yt.length
    download_folder = get_download_folder(yt_title, MAX_TITLE_SIZE)
    video_file_path = get_format_path(
        download_folder=download_folder, media="video", file_format="mp4"
    )
    wav_path = get_format_path(
        download_folder=download_folder, media="audio", file_format="wav"
    )
    srt_path = get_format_path(
        download_folder=download_folder, media="subs", file_format="srt"
    )
    output_video_path = get_format_path(
        download_folder=download_folder, media="burned_video", file_format="mp4"
    )

    # Making commands
    commands = [
        DownloadVideoCommand(download_folder=download_folder),
        DownloadThumbnailCommand(download_folder=download_folder, video_url=url),
        ConvertVideoToAudioCommand(
            video_file_path=video_file_path,
            download_folder=download_folder,
        ),
        Transcriber(wav_path, download_folder, yt_length, model_name, language_code),
        BurnSubtitlesCommand(
            video_file_path=video_file_path,
            subtitle_path=srt_path,
            output_path=output_video_path,
        ),
    ]
    return commands

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
