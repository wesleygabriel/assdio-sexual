let videoAtual = 0;

function atualizarVideo() {
    const iframe = document.getElementById("video-frame");
    iframe.src = window.VIDEOS[videoAtual];
}

function videoProximo() {
    videoAtual++;
    if (videoAtual >= window.VIDEOS.length) {
        videoAtual = 0;
    }
    atualizarVideo();
}

function videoAnterior() {
    videoAtual--;
    if (videoAtual < 0) {
        videoAtual = window.VIDEOS.length - 1;
    }
    atualizarVideo();
}
