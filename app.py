import os
from flask import Flask, render_template, abort, request, session, redirect, url_for, flash
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "chave-secreta-do-projeto"  # 🔐 obrigatória para session



# 🔹 LISTA DE BANNERS
banners = [
    {
        "id": 1,
        "titulo": "Assédio no Trabalho",
        "descricao_curta": "Entenda o que é assédio no ambiente de trabalho.",
        "descricao_completa": (
            "O assédio no trabalho ocorre quando um funcionário é exposto, de forma "
            "repetitiva ou contínua, a situações humilhantes, constrangedoras ou "
            "ameaçadoras durante o exercício de suas funções. Essas atitudes podem "
            "partir de superiores hierárquicos, colegas ou até clientes, e incluem "
            "ofensas verbais, cobranças excessivas, isolamento, desvalorização "
            "profissional ou abusos de poder. O assédio prejudica a saúde mental, "
            "emocional e física do trabalhador, além de afetar o ambiente organizacional, "
            "tornando essencial a conscientização, a prevenção e a denúncia dessas práticas."
        ),
        "imagem": "images/banner1.jpg"
    },
    {
        "id": 2,
        "titulo": "Assédio Escolar",
        "descricao_curta": "Como identificar e denunciar o assédio escolar.",
        "descricao_completa": (
            "O assédio escolar, também conhecido como bullying, envolve comportamentos "
            "repetidos de agressão física, verbal ou psicológica entre estudantes. "
            "Essas ações podem incluir apelidos ofensivos, exclusão social, ameaças, "
            "agressões físicas ou humilhações públicas. O assédio escolar afeta "
            "diretamente o desenvolvimento emocional, o rendimento acadêmico e a "
            "autoestima das vítimas, podendo gerar consequências graves se não for "
            "identificado e combatido adequadamente."
        ),
        "imagem": "images/banner2.jpg"
    },
    {
        "id": 3,
        "titulo": "Assédio Online",
        "descricao_curta": "Os perigos do assédio nas redes sociais.",
        "descricao_completa": (
            "O assédio online ocorre no ambiente digital, principalmente em redes sociais, "
            "aplicativos de mensagens e plataformas virtuais. Ele se manifesta por meio "
            "de comentários ofensivos, ameaças, perseguição, exposição de informações "
            "pessoais ou disseminação de mensagens de ódio. Apesar de acontecer no meio "
            "virtual, o assédio online causa impactos reais na saúde emocional das vítimas, "
            "podendo gerar ansiedade, medo e isolamento social."
        ),
        "imagem": "images/banner3.jpg"
    },
    {
        "id": 4,
        "titulo": "Tipos de Assédio",
        "descricao_curta": "Conheça os principais tipos de assédio.",
        "descricao_completa": (
            "O assédio pode ocorrer de diversas formas, como assédio moral, sexual, "
            "psicológico, institucional ou virtual. Cada tipo possui características "
            "específicas, mas todos têm em comum o desrespeito à dignidade humana. "
            "Reconhecer os diferentes tipos de assédio é fundamental para identificar "
            "situações abusivas, proteger as vítimas e promover ambientes mais seguros, "
            "respeitosos e justos."
        ),
        "imagem": "images/banner4.jpg"
    },
    {
        "id": 5,
        "titulo": "Assédio Moral",
        "descricao_curta": "Práticas abusivas que afetam a dignidade da vítima.",
        "descricao_completa": (
            "O assédio moral consiste em atitudes repetitivas que visam humilhar, "
            "desqualificar ou desestabilizar emocionalmente uma pessoa. Ele pode ocorrer "
            "por meio de críticas constantes, exposição ao ridículo, isolamento, "
            "ameaças veladas ou excesso de cobranças. Esse tipo de assédio compromete "
            "a saúde mental da vítima e pode gerar sentimentos de medo, insegurança "
            "e baixa autoestima."
        ),
        "imagem": "images/banner5.jpg"
    },
    {
        "id": 6,
        "titulo": "Assédio Sexual",
        "descricao_curta": "Condutas inadequadas de cunho sexual.",
        "descricao_completa": (
            "O assédio sexual envolve comportamentos indesejados de natureza sexual, "
            "como comentários, insinuações, gestos, contatos físicos ou chantagens. "
            "Ele pode ocorrer em ambientes de trabalho, estudo ou em espaços públicos, "
            "causando constrangimento, medo e sofrimento à vítima. O assédio sexual "
            "é crime e deve ser denunciado para garantir a proteção e os direitos "
            "da pessoa afetada."
        ),
        "imagem": "images/banner6.jpg"
    },
    {
        "id": 7,
        "titulo": "Consequências do Assédio",
        "descricao_curta": "Impactos do assédio na vida das vítimas.",
        "descricao_completa": (
            "As consequências do assédio podem ser profundas e duradouras, afetando "
            "a saúde mental, emocional e física da vítima. Entre os impactos mais "
            "comuns estão ansiedade, estresse, queda de autoestima, dificuldades "
            "de relacionamento e problemas de desempenho escolar ou profissional. "
            "Por isso, é fundamental reconhecer os sinais e buscar apoio."
        ),
        "imagem": "images/banner7.jpg"
    },
    {
        "id": 8,
        "titulo": "Como Denunciar o Assédio",
        "descricao_curta": "Saiba quais passos seguir para denunciar.",
        "descricao_completa": (
            "Denunciar o assédio é um passo importante para interromper práticas "
            "abusivas e proteger outras pessoas. A vítima pode buscar apoio em "
            "instituições, canais oficiais, responsáveis legais ou órgãos competentes. "
            "Registrar provas, procurar orientação e não se silenciar são atitudes "
            "essenciais para o enfrentamento do assédio."
        ),
        "imagem": "images/banner8.jpg"
    }
]





