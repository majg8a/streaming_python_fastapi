(async () => {
  const video = document.createElement("video");
  await navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((signal) => {
      console.log(signal);
      video.srcObject = signal;
    })
    .catch(alert);
  video.controls = true;
  document.body.appendChild(video);
  video.play();
})();
