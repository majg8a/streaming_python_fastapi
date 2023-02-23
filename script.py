from fastapi import FastAPI, Header
from fastapi.responses import Response,StreamingResponse
from os import getcwd, path

app = FastAPI()

PORTION_SIZE = 1024 * 1024

CURRENT_DIR = getcwd() + "/"


@app.get("/video/{nameVideo}")
def getVideo(nameVideo: str, range: str = Header(None)):
    # start, end = range.replace("bytes=", "").split("-")
    # start = int(start)
    # end = int(start + PORTION_SIZE)
    filePath = CURRENT_DIR + nameVideo

    def iterfile():
        with open(filePath, "rb") as file:
            yield from file

    return StreamingResponse(iterfile(), media_type="video/mp4")
    # with open(filePath, "rb") as file:
    #     file.seek(start)
    #     data = file.read(end - start)
    #     sizeVideo = str(path.getsize(filePath))

    #     headers = {
    #         'Content-Range': f'bytes {str(start)}-{str(end)}/{sizeVideo}',
    #         'Accept-Ranges': 'bytes'
    #     }

    #     return Response(content=data, status_code=206, headers=headers, media_type="video/mp4")
