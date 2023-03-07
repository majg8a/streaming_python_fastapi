from fastapi import FastAPI, WebSocket, Request
import base64
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import cv2

app = FastAPI()


def to_image_string(image_filepath):
    return open(image_filepath, 'rb').read().encode('base64')

def from_base64(base64_data):
    nparr = np.fromstring(base64_data.decode('base64'), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        data.decode("utf-8")
        await websocket.send_bytes(data)

templates = Jinja2Templates(directory="page/")

@app.get("/ui")
def form_post(request: Request):
    return templates.TemplateResponse(
        "index.html", context={"request": request}
    )

app.mount("/", StaticFiles(directory="page"), name="page")


# https://fastapi.tiangolo.com/advanced/websockets/?h=web

# with open(filePath, "rb") as file:
#     file.seek(start)
#     data = file.read(end - start)
#     sizeVideo = str(path.getsize(filePath))

#     headers = {
#         'Content-Range': f'bytes {str(start)}-{str(end)}/{sizeVideo}',
#         'Accept-Ranges': 'bytes'
#     }

#     return Response(content=data, status_code=206, headers=headers, media_type="video/mp4")
