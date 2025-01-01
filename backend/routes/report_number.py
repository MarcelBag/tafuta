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
        network_filter = request.args.get('network')  # Filter by network
        sort_by = request.args.get('sort_by', 'reports')  # Sort by field (default: reports)
        sort_order = request.args.get('sort_order', 'desc')  # Sort order (asc or desc)
        page = int(request.args.get('page', 1))  # Pagination: page number
        per_page = int(request.args.get('per_page', 10))  # Pagination: items per page

        # Determine network based on phone number
        def get_network(phone_number):
            if phone_number.startswith(('+2439', '09')):
                return 'Airtel'
            elif phone_number.startswith(('+24385', '+24389', '085', '089')):
                return 'Orange'
            elif phone_number.startswith(('+24381', '081')):
                return 'Vodacom'
            else:
                return 'Unknown'

        # Query the database
        query = db.query(Number)

        # Apply filtering
        if phone_number:
            query = query.filter(Number.phone_number.like(f"%{phone_number}%"))

        if network_filter:
            query = query.filter(
                Number.phone_number.in_(
                    [num.phone_number for num in query if get_network(num.phone_number) == network_filter]
                )
            )

        # Apply sorting
        sort_column = Number.reports if sort_by == 'reports' else Number.phone_number
        query = query.order_by(sort_column.asc() if sort_order == 'asc' else sort_column.desc())

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
                {
                    "phone_number": num.phone_number,
                    "reports": num.reports,
                    "last_location": num.last_location or "Unknown",
                    "places": num.places or "Unknown",
                    "reported_at": num.reported_at.strftime('%Y-%m-%d %H:%M:%S') if num.reported_at else "Unknown",
                    "network": get_network(num.phone_number)
                }
                for num in numbers
            ],
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_number_bp.route('/dashboard-data', methods=['GET'])
def get_dashboard_data():
    try:
        # Query parameters for filtering
        start_date = request.args.get('start_date')  # e.g., 2024-01-01
        end_date = request.args.get('end_date')  # e.g., 2024-12-31
        network_filter = request.args.get('network')  # e.g., Airtel

        query = db.query(Number)

        # Filter by date range
        if start_date:
            query = query.filter(Number.reported_at >= start_date)
        if end_date:
            query = query.filter(Number.reported_at <= end_date)

        # Filter by network
        def get_network(phone_number):
            if phone_number.startswith(('+2439', '09')):
                return 'Airtel'
            elif phone_number.startswith(('+24385', '+24389', '085', '089')):
                return 'Orange'
            elif phone_number.startswith(('+24381', '081')):
                return 'Vodacom'
            else:
                return 'Unknown'

        if network_filter:
            query = query.filter(
                Number.phone_number.in_(
                    [num.phone_number for num in query if get_network(num.phone_number) == network_filter]
                )
            )

        # Aggregate data
        total_reports = query.count()
        network_counts = {"Airtel": 0, "Orange": 0, "Vodacom": 0, "Unknown": 0}
        places_counts = {}

        for record in query.all():
            network = get_network(record.phone_number)
            network_counts[network] += record.reports

            if record.places:
                places_counts[record.places] = places_counts.get(record.places, 0) + record.reports

        return jsonify({
            "total_reports": total_reports,
            "network_counts": network_counts,
            "places_counts": places_counts
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

