from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "segredo"

# LOGIN DO DONO
USUARIO = "isabele@gmail.com"
SENHA = "1234"

# LOGIN DO ADMIN
USUARIO2 = "isa@gmail.com"
SENHA2 = "1234"

# Banco de dados simples em memória
pedidos = []
contador_id = 1

garcons = {}
cozinheiros = {}

# Agora clientes é um dicionário!
# exemplo: clientes["email@x.com"] = {"nome": "Fulano", "senha": "123"}
clientes = {}

@app.route("/")
def inicio():
    return render_template("inicio.html")


# -------------------------------------
# LOGIN + CADASTRO DE CLIENTE NA MESMA TELA
# -------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    erro = ""

    if request.method == "POST":

        # CADASTRAR CLIENTE
        if request.form.get("acao") == "cadastrar":
            nome = request.form.get("novo_nome")
            email = request.form.get("novo_usuario")
            senha = request.form.get("nova_senha")

            if email in clientes:
                erro = "Este email já está cadastrado!"
            else:
                clientes[email] = {"nome": nome, "senha": senha}
                flash("Cadastro realizado! Agora faça login.", "success")
                return redirect(url_for("login"))

        # LOGIN NORMAL
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

       

        # Admin
        if usuario == USUARIO2 and senha == SENHA2:
            return redirect(url_for("admin"))

        # Garçom
        if usuario in garcons and senha == garcons[usuario]["senha"]:
            return redirect(url_for("garcom"))

        # Cozinheiro
        if usuario in cozinheiros and senha == cozinheiros[usuario]["senha"]:
            return redirect(url_for("cozinha"))

        # Cliente
        if usuario in clientes and senha == clientes[usuario]["senha"]:
            return redirect(url_for("menu"))

        erro = "Usuário ou senha incorretos."

    return render_template("login.html", erro=erro)


# -------------------------------------
# CADASTRO DE CLIENTE (ROTA OPCIONAL)
# -------------------------------------
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        if email in clientes:
            flash("Este email já está cadastrado!", "warning")
            return redirect(url_for("cadastro"))

        clientes[email] = {"nome": nome, "senha": senha}

        flash("Cadastro concluído! Agora faça login.", "success")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


# -------------------------------------
# ÁREA ADMIN – cria garçom e cozinheiro
# -------------------------------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    erro = ""
    msg = ""

    if request.method == "POST":
        tipo = request.form.get("tipo")
        novo_user = request.form.get("novo_usuario")
        nova_senha = request.form.get("nova_senha")

        if tipo == "garcom":
            if novo_user in garcons:
                erro = "Garçom já existe!"
            else:
                garcons[novo_user] = {"senha": nova_senha}
                msg = f"Garçom {novo_user} criado!"

        elif tipo == "cozinheiro":
            if novo_user in cozinheiros:
                erro = "Cozinheiro já existe!"
            else:
                cozinheiros[novo_user] = {"senha": nova_senha}
                msg = f"Cozinheiro {novo_user} criado!"

    return render_template(
        "admin.html",
        erro=erro,
        msg=msg,
        garcons=garcons,
        cozinheiros=cozinheiros
    )


# -------------------------------------
# GARÇOM – envia pedidos
# -------------------------------------
@app.route("/garcom", methods=["GET", "POST"])
def garcom():
    global contador_id
    msg = ""

    if request.method == "POST":
        mesa = request.form.get("mesa")
        item = request.form.get("item")

        novo_pedido = {
            "id": contador_id,
            "mesa": mesa,
            "item": item,
            "status": "pendente"
        }

        pedidos.append(novo_pedido)
        contador_id += 1
        msg = "Pedido enviado!"

    concluidos = [p for p in pedidos if p["status"] == "concluido"]

    return render_template("garcom.html", msg=msg, concluidos=concluidos)


# -------------------------------------
# COZINHA – conclui pedidos
# -------------------------------------
@app.route("/cozinha", methods=["GET", "POST"])
def cozinha():
    if request.method == "POST":
        id_pedido = int(request.form.get("id_pedido"))

        for p in pedidos:
            if p["id"] == id_pedido:
                p["status"] = "concluido"

    pendentes = [p for p in pedidos if p["status"] == "pendente"]

    return render_template("cozinha.html", pendentes=pendentes)


@app.route("/menu")
def menu():
    return render_template("menu.html")


# -------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
