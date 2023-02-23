const video = document.createElement("video");

function main() {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((signal) => {
      video.srcObject(signal);
      document.body.appendChild(video);
      video.play();
    })
    .catch(alert);
}
