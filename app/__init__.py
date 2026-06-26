from flask import Flask
from app.config import Config
from app.extensions import db, bcrypt, jwt, migrate, cache
import logging
from flasgger import Swagger

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Music Recommender API",
        "description": "API documentation for Music Recommender",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter: Bearer <your_token>"
        }
    }
}

# define application factory 
def create_app(config_class=Config):
    app=Flask(__name__)
    swagger=Swagger(app, template=swagger_template)

    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app,db)
    cache.init_app(app)
    

    from app.auth.routes import auth
    from app.songs.routes import songs
    from app.playlist.routes import playlist
    from app.handlers.errors import error
    from app.handlers import jwt_handlers    
        
    app.register_blueprint(auth)
    app.register_blueprint(songs)
    app.register_blueprint(playlist)
    app.register_blueprint(error)
    
    return app