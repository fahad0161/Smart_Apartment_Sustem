Apartment Management Routes


@app.route('/api/apartments', methods=['GET'])
@login_required
def get_apartments():
    """Get all apartments"""
    try:
        status = request.args.get('status')
        floor = request.args.get('floor', type=int)
        apartments = models.Apartment.get_all(status=status, floor=floor)
        return jsonify({'apartments': apartments})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/apartments/<int:apartment_id>', methods=['GET'])
@login_required
def get_apartment(apartment_id):
    """Get a specific apartment"""
    try:
        apartment = models.Apartment.get_by_id(apartment_id)
        if not apartment:
            return jsonify({'error': 'Apartment not found'}), 404
        return jsonify({'apartment': apartment})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/apartments', methods=['POST'])
@login_required
@role_required('admin')
def create_apartment():
    """Create a new apartment (Admin only)"""
    try:
        data = request.get_json()

        required_fields = ['unit_number', 'floor',
                           'bedrooms', 'bathrooms', 'area_sqft', 'rent_amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        apartment_id = models.Apartment.create(
            unit_number=data['unit_number'],
            floor=data['floor'],
            bedrooms=data['bedrooms'],
            bathrooms=data['bathrooms'],
            area_sqft=data['area_sqft'],
            rent_amount=data['rent_amount'],
            status=data.get('status', 'vacant'),
            description=data.get('description', '')
        )

        models.ActivityLog.log(
            g.current_user['user_id'],
            'CREATE',
            'apartment',
            apartment_id,
            f'Created apartment {data["unit_number"]}'
        )

        return jsonify({
            'message': 'Apartment created successfully',
            'apartment_id': apartment_id
        }), 201

    except Exception as e:
        if 'Duplicate entry' in str(e):
            return jsonify({'error': 'Apartment unit number already exists'}), 400
        return jsonify({'error': str(e)}), 500


@app.route('/api/apartments/<int:apartment_id>', methods=['PUT'])
@login_required
@role_required('admin')
def update_apartment(apartment_id):
    """Update an apartment"""
    try:
        data = request.get_json()
        models.Apartment.update(apartment_id, data)

        models.ActivityLog.log(
            g.current_user['user_id'],
            'UPDATE',
            'apartment',
            apartment_id,
            f'Updated apartment {apartment_id}'
        )

        return jsonify({'message': 'Apartment updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/apartments/<int:apartment_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_apartment(apartment_id):
    """Delete an apartment"""
    try:
        models.Apartment.delete(apartment_id)

        models.ActivityLog.log(
            g.current_user['user_id'],
            'DELETE',
            'apartment',
            apartment_id,
            f'Deleted apartment {apartment_id}'
        )

        return jsonify({'message': 'Apartment deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
