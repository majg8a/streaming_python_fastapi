from fastapi import FastAPI, WebSocket, Request
import base64
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import cv2
from PIL import Image
import io

app = FastAPI()


# Take in base64 string and return PIL image
def stringToImage(base64_string):
    return Image.open(io.BytesIO(imgdata))

# convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv


def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()

        encoded_string = data.decode("utf-8").split(',')[1]
        nparr = np.fromstring(base64.b64decode(encoded_string), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # cv2.imwrite('myloadedfile.png', img)

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
