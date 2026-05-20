User Management Routes
# ============================================


@app.route('/api/users', methods=['GET'])
@login_required
@role_required('admin')
def get_users():
    """Get all users (Admin only)"""
    try:
        role = request.args.get('role')
        users = models.User.get_all(role=role)
        return jsonify({'users': users})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users', methods=['POST'])
@login_required
@role_required('admin')
def create_user():
    """Create a new user (Admin only)"""
    try:
        data = request.get_json() or {}

        required_fields = ['username', 'email', 'full_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400

        password = data.get('password') or 'password123'

        user_id = models.User.create(
            username=data['username'],
            password=password,
            email=data['email'],
            full_name=data['full_name'],
            phone=data.get('phone', ''),
            role=data.get('role', 'tenant'),
            apartment_id=data.get('apartment_id')
        )

        models.ActivityLog.log(
            g.current_user['user_id'],
            'CREATE',
            'user',
            user_id,
            f'Created user {data["username"]}'
        )

        return jsonify({
            'message': 'User created successfully',
            'user_id': user_id
        }), 201

    except Exception as e:
        if 'Duplicate entry' in str(e):
            return jsonify({'error': 'Username or email already exists'}), 400
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['GET'])
@login_required
@role_required('admin')
def get_user(user_id):
    """Get a specific user"""
    try:
        user = models.User.get_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'user': user})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['PUT'])
@login_required
@role_required('admin')
def update_user(user_id):
    """Update a user"""
    try:
        data = request.get_json()
        models.User.update(user_id, data)
        models.ActivityLog.log(
            g.current_user['user_id'],
            'UPDATE',
            'user',
            user_id,
            f'Updated user {user_id}'
        )
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_user(user_id):
    """Delete a user (soft delete)"""
    try:
        models.User.delete(user_id)
        models.ActivityLog.log(
            g.current_user['user_id'],
            'DELETE',
            'user',
            user_id,
            f'Deleted user {user_id}'
        )
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
