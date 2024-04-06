# routes.py
from flask import render_template, request
from app import app

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'POST':
        selected_model = request.form['model']
        csv_file = request.files['csvFile']
        # Aqui você pode processar o arquivo CSV e realizar a classificação das instâncias usando o modelo selecionado
        # Exemplo de processamento:
        if csv_file:
            # Salvar o arquivo em algum lugar
            csv_file.save('caminho/para/salvar/arquivo.csv')
            # Realizar o processamento e classificação dos dados usando o modelo selecionado
            # Exemplo:
            # results = classificar_instancias(csv_file, selected_model)
            # return render_template('results.html', results=results)
            return 'Arquivo enviado com sucesso e classificado usando o modelo: {}'.format(selected_model)
    if request.method == 'GET':
        return render_template('classify.html')
    

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         csv_file = request.files['csvFile']
#         # Aqui você pode processar o arquivo CSV e realizar a classificação das instâncias
#         # Exemplo de processamento:
#         if csv_file:
#             # Salvar o arquivo em algum lugar
#             csv_file.save('caminho/para/salvar/arquivo.csv')
#             # Realizar o processamento e classificação dos dados
#             # Exemplo:
#             # results = classificar_instancias(csv_file)
#             # return render_template('results.html', results=results)
#             return 'Arquivo enviado com sucesso!'
#     return render_template('upload.html')