
@app.route('/api/visitors', methods=['GET'])
@login_required
def get_visitors():
    """Get all visitors"""
    try:
        status = request.args.get('status')
        apartment_id = request.args.get('apartment_id', type=int)
        date = request.args.get('date')

        visitors = models.Visitor.get_all(
            status=status, apartment_id=apartment_id, date=date)
        return jsonify({'visitors': visitors})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/visitors/current', methods=['GET'])
@login_required
def get_current_visitors():
    """Get all visitors currently inside"""
    try:
        visitors = models.Visitor.get_current_visitors()
        return jsonify({'visitors': visitors})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/visitors', methods=['POST'])
@login_required
def register_visitor():
    """Register a new visitor"""
    try:
        data = request.get_json()

        required_fields = ['visitor_name', 'apartment_id', 'purpose']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        visitor_id = models.Visitor.create(
            visitor_name=data['visitor_name'],
            phone=data.get('phone', ''),
            apartment_id=data['apartment_id'],
            purpose=data['purpose'],
            checked_by=g.current_user['user_id'],
            email=data.get('email'),
            visitor_count=data.get('visitor_count', 1),
            notes=data.get('notes')
        )

        models.ActivityLog.log(
            g.current_user['user_id'],
            'CREATE',
            'visitor',
            visitor_id,
            f'Registered visitor {data["visitor_name"]}'
        )

        return jsonify({
            'message': 'Visitor registered successfully',
            'visitor_id': visitor_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/visitors/<int:visitor_id>/exit', methods=['PUT'])
@login_required
def log_visitor_exit(visitor_id):
    """Log visitor exit"""
    try:
        rows = models.Visitor.log_exit(visitor_id)
        if rows == 0:
            return jsonify({'error': 'Visitor not found or already exited'}), 404

        models.ActivityLog.log(
            g.current_user['user_id'],
            'EXIT',
            'visitor',
            visitor_id,
            f'Visitor {visitor_id} exited'
        )

        return jsonify({'message': 'Visitor exit logged successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
