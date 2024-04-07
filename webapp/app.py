from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

app = Flask(__name__)

#configuracao do banco
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/teste_db' 
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

from routes import *
# from models import *

# with app.app_context():
#     # Isso garante que as operações sejam executadas no contexto da aplicação Flask
#     db.create_all()


if __name__ == '__main__': 
    # Inicia a aplicação Flask 
    app.run(debug=True, host='0.0.0.0')

