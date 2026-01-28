import os
from flask import Flask, render_template, abort, request, session, redirect, url_for, flash
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from google.cloud import firestore
import traceback

load_dotenv() 

import firebase_admin
from firebase_admin import credentials, firestore




cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
firebase_admin.initialize_app(cred)
db = firestore.client()

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
    if session.get("usuario_logado"):
        flash("Você já está logado.", "info")
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        print("📧 Email digitado:", repr(email))
        print("🔑 Senha digitada:", repr(senha))

        usuarios_ref = (
            db.collection("user")
            .where("email", "==", email)
            .limit(1)
        )

        usuario = None
        for u in usuarios_ref.stream():
            usuario = u.to_dict()
            usuario["id"] = u.id

        print("👤 Usuário encontrado:", usuario)

        if not usuario:
            flash("Usuário não encontrado.", "error")
            return render_template("login.html")

        senha_bd = str(usuario.get("password", "")).strip()

        print("🔐 Senha no Firestore:", repr(senha_bd))
        print("⌨️ Senha digitada:", repr(senha))

        if senha_bd != senha:
            flash("Senha incorreta.", "error")
            return render_template("login.html")

        # ✅ LOGIN OK
        session["usuario_logado"] = True
        session["usuario_id"] = usuario["id"]
        session["usuario_nome"] = usuario.get("name", "")
        session["usuario_role"] = usuario.get("role", "user")

        print("✅ Login OK | Role:", session["usuario_role"])

        if session["usuario_role"] == "admin":
            return redirect(url_for("admin"))

        destino = session.pop("destino_pos_login", None)
        if destino:
            return redirect(destino)

        return redirect(url_for("index"))

    return render_template("login.html")



@app.route("/admin")
def admin():
    if not session.get("usuario_logado"):
        return redirect(url_for("login"))

    if session.get("usuario_role") != "admin":
        abort(403)  # acesso negado

    return render_template("admin.html")



# ===============================
# 🔹 LOGOUT
# ===============================

@app.route("/logout")
def logout():
    session.pop("usuario_logado", None)
    return redirect(url_for("index"))



@app.route("/desabafo")
def desabafo():
    if not session.get("usuario_logado"):
        return redirect(url_for("login"))

    return render_template("desabafo.html")


# ===============================
# 🔹 DESABAFO (PROTEGIDO)
# ===============================

@app.route("/enviar_desabafo", methods=["GET", "POST"])
def enviar_desabafo():
    if not session.get("usuario_logado"):
        session["destino_pos_login"] = url_for("desabafo")
        return redirect(url_for("login"))

    if request.method == "POST":
        data = request.get_json()

        mensagem = data.get("mensagem", "").strip()
        anonimo = data.get("anonimo", False)
        nome = data.get("nome", "").strip()

        if not mensagem:
            return {"erro": "Mensagem vazia"}, 400

        autor = "Anônimo" if anonimo or not nome else nome

        db.collection("desabafos").add({
            "usuario_id": session["usuario_id"],
            "autor": autor,
            "mensagem": mensagem,
            "anonimo": anonimo,
            "apagado": False,
            "criado_em": firestore.SERVER_TIMESTAMP
        })

        return {"sucesso": True}, 200

    return render_template("desabafo.html")


# ===============================
# 🔹 historicode desabafos
# ===============================

@app.route("/meus_desabafos")
def meus_desabafos():

    if not session.get("usuario_logado"):
        flash("Faça login para acessar seus desabafos.", "warning")
        session["destino_pos_login"] = url_for("meus_desabafos")
        return redirect(url_for("login"))

    usuario_id = session["usuario_id"]

    docs = (
    db.collection("desabafos")
    .where("usuario_id", "==", usuario_id)
    .where("apagado", "==", False)
    .order_by("criado_em", direction=firestore.Query.DESCENDING)
    .stream()
)


    desabafos = []
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        desabafos.append(d)

    return render_template("meus_desabafos.html", desabafos=desabafos)





# ===============================
# 🔹 excluir
# ===============================

