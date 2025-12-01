from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Usuário e senha fixos para teste
USUARIO = "isabele@gmail.com"
SENHA = "1234"

USUARIO2 = "isa@gmail.com"
SENHA2 = "1234"

# Lista onde os pedidos serão armazenados
pedidos = []
contador_id = 1

# armazena os logins dos garçons
garcons = {}
# armazena os logins dos cozinheiros
cozinheiros = {}

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = ""
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        # login de usuário
        if usuario == USUARIO and senha == SENHA:
            return redirect(url_for("inicio"))

        # login de admin
        if usuario == USUARIO2 and senha == SENHA2:
            return redirect(url_for("admin"))

        # login de garçom
        if usuario in garcons and senha == garcons[usuario]["senha"]:
            return redirect(url_for("garcom"))
        
        # login de cozinheiro
        if usuario in cozinheiros and senha == cozinheiros[usuario]["senha"]:
          return redirect(url_for("cozinha"))


        # se nada deu certo
        erro = "Usuário ou senha incorretos"

    return render_template("login.html", erro=erro)



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
                erro = "Esse garçom já existe!"
            else:
                garcons[novo_user] = {"senha": nova_senha}
                msg = f"Garçom {novo_user} criado com sucesso!"

        elif tipo == "cozinheiro":
            if novo_user in cozinheiros:
                erro = "Esse cozinheiro já existe!"
            else:
                cozinheiros[novo_user] = {"senha": nova_senha}
                msg = f"Cozinheiro {novo_user} criado com sucesso!"

    return render_template(
        "admin.html",
        erro=erro,
        msg=msg,
        garcons=garcons,
        cozinheiros=cozinheiros
    )



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
        msg = "Pedido enviado para a cozinha!"

    # lista apenas pedidos concluídos para aviso
    concluidos = [p for p in pedidos if p["status"] == "concluido"]

    return render_template("garcom.html", msg=msg, concluidos=concluidos)


@app.route("/cozinha", methods=["GET", "POST"])
def cozinha():
    if request.method == "POST":
        id_pedido = int(request.form.get("id_pedido"))

        # procurar o pedido e atualizar
        for p in pedidos:
            if p["id"] == id_pedido:
                p["status"] = "concluido"

    # lista só pedidos pendentes
    pendentes = [p for p in pedidos if p["status"] == "pendente"]

    return render_template("cozinha.html", pendentes=pendentes)

@app.route("/menu")
def menu():
    return render_template("menu.html")


if __name__ == "__main__":
    app.run(debug=True)
