from flask import render_template, request, jsonify
from app import app
from utils import generate_classes, get_models


@app.route('/')
def index():
    modelos = get_models()
    return render_template('home.html', modelos=modelos)

 
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
        return render_template('result.html', model=selected_model, imagens=imagens, network_outputs=network_outputs, targets=targets)
    
    if request.method == 'GET':
        modelos = get_models()
        return render_template('classify.html', modelos=modelos)
    
    return "Erro", 404