# rota principal


@app.route("/")
def index():
    return render_template("index.html", banners=banners)

@app.route("/contato", methods=["GET", "POST"])
def contact():
    enviado = False

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        mensagem = request.form["mensagem"]

        msg = EmailMessage()
        msg["Subject"] = "Contato - Site Bota Pra Fora"
        msg["From"] = "seu email"
        msg["To"] = "seu email"
        msg.set_content(f"""
Nome: {nome}
E-mail: {email}

Mensagem:
{mensagem}
        """)

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login("seu email", "senha de app")
                smtp.send_message(msg)

            enviado = True

        except Exception as e:
            print(e)

    return render_template("contact.html", enviado=enviado)


# ===============================
# 🔹 LOGIN (SIMPLES)
# ===============================

@app.route("/login", methods=["GET", "POST"])
def login():
    # 🔒 se já estiver logado
    if session.get("usuario_logado"):
        flash("Você já está logado.")
        return redirect(url_for("index"))
        # ou: return redirect(url_for("desabafo"))

    if request.method == "POST":
        # login fictício
        session["usuario_logado"] = True

        # redirecionamento pós-login (se veio do desabafo bloqueado)
        destino = session.pop("destino_pos_login", None)
        flash("Login realizado com sucesso!")

        if destino:
            return redirect(destino)

        return redirect(url_for("index"))

    return render_template("login.html")


# ===============================
# 🔹 LOGOUT
# ===============================

@app.route("/logout")
def logout():
    session.pop("usuario_logado", None)
    return redirect(url_for("index"))

# ===============================
# 🔹 DESABAFO (PROTEGIDO)
# ===============================

@app.route("/desabafo", methods=["GET", "POST"])
def desabafo():
    if not session.get("usuario_logado"):
        # salva tentativa de acesso
        session["proxima_pagina"] = url_for("desabafo")
        return render_template("desabafos_bloqueado.html")

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

# ===============================
# 🔹 historicode desabafos
# ===============================
desabafos = []

@app.route("/meus_desabafos")
def meus_desabafos():
    usuario = session.get("usuario_id")

    meus = [d for d in desabafos if d["usuario"] == usuario]

    return render_template("meus_desabafos.html", desabafos=meus)


# ===============================
# 🔹 excluir
# ===============================

@app.route("/excluir_desabafo/<int:id>", methods=["POST"])
def excluir_desabafo(id):
    global desabafos
    usuario = session.get("usuario_id")

    desabafos = [d for d in desabafos if not (d["id"] == id and d["usuario"] == usuario)]
    return redirect(url_for("meus_desabafos"))

# ===============================
# 🔹 publico
# ===============================
@app.route("/desabafos_publicos")
def desabafos_publicos():
    return render_template(
        "desabafos_publicos.html",
        desabafos=desabafos
    )


# ===============================
# 🔹 PESQUISA
# ===============================

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

# ===============================
# 🔹 CONTEÚDO COMPLETO
# ===============================

@app.route("/conteudo/<int:id>")
def conteudo(id):
    banner = next((b for b in banners if b["id"] == id), None)
    if not banner:
        abort(404)

    return render_template("conteudo.html", banner=banner)

# ===============================
# 🔹 EXECUÇÃO
# ===============================

def main():
    app.run(port=int(os.environ.get("PORT", 5006)), debug=True)

if __name__ == "__main__":
    main()