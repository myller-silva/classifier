# Aplicação de Predição de Dígitos Manuscritos

Esta aplicação Flask foi desenvolvida para receber imagens de dígitos manuscritos, fazer a predição desses dígitos usando um modelo de aprendizado de máquina treinado e retornar os resultados da predição.

## Tecnologias Utilizadas

- Python
- Flask
- scikit-learn
- HTML
- CSS
- JavaScript

## Pré-requisitos

- Python 3.x
- Pacotes Python listados em `requirements.txt`
- Um modelo treinado para a predição de dígitos manuscritos

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu_usuario/sua_aplicacao.git
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd sua_aplicacao
   ```

3. Instale os pacotes Python necessários:

   ```bash
   pip install -r requirements.txt
   ```

4. Coloque seu modelo treinado (por exemplo, um modelo de regressão logística, SVM, etc.) na pasta `models/`.

## Executando a Aplicação

1. Execute o seguinte comando para iniciar o servidor Flask:

   ```bash
   python app.py
   ```

2. Acesse a aplicação em seu navegador usando o endereço:

   `
   http://localhost:5000
   `

## Como Usar

1. Na página inicial, você verá um formulário para carregar uma imagem contendo um dígito manuscrito.

2. Selecione uma imagem e envie o formulário.

3. O modelo fará a predição do dígito na imagem e exibirá o resultado na página.

## Estrutura do Projeto

```plaintext
sua_aplicacao/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models/
│   │   └── seu_modelo_treinado.pkl
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── ...
│
├── templates/
│   ├── index.html
│   └── ...
│
├── app.py
└── requirements.txt
```

- **`app/`:** Contém o código da aplicação Flask.
- **`static/`:** Contém arquivos estáticos como CSS, JavaScript, etc.
- **`templates/`:** Contém os arquivos HTML para renderização das páginas.
- **`app.py`:** Arquivo principal que inicia o servidor Flask.
- **`requirements.txt`:** Lista de pacotes Python necessários.
