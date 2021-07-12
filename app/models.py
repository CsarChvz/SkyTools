from enum import unique
from operator import index
from re import S, T
import re
from flask.globals import request
from sqlalchemy.orm import backref, defaultload
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db
from datetime import datetime, timezone
import hashlib
from markdown import markdown
import bleach

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    image_profile = db.Column(db.String(20), unique=False, default='default.jpg')
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    avatar_hash = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            #Se guarda el hash en el espacio del usuario, esto con la funcion que devuelve el hash
            self.avatar_hash = self.gravatar_hash()
            db.session.commit()
    
    #Funciono para hacer el hash con el email para el avatar
    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()


    #Funcion para genera avatar

    def gravatar(self, size=100, default='identicon', rating='g'):
        """
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        """
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash() 
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)
    #Se hace un atributo en el cual se guarda la clave en cadena sencilla
    
    #Si se intenta leer no se va a poder porque va a dar un error
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    #Entonces cuando se establece o se pone un valor en el atributo, se da la siguiente funcion
    @password.setter
    #La funcion con el mismo nombre del metodo, pero con la unica diferencia de que el parametro "password" es un atributo
    #Entonces cuando se sobreescribe el atributo, este sobreescribe otro atributo que sería el password_hash y lo que mete ahi es la contraseña de hash
    #que sería el atributo password que se genera un hash
    def password(self, password):
        #Guarda en su espacio/variable el hash del atributo password
        self.password_hash = generate_password_hash(password)

    #Este metodo lo que hace es tomar  la palabra para verificar si es la misma, si son iguales los hash entonces es correcto
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Tool(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    link = db.Column(db.String(220), unique=False, nullable=False)
    category = db.Column(db.String(30), unique=False, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    image_tool = db.Column(db.String(20), unique=False, nullable=False)
    tool = db.relationship('UserTool', backref='user_tool')
    image_preview = db.Column(db.String(20), unique=False, nullable=False)
    descripcion = db.Column(db.String(1000), unique=False, nullable=False)
    type_tool = db.Column(db.String(20), unique=False, nullable=False)


class UserTool(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'))

class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20), unique=True, nullable=False)
    image_category = db.Column(db.String(30), unique=False, nullable=True)
    type_category_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    url_for_category = db.Column(db.String(30), unique=True, nullable=True)
    category_id = db.relationship('Tool', backref='category_name')

class Type(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name_type = db.Column(db.String(30), unique=True, nullable=False)
    type_ca = db.relationship('Category', backref='type_ca')