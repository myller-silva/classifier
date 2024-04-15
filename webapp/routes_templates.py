from flask import jsonify, render_template, request
import requests
from app import app
from utils import get_models_dataframe

base_url: str = "http://localhost:5000"
base_url_api: str = f"{base_url}/api"

# modelos_chagas = get_models_dataframe("chagas", ".pkl")
modelos_digits = get_models_dataframe("digits", ".h5")

# TODO: definir rotas do navbar fora no arquivo de rotas


@app.route("/")
def index():
    return render_template("home.html", modelos=modelos_digits)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/classify/digits", methods=["GET"])
def get_classify_digits():
    modelos = modelos_digits
    return render_template("classify/digits.html", modelos=modelos)


# TODO: modificar request, usar o test_client
@app.route("/classify/digits", methods=["POST"])
def post_classify_digits():
    if "csvFile" not in request.files:
        return jsonify({"Erro": "Arquivo não enviado"}), 404
    
    if "model" not in request.form:
        return jsonify({"Erro": "Modelo não enviado"}), 404
    selected_model = request.form["model"]
    
    response = requests.post(
        f"{base_url_api}/classify/digits",
        data={"model": selected_model},
        files=request.files,
    )

    if response.status_code != 200:
        return (jsonify({"Erro": f"{response.text}"}), response.status_code)

    response_json = response.json()
    return render_template(
        "result/digits.html",
        model=selected_model,
        imagens=response_json["imagens"],
        targets=response_json["targets"],
        network_outputs=response_json["network_outputs"],
    )
