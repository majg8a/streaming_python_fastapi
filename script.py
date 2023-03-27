from fastapi import FastAPI, WebSocket, Request
import base64
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import cv2
import pose
app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()

        databstring = data.decode("utf-8").split(',')

        filedata = databstring[0]
        encoded_string = databstring[1]

        img = cv2.imdecode(np.fromstring(base64.b64decode(
            encoded_string), np.uint8), cv2.IMREAD_COLOR)

        poseResults = pose.predict(img)[11:]
        # print(poseResults[0])

        imgstr = bytes(
            f"{filedata},{str(base64.b64encode(cv2.imencode('.png', img)[1]), 'utf-8')}", "utf-8")

        await websocket.send_bytes(imgstr)

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
