let atual = 0;
const banners = window.BANNERS;

function atualizar() {
    const banner = banners[atual];

    document.getElementById("banner-img").src =
        "/static/" + banner.imagem;

    document.getElementById("banner-titulo").innerText =
        banner.titulo;

    document.getElementById("banner-desc").innerText =
        banner.descricao_curta;

    document.getElementById("banner-link").href =
        "/conteudo/" + banner.id;
}

function proximo() {
    atual++;
    if (atual >= banners.length) {
        atual = 0;
    }
    atualizar();
}

function anterior() {
    atual--;
    if (atual < 0) {
        atual = banners.length - 1;
    }
    atualizar();
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("btn-proximo").addEventListener("click", proximo);
    document.getElementById("btn-anterior").addEventListener("click", anterior);
});
