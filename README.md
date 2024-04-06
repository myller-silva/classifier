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

## Migração  

1. **Configurar o Flask-Migrate:** Certifique-se de ter o Flask-Migrate instalado em seu ambiente virtual. Você pode instalá-lo usando o pip:

   ```
   pip install Flask-Migrate
   ```

2. **Inicializar o Flask-Migrate:** No arquivo principal da sua aplicação Flask (geralmente `app.py`), inicialize o Flask-Migrate passando sua aplicação Flask e o objeto `db` como argumentos:

   ```python
   from flask import Flask
   from flask_sqlalchemy import SQLAlchemy
   from flask_migrate import Migrate

   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seu_banco_de_dados.db'
   db = SQLAlchemy(app)
   migrate = Migrate(app, db)
   ```

   Certifique-se de importar `Flask`, `SQLAlchemy`, `Migrate` e quaisquer outros objetos necessários.

3. **Criar Migrações Iniciais:** Após definir seus modelos de banco de dados, você precisa criar uma migração inicial. Navegue até o diretório da sua aplicação e execute o seguinte comando:

   ```
   flask db init
   ```

   Isso criará um diretório chamado `migrations` na raiz do seu projeto, onde as migrações de banco de dados serão armazenadas.

4. **Gerar Migrações:** Agora, você pode gerar uma migração inicial para seus modelos de banco de dados. Execute o seguinte comando:

   ```
   flask db migrate -m "Inicialização da base de dados"
   ```

   Isso criará um arquivo de migração com os detalhes dos modelos de banco de dados.

5. **Aplicar Migrações:** Finalmente, você precisa aplicar as migrações ao seu banco de dados. Use o seguinte comando para isso:

   ```
   flask db upgrade
   ```

   Isso aplicará todas as migrações pendentes ao banco de dados, criando as tabelas conforme definido nos modelos.

## Executando a Aplicação

1. Ative o ambiente virtual com um desses comandos:

```bash
.\flask_env\Scripts\activate
```

```bash
flask_env\Scripts\activate
```

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
