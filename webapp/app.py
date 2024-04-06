import numpy as np
import matplotlib.pyplot as plt

from flask import Flask, render_template, request
from io import BytesIO
import base64

app = Flask(__name__)


def plot_matrix(matrix_str):
    matrix = np.array(eval(matrix_str))
    plt.imshow(matrix, cmap='gray')  # Usando o mapa de cores 'gray'
    plt.axis('off')  # Removendo os eixos
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/plot_matrix', methods=['GET', 'POST'])
def plot():
    if request.method == 'POST':
        matrix_str = request.form['matrix']
        image_base64 = plot_matrix(matrix_str)
        return f'<img src="data:image/png;base64,{image_base64}" alt="Matrix Plot">'
    else:
        return render_template('plot_matrix.html')


if __name__ == '__main__':
    app.run(debug=True)