@app.route("/desabafo/excluir/<id>")
def excluir_desabafo(id):
    if not session.get("usuario_logado"):
        return redirect(url_for("login"))

    doc_ref = db.collection("desabafos").document(id)
    doc = doc_ref.get()

    if not doc.exists:
        flash("Desabafo não encontrado.", "error")
        return redirect(url_for("meus_desabafos"))

    desabafo = doc.to_dict()

    # 🔒 segurança: só o dono pode excluir
    if desabafo["user_id"] != session["usuario_id"]:
        flash("Acesso negado.", "error")
        return redirect(url_for("index"))

    doc_ref.delete()
    flash("Desabafo excluído.", "success")

    return redirect(url_for("meus_desabafos"))


# ===============================
# 🔹 publico
# ===============================
@app.route("/desabafos-publicos")
def desabafos_publicos():
    desabafos = []

    docs = (
        db.collection("desabafos")
        .where("publico", "==", True)
        .order_by("data", direction=firestore.Query.DESCENDING)
        .stream()
    )

    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        desabafos.append(d)

    return render_template("desabafos_publicos.html", desabafos=desabafos)



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


def somente_admin():
    return (
        session.get("usuario_logado") is True
        and session.get("usuario_role") == "admin"
    )

@app.route("/admin/usuarios")
def admin_usuarios():
    if session.get("usuario_role") != "admin":
        flash("Acesso negado.", "error")
        return redirect(url_for("index"))

    usuarios = []
    docs = db.collection("user").stream()

    for doc in docs:
        u = doc.to_dict()
        u["id"] = doc.id
        usuarios.append(u)

    return render_template("admin_usuarios.html", usuarios=usuarios)



@app.route("/admin/usuarios/criar", methods=["POST"])
def admin_criar_usuario():
    if not somente_admin():
        flash("Acesso negado.", "error")
        return redirect(url_for("index"))

    nome = request.form.get("name")
    email = request.form.get("email")
    senha = request.form.get("password")
    role = request.form.get("role", "user")

    # 🔒 validação básica
    if not nome or not email or not senha:
        flash("Preencha todos os campos.", "error")
        return redirect(url_for("admin_usuarios"))

    # ❗ evita email duplicado
    existe = db.collection("user").where("email", "==", email).limit(1).get()
    if existe:
        flash("Email já cadastrado.", "error")
        return redirect(url_for("admin_usuarios"))

    db.collection("user").add({
        "name": nome,
        "email": email,
        "password": senha,
        "role": role
    })

    flash("Usuário criado com sucesso!", "success")
    return redirect(url_for("admin_usuarios"))


@app.route("/admin/usuarios/excluir/<id>")
def admin_excluir_usuario(id):
    if not somente_admin():
        flash("Acesso negado.", "error")
        return redirect(url_for("index"))

    # ❌ impede admin se excluir
    if id == session.get("usuario_id"):
        flash("Você não pode excluir seu próprio usuário.", "error")
        return redirect(url_for("admin_usuarios"))

    db.collection("user").document(id).delete()

    flash("Usuário excluído com sucesso.", "success")
    return redirect(url_for("admin_usuarios"))


@app.route("/admin/desabafos")
def admin_desabafos():
    if session.get("usuario_role") != "admin":
        flash("Acesso negado.", "error")
        return redirect(url_for("index"))

    desabafos = []

    docs = (
        db.collection("desabafos")
        .order_by("data", direction=firestore.Query.DESCENDING)
        .stream()
    )
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        desabafos.append(d)
    return render_template("admin_desabafos.html", desabafos=desabafos)


@app.route("/admin/desabafos/excluir/<id>")
def admin_excluir_desabafo(id):
    if session.get("usuario_role") != "admin":
        return redirect(url_for("index"))

    db.collection("desabafos").document(id).delete()
    flash("Desabafo removido.", "success")

    return redirect(url_for("admin_desabafos"))



# ===============================
# 🔹 EXECUÇÃO
# ===============================

def main():
    app.run(port=int(os.environ.get("PORT", 5012)), debug=True)

if __name__ == "__main__":
    main()