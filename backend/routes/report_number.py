from flask import Blueprint, request, jsonify
from models.database import SessionLocal
from models.number import Number

report_number_bp = Blueprint('report_number', __name__)
db = SessionLocal()

@report_number_bp.route('/report', methods=['POST'])
def report_number():
    data = request.json
    phone_number = data.get('phone_number')
    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    # Check if the number already exists
    number = db.query(Number).filter_by(phone_number=phone_number).first()
    if not number:
        number = Number(phone_number=phone_number, reports=1)
        db.add(number)
    else:
        number.reports += 1
    db.commit()
    return jsonify({"status": "success", "phone_number": phone_number, "reports": number.reports})

@report_number_bp.route('/report', methods=['GET'])
def get_reported_numbers():
    numbers = db.query(Number).all()
    result = [{"phone_number": num.phone_number, "reports": num.reports} for num in numbers]
    return jsonify(result)
