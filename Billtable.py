Bill Management Routes


@app.route('/api/bills', methods=['GET'])
@login_required
def get_bills():
    """Get all bills"""
    try:
        status = request.args.get('status')
        bill_type = request.args.get('type')
        user_id = request.args.get('user_id', type=int)

        # If user is tenant, only show their bills
        if g.current_user['role'] == 'tenant':
            user_id = g.current_user['user_id']

        bills = models.Bill.get_all(
            status=status, bill_type=bill_type, user_id=user_id)
        return jsonify({'bills': bills})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/bills/<int:bill_id>', methods=['GET'])
@login_required
def get_bill(bill_id):
    """Get a specific bill"""
    try:
        bill = models.Bill.get_by_id(bill_id)
        if not bill:
            return jsonify({'error': 'Bill not found'}), 404
        return jsonify({'bill': bill})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/bills', methods=['POST'])
@login_required
@role_required('admin')
def create_bill():
    """Create a new bill (Admin only)"""
    try:
        data = request.get_json()

        required_fields = ['user_id', 'apartment_id',
                           'bill_type', 'amount', 'due_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        bill_id = models.Bill.create(
            user_id=data['user_id'],
            apartment_id=data['apartment_id'],
            bill_type=data['bill_type'],
            amount=data['amount'],
            units_used=data.get('units_used'),
            due_date=data['due_date'],
            notes=data.get('notes')
        )

        models.ActivityLog.log(
            g.current_user['user_id'],
            'CREATE',
            'bill',
            bill_id,
            f'Created {data["bill_type"]} bill for user {data["user_id"]}'
        )

        return jsonify({
            'message': 'Bill created successfully',
            'bill_id': bill_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/bills/<int:bill_id>', methods=['PUT'])
@login_required
@role_required('admin')
def update_bill(bill_id):
    """Update a bill"""
    try:
        data = request.get_json()
        models.Bill.update(bill_id, data)

        models.ActivityLog.log(
            g.current_user['user_id'],
            'UPDATE',
            'bill',
            bill_id,
            f'Updated bill {bill_id}'
        )

        return jsonify({'message': 'Bill updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/bills/<int:bill_id>/pay', methods=['POST'])
@login_required
def pay_bill(bill_id):
    """Mark a bill as paid"""
    try:
        data = request.get_json()

        # Only bill owner or admin can pay
        bill = models.Bill.get_by_id(bill_id)
        if not bill:
            return jsonify({'error': 'Bill not found'}), 404

        if g.current_user['role'] != 'admin' and bill['user_id'] != g.current_user['user_id']:
            return jsonify({'error': 'Not authorized to pay this bill'}), 403

        models.Bill.mark_as_paid(
            bill_id,
            payment_method=data.get('payment_method'),
            transaction_id=data.get('transaction_id')
        )

        models.ActivityLog.log(
            g.current_user['user_id'],
            'PAYMENT',
            'bill',
            bill_id,
            f'Payment received for bill {bill_id}'
        )

        return jsonify({'message': 'Bill marked as paid successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/bills/overdue', methods=['GET'])
@login_required
@role_required('admin')
def get_overdue_bills():
    """Get all overdue bills (Admin only)"""
    try:
        bills = models.Bill.get_overdue()
        return jsonify({'bills': bills})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
