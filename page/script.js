(async () => {
  const video = document.createElement("video");

  const mediastream = await navigator.mediaDevices
    .getUserMedia({ video: true })
    .catch(alert);

  // setInterval(() => {
  //   const imageCapture = new ImageCapture(stream.getVideoTracks()[0]);
  // }, 1000);
  // ws.onopen = () => setInterval(captureImage, 1000 / FPS); // ws is new WebSocket(WS_URL)

  const socket = new WebSocket("ws://localhost:5000/ws");

  // Connection opened
  socket.addEventListener("open", (event) => {
    const recorder = new MediaRecorder(mediastream);

    recorder.ondataavailable = ({ data }) => {
      data ? socket.send(data) : null;
    };

    recorder.start(1000);
  });

  // Listen for messages
  socket.addEventListener("message", (event) => {
    console.log("Message from server ", event.data);
  });
})();
