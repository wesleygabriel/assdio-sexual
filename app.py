import os
from flask import Flask, render_template, abort, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "chave-secreta-do-projeto"  # 🔐 obrigatória para session

# 🔹 LISTA DE BANNERS
banners = [
    {
        "id": 1,
        "titulo": "Assédio no Trabalho",
        "descricao_curta": "Entenda o que é assédio no ambiente de trabalho.",
        "descricao_completa": "Texto completo sobre assédio no trabalho.",
        "imagem": "images/banner1.jpg"
    },
    {
        "id": 2,
        "titulo": "Assédio Escolar",
        "descricao_curta": "Como identificar e denunciar o assédio escolar.",
        "descricao_completa": "Texto completo sobre assédio escolar.",
        "imagem": "images/banner2.jpg"
    },
    {
        "id": 3,
        "titulo": "Assédio Online",
        "descricao_curta": "Os perigos do assédio nas redes sociais.",
        "descricao_completa": "Texto completo sobre assédio online.",
        "imagem": "images/banner3.jpg"
    },
    {
        "id": 4,
        "titulo": "Tipos de Assédio",
        "descricao_curta": "Conheça os principais tipos de assédio.",
        "descricao_completa": "Descrição completa sobre os tipos de assédio.",
        "imagem": "images/banner4.jpg"
    }
]

# 🔹 ROTAS PRINCIPAIS
@app.route("/")
def index():
    return render_template("index.html", banners=banners)

@app.route("/contato")
def contact():
    return render_template("contact.html")

# 🔹 LOGIN (simples)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # login fictício (exemplo)
        session["usuario_logado"] = True
        return redirect(url_for("desabafo"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario_logado", None)
    return redirect(url_for("index"))

# 🔹 DESABAFO (PROTEGIDO)
@app.route("/desabafo", methods=["GET", "POST"])
def desabafo():
    if not session.get("usuario_logado"):
        return render_template("desabafo_bloqueado.html")

    mensagem = None
    nome = None
    anonimo = False

    if request.method == "POST":
        nome = request.form.get("nome")
        anonimo = request.form.get("anonimo")
        mensagem = request.form.get("mensagem")

    return render_template(
        "desabafo.html",
        mensagem=mensagem,
        nome=nome,
        anonimo=anonimo
    )

# 🔹 PESQUISA
@app.route("/pesquisa")
def pesquisa():
    termo = request.args.get("q", "").lower()

    resultados = [
        banner for banner in banners
        if termo in banner["titulo"].lower()
        or termo in banner["descricao_curta"].lower()
    ]

    return render_template(
        "pesquisa.html",
        termo=termo,
        resultados=resultados
    )

# 🔹 CONTEÚDO COMPLETO
@app.route("/conteudo/<int:id>")
def conteudo(id):
    banner = next((b for b in banners if b["id"] == id), None)
    if not banner:
        abort(404)
    return render_template("conteudo.html", banner=banner)

def main():
    app.run(port=int(os.environ.get('PORT', 5001)), debug=True)

if __name__ == "__main__":
    main()
