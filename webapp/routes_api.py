from flask import jsonify, request
import numpy as np
import pandas as pd
from app import app
from utils import (
    generate_images,
    get_network_outputs_digits,
    get_models_dataframe,
)

modelos_digits = get_models_dataframe("digits", extension=".h5")
base_url_api = "/api"


def classificar_instancia(model_pkl, instance):
    # todo: fazer uma funcao para conferir se está na ordem correta
    values_list = np.array(list(instance.values()))
    values_list = values_list[:-1]
    values_list = values_list.reshape(1, -1)
    predict = model_pkl.predict(values_list)
    predict_proba = model_pkl.predict_proba(values_list)
    return predict, predict_proba


@app.route(f"{base_url_api}/models/digits", methods=["GET"])
def get_api_models_digits():
    return jsonify(modelos_digits)


@app.route(f"{base_url_api}/classify/digits", methods=["POST"])
def post_api_classify_digits():

    if "csvFile" not in request.files:
        return jsonify({"Erro": "Arquivo não enviado"}), 404
    if "model" not in request.form:
        return jsonify({"Erro": "Modelo não enviado"}), 404
    
    csv_file = request.files["csvFile"]
    df = pd.read_csv(csv_file)
    
    selected_model = request.form["model"]
    
    network_outputs, targets = get_network_outputs_digits(
        path_model="utils/modelos/digits",
        dataframe=df,
        modelo=selected_model,
    )
    
    imagens = generate_images(df)
    
    return (
        jsonify(
            {
                "imagens": imagens,
                "model": selected_model,
                "network_outputs": network_outputs,
                "targets": targets,
            }
        ),
        200,
    )

