const blobToImage = async (blob = new Blob([])) => {
  const img = new Image();
  img.src = URL.createObjectURL(blob);
  await new Promise((res) => (img.onload = res));
  return img;
};

const videoToFrameBlob = async (video) => {
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const context = canvas.getContext("2d");
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  return await new Promise((res) => canvas.toBlob(res));
};

(async () => {
  const video = document.createElement("video");
  const mediastream = await navigator.mediaDevices
    .getUserMedia({ video: { width: 720, height: 360 } })
    .catch(alert);
  video.srcObject = mediastream;
  document.body.append(video);
  const canvas = document.createElement("canvas");

  const context = canvas.getContext("2d");
  document.body.append(canvas);
  const socket = new WebSocket("ws://localhost:5000/ws");

  socket.addEventListener("open", async (event) => {
    await video.play();
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const frameBlob = await videoToFrameBlob(video);
    socket.send(frameBlob);
  });

  socket.addEventListener("message", async ({ data }) => {
    const img = await blobToImage(data);
    context.drawImage(img, 0, 0, img.width, img.height);
    setTimeout(async () => socket.send(await videoToFrameBlob(video)), 0);
  });
})();
