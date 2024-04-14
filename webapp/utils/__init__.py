import pandas as pd
from io import BytesIO
import base64
import numpy as np
import os
from app import app
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt


matplotlib.use('Agg')  # Definindo o backend de Matplotlib para não interativo

def generate_base64_digit(column_values): 
    image = np.array(column_values).reshape(8, 8)
    plt.figure() 
    plt.imshow(image, cmap='gray')
    plt.axis('off')  
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
    buffer.seek(0) 
    base64_image = base64.b64encode(buffer.getvalue()).decode()
    plt.close() 
    return base64_image


def generate_image(row):   
    column_values = row[:-1]  # Selecionar todas as colunas exceto a última
    img_base64 = generate_base64_digit(column_values)
    return img_base64


def read_model_keras(path:str, file: str):
    file_path = os.path.join(app.root_path, path, file)
    loaded_model = tf.keras.models.load_model(file_path)
    return loaded_model



# def classificar_instancia(model_pkl, instance):
#     # todo: fazer uma funcao para conferir se está na ordem correta
#     values_list = np.array(list(instance.values()))
#     values_list = values_list[:-1]
#     values_list = values_list.reshape(1, -1)
#     predict = model_pkl.predict(values_list)
#     predict_proba = model_pkl.predict_proba(values_list)
#     return predict, predict_proba


def generate_classes_image(path_model:str, csv_file:str, modelo:str):
    dataframe = pd.read_csv(csv_file)
    # dataframe = pd.DataFrame(csv_file)
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


def generate_images(data_array:list):
    dataframe = pd.read_csv(data_array)
    imagens = []
    for i in range(len(dataframe)): 
        imagem = generate_image(dataframe.iloc[i])
        imagens.append(imagem) 
    return imagens


def get_models_dataframe(dataframe_path, extension = '.h5'): 
    folder_path = os.path.join(app.root_path, 'utils', 'modelos', dataframe_path) 
    model_files = [] 
    for file_name in os.listdir(folder_path): 
        if file_name.endswith(extension): 
            model_files.append(file_name)
    return model_files


import pickle
def get_model_with_extension(dataframe_path:str ='', file:str = '', extension:str = '.pkl'): 
    folder_path = os.path.join(app.root_path, 'utils', 'modelos', dataframe_path)
    
    if not file.endswith(extension): 
        return None
    
    model_file = os.path.join(folder_path, file)
    if os.path.exists(model_file):
        with open(model_file, 'rb') as f:
            model = pickle.load(f)
        return model
    
    return None