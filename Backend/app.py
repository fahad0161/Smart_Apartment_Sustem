from flask import Flask, request, jsonify, g
from flask_cors import CORS
from functools import wraps
import models
from config import Config
import traceback

app = Flask(__name__)
CORS(app)

# ============================================
# Authentication Decorator
# ============================================


def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Authentication required'}), 401

        session = models.Session.get_by_token(token)
        if not session:
            return jsonify({'error': 'Invalid or expired session'}), 401

        g.current_user = session
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.current_user['role'] not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============================================
# Error Handlers
# ============================================


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

# ============================================
# Health Check
# ============================================


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Smart Apartment System API is running'})

# ============================================
# Authentication Routes
# ============================================


@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()

        required_fields = ['username', 'password', 'email', 'full_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        user_id = models.User.create(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            full_name=data['full_name'],
            phone=data.get('phone', ''),
            role=data.get('role', 'tenant'),
            apartment_id=data.get('apartment_id')
        )

        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id
        }), 201

    except Exception as e:
        if 'Duplicate entry' in str(e):
            return jsonify({'error': 'Username or email already exists'}), 400
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()

        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password required'}), 400

        user = models.User.authenticate(data['username'], data['password'])

        if not user:
            return jsonify({'error': 'Invalid username or password'}), 401

        token = models.Session.create(
            user_id=user['id'],
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )

        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'role': user['role'],
                'apartment_id': user['apartment_id']
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """User logout"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        models.Session.delete(token)
        return jsonify({'message': 'Logged out successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current user information"""
    try:
        user = models.User.get_by_id(g.current_user['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'phone': user['phone'],
                'role': user['role'],
                'apartment_id': user['apartment_id']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# User Management Routes
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

# ============================================
# Apartment Management Routes
# ============================================


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

# ============================================
# Bill Management Routes
# ============================================


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

# ============================================
# Visitor Management Routes
# ============================================


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

# ============================================
# Service Request Routes
# ============================================


@app.route('/api/service-requests', methods=['GET'])
@login_required
def get_service_requests():
    """Get all service requests"""
    try:
        status = request.args.get('status')
        priority = request.args.get('priority')
        request_type = request.args.get('type')
        user_id = request.args.get('user_id', type=int)

        # If user is tenant, only show their requests
        if g.current_user['role'] == 'tenant':
            user_id = g.current_user['user_id']

        requests = models.ServiceRequest.get_all(
            status=status,
            priority=priority,
            request_type=request_type,
            user_id=user_id
        )
        return jsonify({'requests': requests})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/service-requests/<int:request_id>', methods=['GET'])
@login_required
def get_service_request(request_id):
    """Get a specific service request"""
    try:
        service_request = models.ServiceRequest.get_by_id(request_id)
        if not service_request:
            return jsonify({'error': 'Service request not found'}), 404
        return jsonify({'request': service_request})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/service-requests', methods=['POST'])
@login_required
def create_service_request():
    """Create a new service request"""
    try:
        data = request.get_json()

        required_fields = ['apartment_id', 'request_type', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # If user is tenant, use their apartment and user_id
        user_id = g.current_user['user_id']
        apartment_id = data['apartment_id']

        if g.current_user['role'] == 'tenant':
            user_id = g.current_user['user_id']
            if not apartment_id:
                apartment_id = g.current_user['apartment_id']

        request_id = models.ServiceRequest.create(
            user_id=user_id,
            apartment_id=apartment_id,
            request_type=data['request_type'],
            description=data['description'],
            priority=data.get('priority', 'medium'),
            scheduled_date=data.get('scheduled_date')
        )

        models.ActivityLog.log(
            g.current_user['user_id'],
            'CREATE',
            'service_request',
            request_id,
            f'Created {data["request_type"]} service request'
        )

        return jsonify({
            'message': 'Service request created successfully',
            'request_id': request_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/service-requests/<int:request_id>', methods=['PUT'])
@login_required
def update_service_request(request_id):
    """Update a service request"""
    try:
        data = request.get_json()

        # Only admin can update other users' requests
        service_request = models.ServiceRequest.get_by_id(request_id)
        if not service_request:
            return jsonify({'error': 'Service request not found'}), 404

        if g.current_user['role'] != 'admin' and service_request['user_id'] != g.current_user['user_id']:
            return jsonify({'error': 'Not authorized to update this request'}), 403

        # Only admin can assign requests
        if 'assigned_to' in data and g.current_user['role'] != 'admin':
            return jsonify({'error': 'Only admin can assign requests'}), 403

        models.ServiceRequest.update(request_id, data)

        models.ActivityLog.log(
            g.current_user['user_id'],
            'UPDATE',
            'service_request',
            request_id,
            f'Updated service request {request_id}'
        )

        return jsonify({'message': 'Service request updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# Dashboard Routes
# ============================================


@app.route('/api/dashboard/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        stats = {
            'apartments': models.Apartment.get_occupancy_stats(),
            'bills': models.Bill.get_billing_stats(),
            'visitors': models.Visitor.get_visitor_stats(),
            'service_requests': models.ServiceRequest.get_request_stats()
        }

        # Get counts
        stats['total_users'] = len(models.User.get_all())
        stats['total_tenants'] = len(models.User.get_all(role='tenant'))
        stats['total_guards'] = len(models.User.get_all(role='security'))

        return jsonify({'stats': stats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/activity-log', methods=['GET'])
@login_required
@role_required('admin')
def get_activity_log():
    """Get recent activity log (Admin only)"""
    try:
        limit = request.args.get('limit', 50, type=int)
        logs = models.ActivityLog.get_recent(limit=limit)
        return jsonify({'logs': logs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# Main Entry Point
# ============================================


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
