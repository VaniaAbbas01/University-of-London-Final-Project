from flask import Flask
from config import Config
from routes.mainRoute import main_bp
from routes.uploadRoute import upload_bp
from routes.analysisRoute import analysis_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(analysis_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
