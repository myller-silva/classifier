from flask import render_template, request, jsonify
from app import app
from utils import generate_classes_image, get_model_with_extension, get_models_dataframe


import pickle
# Carregar o modelo .pkl
# with open('utils/chagas/model.pkl', 'rb') as model_file:
#     model = pickle.load('utils/chagas/model.pkl')



@app.route('/')
def index():
    modelos = get_models_dataframe('digits')
    return render_template('home.html', modelos=modelos)


# Rota para listar todos os modelos do dataset digits
@app.route('/models/digits', methods=['GET'])
def get_models_digits():
    models = get_models_dataframe('digits')
    return jsonify(models)


# Rota para listar todos os modelos do dataset chagas
@app.route('/models/chagas', methods=['GET'])
def get_models_chagas():
    models = get_models_dataframe('chagas', extension='.pkl')
    return jsonify(models)


import numpy as np
@app.route('/chagas', methods=['POST'])
def classificar_chagas():

    data = request.get_json() 
    if data and 'model' in data:
        model:str = data['model']    
        model_pkl = get_model_with_extension(
            dataframe_path='chagas',
            file='model',
            extension='.pkl')
        
        instance = data['instancia']
        # todo: conferir se está na ordem correta
        values_list = np.array(list(instance.values()))
        values_list = values_list[:-1]
        values_list = values_list.reshape(1, -1)
        predict = model_pkl.predict(values_list)
        predict_proba = model_pkl.predict_proba(values_list)
        
        print(type(predict_proba), predict_proba)
        
        return jsonify({
            'predict': predict.tolist(),
            'predict_proba': predict_proba.tolist()
        })

    else:
        return jsonify({'error': 'Dataset name not provided'})



@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/explain', methods=['GET', 'POST'])
def explain():
    modelos = get_models_dataframe('digits')
    
    if request.method == 'POST':
        if 'csvFile' not in request.files:
            return render_template('explain.html', error="Nenhum arquivo CSV enviado")
        
        return render_template('explain.html', modelos=modelos)
        
    if request.method == 'GET':
        return render_template('explain.html', modelos=modelos)
        
    return "Erro", 404


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        if 'csvFile' not in request.files:
            return render_template('classify.html', error="Nenhum arquivo CSV enviado")
        csv_file = request.files['csvFile']
        selected_model = request.form['model']  
        imagens, targets, network_outputs = generate_classes_image('utils/modelos/digits', csv_file, selected_model) 
        return render_template('result.html', model=selected_model, imagens=imagens, network_outputs=network_outputs, targets=targets)
    
    if request.method == 'GET':
        modelos = get_models_dataframe('digits')
        return render_template('classify.html', modelos=modelos)
    
    return "Erro", 404
