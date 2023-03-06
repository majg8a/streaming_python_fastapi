const base64BlobToImage = async (src) => {
  const img = new Image();
  img.src = await src.text();
  await new Promise((res) => (img.onload = res));
  return img;
};

const videoToByteArrayBase64 = (video) => {
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const context = canvas.getContext("2d");
  context.drawImage(video, 0, 0);
  const utf8Encode = new TextEncoder();
  return utf8Encode.encode(canvas.toDataURL());
};

const videoStreaming = async () => {
  const video = document.createElement("video");
  const mediastream = await navigator.mediaDevices
    .getUserMedia({ video: { width: 720, height: 360 } })
    .catch(alert);
  video.srcObject = mediastream;
  const canvas = document.createElement("canvas");

  const context = canvas.getContext("2d");
  document.body.append(canvas);
  const socket = new WebSocket("ws://localhost:5000/ws");

  socket.addEventListener("open", async (event) => {
    await video.play();
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    socket.send(videoToByteArrayBase64(video));
  });

  socket.addEventListener("message", async ({ data }) => {
    const img = await base64BlobToImage(data);
    context.drawImage(img, 0, 0);
    setTimeout(async () => socket.send(videoToByteArrayBase64(video)), 10);
  });
};

videoStreaming();
