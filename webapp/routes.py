from flask import render_template, request, jsonify
from app import app
from utils import generate_classes, get_models, generate_explanations
import cplex


@app.route('/')
def index():
    modelos = get_models()
    return render_template('home.html', modelos=modelos)


# # Função para carregar o modelo LP
# def get_model_lp_from_file(lp_file):
#     # Crie uma instância do objeto CPLEX
#     modelo_lp = cplex.Cplex()
 
#     modelo_lp.read(lp_file)

#     return modelo_lp


# # Rota para carregar o modelo MILP
# import os
# @app.route('/load_model')
# def load_model():
#     # Caminho para o arquivo LP
#     lp_file_path = os.path.join(app.root_path, 'utils/modelos/digits/model_4layers_20neurons.h5/original.lp')

#     # Carregar o modelo LP
#     modelo_lp = get_model_lp_from_file(lp_file_path)

#     # Obter informações relevantes sobre o modelo
#     variaveis = modelo_lp.variables.get_names()
#     # Outras informações sobre o modelo podem ser obtidas da mesma forma

#     # Retornar informações sobre o modelo
#     return jsonify({"variaveis": variaveis})

    
@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/explain', methods=['GET', 'POST'])
def explain():
    modelos = get_models()
    
    if request.method == 'POST':
        if 'csvFile' not in request.files:
            return render_template('explain.html', error="Nenhum arquivo CSV enviado")
        
        return render_template('explain.html', modelos=modelos)
        # csv_file = request.files['csvFile']
        # selected_model = request.form['model']
        
        # variaveis = generate_explanations(csv_file, selected_model)
        # return str(variaveis)
        # imagens, targets, network_outputs = generate_classes(csv_file, selected_model) 
        # return render_template('result.html', imagens=imagens, network_outputs=network_outputs, targets=targets)
        
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
        imagens, targets, network_outputs = generate_classes(csv_file, selected_model) 
        return render_template('result.html', imagens=imagens, network_outputs=network_outputs, targets=targets)
    
    if request.method == 'GET':
        modelos = get_models()
        return render_template('classify.html', modelos=modelos)
    
    return "Erro", 404
