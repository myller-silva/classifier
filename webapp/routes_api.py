from flask import jsonify, request
import numpy as np
from app import app
from utils import (
    generate_images,
    get_model_with_extension,
    generate_classes_image,
    get_models_dataframe,
)

modelos_chagas = get_models_dataframe("chagas", extension=".pkl")
modelos_digits = get_models_dataframe("digits", extension=".h5")


@app.route("/models/chagas", methods=["GET"])
def get_models_chagas():
    return jsonify(modelos_chagas)


def classificar_instancia(model_pkl, instance):
    # todo: fazer uma funcao para conferir se está na ordem correta
    values_list = np.array(list(instance.values()))
    values_list = values_list[:-1]
    values_list = values_list.reshape(1, -1)
    predict = model_pkl.predict(values_list)
    predict_proba = model_pkl.predict_proba(values_list)
    return predict, predict_proba


@app.route("/chagas", methods=["POST"])
def post_classificar_chagas():
    data = request.get_json()
    if data and "model" in data and "instancia" in data:
        model: str = data["model"]
        instance = data["instancia"]

        model_pkl = get_model_with_extension(
            dataframe_path="chagas", file=model, extension=".pkl"
        )
        if not model_pkl:
            return jsonify({"Erro": f"Modelo {model} não encontrado."}), 404

        predict, predict_proba = classificar_instancia(model_pkl, instance)

        return jsonify(
            {"predict": predict.tolist(), "predict_proba": predict_proba.tolist()}
        )
    else:
        return jsonify({"error": "Parâmetros inválidos"}), 400


@app.route("/models/digits", methods=["GET"])
def get_models_digits():
    return jsonify(modelos_digits)


@app.route("/digits", methods=["POST"])
def post_classificar_digits():

    data = request.get_json()
    csv_file = data["csvFile"]
    selected_model = data["model"]
    imagens, targets, network_outputs = generate_classes_image(
        "utils/modelos/digits", csv_file, selected_model
    )
    return jsonify(
        {
            "model": selected_model,
            "imagens": imagens,
            "network_outputs": network_outputs,
            "targets": targets,
        }
    )


@app.route("/csv_to_imagens", methods=["POST"])
def post_generate_images():
    # TODO: pegar o formato da imagem / matriz_size = (8, 8)
    if "csvFile" not in request.files:
        return jsonify({"Erro": "Arquivo não enviado"}), 404
    csv_file = request.files["csvFile"]
    return jsonify(generate_images(csv_file))
