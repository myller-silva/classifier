from flask import render_template, request, jsonify
from app import app
from utils import generate_classes_image, get_models_dataframe


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
    models = get_models_dataframe('chagas', extention='.pkl')
    return jsonify(models)

@app.route('/chagas', methods=['POST'])
def classificar_chagas():

    data = request.get_json()
    model = pickle.load('utils/chagas/model.pkl')
    return 'model carregado com sucesso'
    
    # Classificar a instância do dataset
    classificacao = model.predict(data['instancia'])
    pass


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
        imagens, targets, network_outputs = generate_classes_image(csv_file, selected_model) 
        return render_template('result.html', model=selected_model, imagens=imagens, network_outputs=network_outputs, targets=targets)
    
    if request.method == 'GET':
        modelos = get_models_dataframe('digits')
        return render_template('classify.html', modelos=modelos)
    
    return "Erro", 404
