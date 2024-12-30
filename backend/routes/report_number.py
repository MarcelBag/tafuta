from flask import Blueprint, request, jsonify
from models.database import SessionLocal
from models.number import Number

report_number_bp = Blueprint('report_number', __name__)
db = SessionLocal()

@report_number_bp.route('/report', methods=['POST'])
def report_number():
    try:
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
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_number_bp.route('/report', methods=['GET'])
def get_reported_numbers():
    try:
        # Get query parameters
        phone_number = request.args.get('phone_number')  # Filter by phone number
        sort_by = request.args.get('sort_by', 'reports')  # Sort by field (default: reports)
        sort_order = request.args.get('sort_order', 'desc')  # Sort order (asc or desc)
        page = int(request.args.get('page', 1))  # Pagination: page number
        per_page = int(request.args.get('per_page', 10))  # Pagination: items per page

        # Query the database
        query = db.query(Number)

        # Apply filtering
        if phone_number:
            query = query.filter(Number.phone_number.like(f"%{phone_number}%"))

        # Apply sorting
        if sort_by == 'reports':
            sort_column = Number.reports
        elif sort_by == 'phone_number':
            sort_column = Number.phone_number
        else:
            sort_column = Number.reports  # Default to reports

        if sort_order == 'asc':
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # Apply pagination
        total_items = query.count()
        numbers = query.offset((page - 1) * per_page).limit(per_page).all()

        # Format the response
        result = {
            "total_items": total_items,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_items + per_page - 1) // per_page,
            "data": [
                {"phone_number": num.phone_number, "reports": num.reports}
                for num in numbers
            ],
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
