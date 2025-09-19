from email.utils import quote
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')
    sql_sv_pwd = '325040'

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:%s@localhost/parkingdb?charset=utf8mb4" % quote(sql_sv_pwd)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)
    
    return app

app = create_app()
