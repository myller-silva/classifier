import pandas as pd
from io import BytesIO
import base64
import numpy as np
import os
from app import app
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt


matplotlib.use("Agg")  # Definindo o backend de Matplotlib para não interativo


def generate_base64_digit(column_values):
    image = np.array(column_values).reshape(8, 8)
    plt.figure()
    plt.imshow(image, cmap="gray")
    plt.axis("off")
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight", pad_inches=0)
    buffer.seek(0)
    base64_image = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    return base64_image


def generate_image(row):
    column_values = row[:-1]  # Selecionar todas as colunas exceto a última
    img_base64 = generate_base64_digit(column_values)
    return img_base64


def read_model_keras(path: str, file: str):
    file_path = os.path.join(app.root_path, path, file)
    loaded_model = tf.keras.models.load_model(file_path)
    return loaded_model




def get_network_outputs_digits(path_model: str, dataframe: pd.DataFrame, modelo: str):
    loaded_model = read_model_keras(path=path_model, file=modelo)
    targets, network_outputs = [], []
    for i in range(len(dataframe)):
        target = dataframe.iloc[i][-1]
        targets.append(target)
        network_input = dataframe.iloc[i, :-1]
        network_input = tf.reshape(tf.constant(network_input), (1, -1))
        network_output = loaded_model.predict(network_input, verbose=0)[0]
        network_output = tf.argmax(network_output)
        network_outputs.append(int(network_output))
    return targets, network_outputs


def generate_images(df: pd.DataFrame):
    imagens = []
    dataframe = df
    for i in range(len(dataframe)):
        imagem = generate_image(dataframe.iloc[i])
        imagens.append(imagem)
    return imagens


def get_models_dataframe(dataframe_path, extension=".h5"):
    folder_path = os.path.join(app.root_path, "utils", "modelos", dataframe_path)
    model_files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(extension):
            model_files.append(file_name)
    return model_files


import pickle


def get_model_with_extension(
    dataframe_path: str = "", file: str = "", extension: str = ".pkl"
):
    folder_path = os.path.join(app.root_path, "utils", "modelos", dataframe_path)
    if not file.endswith(extension):
        return None
    model_file = os.path.join(folder_path, file)
    if os.path.exists(model_file):
        with open(model_file, "rb") as f:
            model = pickle.load(f)
        return model
    return None
