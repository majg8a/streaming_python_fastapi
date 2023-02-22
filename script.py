from fastapi import FastAPI, Header
from fastapi.responses import Response
from os import getcwd, path

app = FastAPI()

PORTION_SIZE = 1024 * 1024

CURRENT_DIR = getcwd() + "/"


@app.get("/video/{name_video}")
def getVideo(nameVideo: str, range: str = Header(None)):
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end + PORTION_SIZE)
    filePath = CURRENT_DIR + nameVideo

    with open(filePath, "rb") as file:
        file.seek(start)
        data = file.read(end - start)
        sizeVideo = str(path.getsize(filePath))

        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{sizeVideo}',
            'Accept-Ranges': 'bytes'
        }

        return Response(content=data, status_code=206, headers=headers, media_type="video/mp4")


#https://github.com/mpimentel04/rtsp_fastapi/blob/master/webstreaming.py
#https://stackoverflow.com/questions/65971081/stream-video-to-web-browser-with-fastapi