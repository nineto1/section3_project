from flask import Flask

def create_app() :
    app = Flask(__name__)
    from flask_app.main import main_bp
    from flask_app.metabase_view import metabase_bp
    from flask_app.model import model_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(metabase_bp, url_prefix='/metabase')
    app.register_blueprint(model_bp, url_prefix='/model')
    return app

if __name__ == '__main__' :
    app = create_app()
    app.run()