# from fastapi import FastAPI, Header, WebSocket
from fastapi import FastAPI, WebSocket
# from fastapi.responses import Response, StreamingResponse, FileResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()


# PORTION_SIZE = 1024 * 1024

# CURRENT_DIR = getcwd() + "/"


# @app.get("/video/{nameVideo}")
# def getVideo(nameVideo: str, range: str = Header(None)):
#     # start, end = range.replace("bytes=", "").split("-")
#     # start = int(start)
#     # end = int(start + PORTION_SIZE)
#     filePath = CURRENT_DIR + nameVideo

#     def iterfile():
#         with open(filePath, "rb") as file:
#             yield from file

#     return StreamingResponse(iterfile(), media_type="video/mp4")
# @app.get("/", response_class=HTMLResponse)
# async def pageUI(request):
#     return templates.TemplateResponse("index.html", context={"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        await websocket.send_bytes(data)


@app.get("/", response_class=RedirectResponse)
def redirect(request):
    print(f"dfasdfasdfasdf {request.url._url}")
    return f"{request.url._url}/page/index.html"


templates = Jinja2Templates(directory="/")
app.mount("/page", StaticFiles(directory="./page"), name="page")


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
