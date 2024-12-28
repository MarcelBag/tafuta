from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Tafuta API!"})

if __name__ == "__main__":
    app.run(debug=True)

from routes.track_number import track_number_bp

app.register_blueprint(track_number_bp)

from models.database import engine, Base

# Initialize tables
Base.metadata.create_all(bind=engine)

from routes.report_number import report_number_bp

app.register_blueprint(report_number_bp)

