from flask import Flask, jsonify
from routes.track_number import track_number_bp
from routes.report_number import report_number_bp
from models.database import engine, Base
from flask_cors import CORS

app = Flask(__name__)

# Register blueprints
app.register_blueprint(track_number_bp)
app.register_blueprint(report_number_bp)
app = Flask (__name__)

# Initialize tables
Base.metadata.create_all(bind=engine)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Tafuta API!"})

if __name__ == "__main__":
    print("Starting Flask app...")  # Log to confirm script is executing
    app.run(debug=True)
CORS(app)