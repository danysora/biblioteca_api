from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    libros = db.relationship('Libro', backref='autor', lazy=True)

class Libro(db.Model):
    __tablename__ = 'libros'  

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    fecha_publicacion = db.Column(db.Date)
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'), nullable=False)
    paginas = db.Column(db.Integer)

    autor = db.relationship('Autor', backref='libros')

#Para ejecutar una migracion se usa este comando flask db migrate -m "aqui va un mensaje sobre la migracion"

#Ejemplo:
#Primero se agregan los campos a cambiar en la clase, como una columna de paginas a un libro
#flask db migrate -m "Agregar columna paginas a libro"
#Despues flask db upgrade y listo