from config import DatabaseConfig, Config
import pymysql
import bcrypt
from datetime import datetime, timedelta
import uuid


def _password_matches(plain_password, stored_password):
    """Check a password against either plain text or a bcrypt hash."""
    if stored_password.startswith('$2a$') or stored_password.startswith('$2b$') or stored_password.startswith('$2y$'):
        return bcrypt.checkpw(plain_password.encode('utf-8'), stored_password.encode('utf-8'))
    return plain_password == stored_password


class BaseModel:
    """Base model with common database operations"""
    @staticmethod
    def execute_query(query, params=None, fetch_one=False, fetch_all=True):
        """Execute a query and return results"""
        conn = DatabaseConfig.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                return None
        finally:
            conn.close()

    @staticmethod
    def execute_insert(query, params=None):
        """Execute an insert query and return the last inserted id"""
        conn = DatabaseConfig.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def execute_update(query, params=None):
        """Execute an update query and return affected rows"""
        conn = DatabaseConfig.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount
        finally:
            conn.close()


class User(BaseModel):
    """User model for authentication and management"""

    @staticmethod
    def create(username, password, email, full_name, phone, role='tenant', apartment_id=None):
        """Create a new user"""
        query = """
            INSERT INTO users (username, password, email, full_name, phone, role, apartment_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return User.execute_insert(query, (username, password, email, full_name, phone, role, apartment_id))

    @staticmethod
    def authenticate(username, password):
        """Authenticate a user"""
        query = "SELECT * FROM users WHERE username = %s AND is_active = TRUE"
        user = User.execute_query(query, (username,), fetch_one=True)

        if user and _password_matches(password, user['password']):
            return user
        return None

    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        query = "SELECT id, username, email, full_name, phone, role, apartment_id, created_at FROM users WHERE id = %s"
        return User.execute_query(query, (user_id,), fetch_one=True)

    @staticmethod
    def get_all(role=None, active_only=True):
        """Get all users, optionally filtered by role"""
        if role:
            query = "SELECT id, username, email, full_name, phone, role, apartment_id, is_active, created_at FROM users WHERE role = %s"
            params = (role,)
        else:
            query = "SELECT id, username, email, full_name, phone, role, apartment_id, is_active, created_at FROM users"
            params = None

        if active_only:
            query += " AND is_active = TRUE" if params else " WHERE is_active = TRUE"

        return User.execute_query(query, params, fetch_all=True) if params else User.execute_query(query, fetch_all=True)

    @staticmethod
    def update(user_id, data):
        """Update user information"""
        fields = []
        params = []

        for key, value in data.items():
            if key not in ['id', 'password']:
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return 0

        params.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
        return User.execute_update(query, tuple(params))

    @staticmethod
    def update_password(user_id, new_password):
        """Update user password"""
        query = "UPDATE users SET password = %s WHERE id = %s"
        return User.execute_update(query, (new_password, user_id))

    @staticmethod
    def delete(user_id):
        """Soft delete a user"""
        query = "UPDATE users SET is_active = FALSE WHERE id = %s"
        return User.execute_update(query, (user_id,))


class Session(BaseModel):
    """Session model for authentication management"""

    @staticmethod
    def create(user_id, ip_address=None, user_agent=None):
        """Create a new session"""
        token = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(hours=Config.SESSION_EXPIRY_HOURS)

        query = """
            INSERT INTO sessions (user_id, session_token, ip_address, user_agent, expires_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        Session.execute_insert(
            query, (user_id, token, ip_address, user_agent, expires_at))
        return token

    @staticmethod
    def get_by_token(token):
        """Get session by token"""
        query = """
            SELECT s.*, u.id as user_id, u.username, u.email, u.full_name, u.role, u.apartment_id
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_token = %s AND s.expires_at > NOW()
        """
        return Session.execute_query(query, (token,), fetch_one=True)

    @staticmethod
    def delete(token):
        """Delete a session"""
        query = "DELETE FROM sessions WHERE session_token = %s"
        return Session.execute_update(query, (token,))

    @staticmethod
    def delete_all_for_user(user_id):
        """Delete all sessions for a user"""
        query = "DELETE FROM sessions WHERE user_id = %s"
        return Session.execute_update(query, (user_id,))

    @staticmethod
    def clean_expired():
        """Remove expired sessions"""
        query = "DELETE FROM sessions WHERE expires_at < NOW()"
        Session.execute_update(query)


class Apartment(BaseModel):
    """Apartment model for property management"""

    @staticmethod
    def create(unit_number, floor, bedrooms, bathrooms, area_sqft, rent_amount, status='vacant', description=None):
        """Create a new apartment"""
        query = """
            INSERT INTO apartments (unit_number, floor, bedrooms, bathrooms, area_sqft, rent_amount, status, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        return Apartment.execute_insert(query, (unit_number, floor, bedrooms, bathrooms, area_sqft, rent_amount, status, description))

    @staticmethod
    def get_by_id(apartment_id):
        """Get apartment by ID"""
        query = "SELECT * FROM apartments WHERE id = %s"
        return Apartment.execute_query(query, (apartment_id,), fetch_one=True)

    @staticmethod
    def get_all(status=None, floor=None):
        """Get all apartments with optional filters"""
        conditions = []
        params = []

        if status:
            conditions.append("status = %s")
            params.append(status)
        if floor:
            conditions.append("floor = %s")
            params.append(floor)

        where_clause = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        query = f"SELECT * FROM apartments{where_clause} ORDER BY unit_number"
        return Apartment.execute_query(query, tuple(params) if params else None, fetch_all=True)

    @staticmethod
    def update(apartment_id, data):
        """Update apartment information"""
        fields = []
        params = []

        for key, value in data.items():
            if key != 'id':
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return 0

        params.append(apartment_id)
        query = f"UPDATE apartments SET {', '.join(fields)} WHERE id = %s"
        return Apartment.execute_update(query, tuple(params))

    @staticmethod
    def delete(apartment_id):
        """Delete an apartment"""
        query = "DELETE FROM apartments WHERE id = %s"
        return Apartment.execute_update(query, (apartment_id,))

    @staticmethod
    def get_occupancy_stats():
        """Get occupancy statistics"""
        query = """
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status = 'occupied' THEN 1 ELSE 0 END) as occupied,
                SUM(CASE WHEN status = 'vacant' THEN 1 ELSE 0 END) as vacant
            FROM apartments
        """
        return Apartment.execute_query(query, fetch_one=True)


class Bill(BaseModel):
    """Bill model for billing management"""

    @staticmethod
    def create(user_id, apartment_id, bill_type, amount, units_used=None, due_date=None, notes=None):
        """Create a new bill"""
        if due_date is None:
            due_date = (datetime.now() + timedelta(days=30)
                        ).strftime('%Y-%m-%d')

        query = """
            INSERT INTO bills (user_id, apartment_id, bill_type, amount, units_used, due_date, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return Bill.execute_insert(query, (user_id, apartment_id, bill_type, amount, units_used, due_date, notes))

    @staticmethod
    def get_by_id(bill_id):
        """Get bill by ID"""
        query = "SELECT * FROM bills WHERE id = %s"
        return Bill.execute_query(query, (bill_id,), fetch_one=True)

    @staticmethod
    def get_all(status=None, bill_type=None, user_id=None):
        """Get all bills with optional filters"""
        conditions = []
        params = []

        if status:
            conditions.append("b.status = %s")
            params.append(status)
        if bill_type:
            conditions.append("b.bill_type = %s")
            params.append(bill_type)
        if user_id:
            conditions.append("b.user_id = %s")
            params.append(user_id)

        where_clause = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        query = f"""
            SELECT b.*, u.full_name as tenant_name, a.unit_number
            FROM bills b
            JOIN users u ON b.user_id = u.id
            JOIN apartments a ON b.apartment_id = a.id
            {where_clause}
            ORDER BY b.created_at DESC
        """
        return Bill.execute_query(query, tuple(params) if params else None, fetch_all=True)

    @staticmethod
    def update(bill_id, data):
        """Update bill information"""
        fields = []
        params = []

        for key, value in data.items():
            if key != 'id':
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return 0

        params.append(bill_id)
        query = f"UPDATE bills SET {', '.join(fields)} WHERE id = %s"
        return Bill.execute_update(query, tuple(params))

    @staticmethod
    def mark_as_paid(bill_id, payment_method=None, transaction_id=None):
        """Mark a bill as paid"""
        query = """
            UPDATE bills
            SET status = 'paid', paid_date = CURDATE(), payment_method = %s, transaction_id = %s
            WHERE id = %s
        """
        return Bill.execute_update(query, (payment_method, transaction_id, bill_id))

    @staticmethod
    def get_overdue():
        """Get all overdue bills"""
        query = """
            SELECT b.*, u.full_name as tenant_name, a.unit_number
            FROM bills b
            JOIN users u ON b.user_id = u.id
            JOIN apartments a ON b.apartment_id = a.id
            WHERE b.status = 'pending' AND b.due_date < CURDATE()
            ORDER BY b.due_date
        """
        return Bill.execute_query(query, fetch_all=True)

    @staticmethod
    def get_billing_stats():
        """Get billing statistics"""
        query = """
            SELECT
                COUNT(*) as total_bills,
                SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END) as total_collected,
                SUM(CASE WHEN status = 'pending' THEN amount ELSE 0 END) as total_pending,
                SUM(CASE WHEN status = 'overdue' THEN amount ELSE 0 END) as total_overdue
            FROM bills
        """
        return Bill.execute_query(query, fetch_one=True)


class Visitor(BaseModel):
    """Visitor model for visitor management"""

    @staticmethod
    def create(visitor_name, phone, apartment_id, purpose, checked_by, email=None, visitor_count=1, notes=None):
        """Register a new visitor"""
        query = """
            INSERT INTO visitors (visitor_name, phone, email, apartment_id, purpose, checked_by, visitor_count, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        return Visitor.execute_insert(query, (visitor_name, phone, email, apartment_id, purpose, checked_by, visitor_count, notes))

    @staticmethod
    def get_by_id(visitor_id):
        """Get visitor by ID"""
        query = "SELECT * FROM visitors WHERE id = %s"
        return Visitor.execute_query(query, (visitor_id,), fetch_one=True)

    @staticmethod
    def get_all(status=None, apartment_id=None, date=None):
        """Get all visitors with optional filters"""
        conditions = []
        params = []

        if status:
            conditions.append("v.status = %s")
            params.append(status)
        if apartment_id:
            conditions.append("v.apartment_id = %s")
            params.append(apartment_id)
        if date:
            conditions.append("DATE(v.entry_time) = %s")
            params.append(date)

        where_clause = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        query = f"""
            SELECT v.*, a.unit_number, u.full_name as checked_by_name
            FROM visitors v
            JOIN apartments a ON v.apartment_id = a.id
            JOIN users u ON v.checked_by = u.id
            {where_clause}
            ORDER BY v.entry_time DESC
        """
        return Visitor.execute_query(query, tuple(params) if params else None, fetch_all=True)

    @staticmethod
    def log_exit(visitor_id):
        """Log visitor exit"""
        query = "UPDATE visitors SET exit_time = NOW(), status = 'exited' WHERE id = %s AND status = 'inside'"
        return Visitor.execute_update(query, (visitor_id,))

    @staticmethod
    def get_current_visitors():
        """Get all visitors currently inside"""
        query = """
            SELECT v.*, a.unit_number, u.full_name as checked_by_name
            FROM visitors v
            JOIN apartments a ON v.apartment_id = a.id
            JOIN users u ON v.checked_by = u.id
            WHERE v.status = 'inside'
            ORDER BY v.entry_time DESC
        """
        return Visitor.execute_query(query, fetch_all=True)

    @staticmethod
    def get_visitor_stats():
        """Get visitor statistics"""
        query = """
            SELECT
                COUNT(*) as total_visits,
                SUM(CASE WHEN status = 'inside' THEN 1 ELSE 0 END) as current_visitors,
                SUM(CASE WHEN DATE(entry_time) = CURDATE() THEN 1 ELSE 0 END) as today_visits
            FROM visitors
        """
        return Visitor.execute_query(query, fetch_one=True)


class ServiceRequest(BaseModel):
    """Service Request model for maintenance management"""

    @staticmethod
    def create_request_number():
        """Generate a unique request number"""
        today = datetime.now().strftime('%Y%m%d')
        query = "SELECT COUNT(*) as count FROM service_requests WHERE DATE(created_at) = CURDATE()"
        result = ServiceRequest.execute_query(query, fetch_one=True)
        count = result['count'] + 1 if result else 1
        return f"SR-{today}-{count:03d}"

    @staticmethod
    def create(user_id, apartment_id, request_type, description, priority='medium', scheduled_date=None):
        """Create a new service request"""
        request_number = ServiceRequest.create_request_number()
        query = """
            INSERT INTO service_requests (request_number, user_id, apartment_id, request_type, description, priority, scheduled_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return ServiceRequest.execute_insert(query, (request_number, user_id, apartment_id, request_type, description, priority, scheduled_date))

    @staticmethod
    def get_by_id(request_id):
        """Get service request by ID"""
        query = """
            SELECT sr.*, u.full_name as tenant_name, a.unit_number, au.full_name as assigned_to_name
            FROM service_requests sr
            JOIN users u ON sr.user_id = u.id
            JOIN apartments a ON sr.apartment_id = a.id
            LEFT JOIN users au ON sr.assigned_to = au.id
            WHERE sr.id = %s
        """
        return ServiceRequest.execute_query(query, (request_id,), fetch_one=True)

    @staticmethod
    def get_all(status=None, priority=None, request_type=None, user_id=None):
        """Get all service requests with optional filters"""
        conditions = []
        params = []

        if status:
            conditions.append("sr.status = %s")
            params.append(status)
        if priority:
            conditions.append("sr.priority = %s")
            params.append(priority)
        if request_type:
            conditions.append("sr.request_type = %s")
            params.append(request_type)
        if user_id:
            conditions.append("sr.user_id = %s")
            params.append(user_id)

        where_clause = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        query = f"""
            SELECT sr.*, u.full_name as tenant_name, a.unit_number, au.full_name as assigned_to_name
            FROM service_requests sr
            JOIN users u ON sr.user_id = u.id
            JOIN apartments a ON sr.apartment_id = a.id
            LEFT JOIN users au ON sr.assigned_to = au.id
            {where_clause}
            ORDER BY
                CASE sr.priority
                    WHEN 'urgent' THEN 1
                    WHEN 'high' THEN 2
                    WHEN 'medium' THEN 3
                    WHEN 'low' THEN 4
                END,
                sr.created_at DESC
        """
        return ServiceRequest.execute_query(query, tuple(params) if params else None, fetch_all=True)

    @staticmethod
    def update(request_id, data):
        """Update service request information"""
        fields = []
        params = []

        for key, value in data.items():
            if key not in ['id', 'request_number']:
                if key == 'status' and value == 'completed':
                    fields.append("completed_at = NOW()")
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return 0

        params.append(request_id)
        query = f"UPDATE service_requests SET {', '.join(fields)} WHERE id = %s"
        return ServiceRequest.execute_update(query, tuple(params))

    @staticmethod
    def get_request_stats():
        """Get service request statistics"""
        query = """
            SELECT
                COUNT(*) as total_requests,
                SUM(CASE WHEN status = 'submitted' THEN 1 ELSE 0 END) as submitted,
                SUM(CASE WHEN status = 'assigned' THEN 1 ELSE 0 END) as assigned,
                SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled
            FROM service_requests
        """
        return ServiceRequest.execute_query(query, fetch_one=True)


class ActivityLog(BaseModel):
    """Activity Log model for tracking user actions"""

    @staticmethod
    def log(user_id, action, table_affected=None, record_id=None, details=None, ip_address=None):
        """Log an activity"""
        query = """
            INSERT INTO activity_log (user_id, action, table_affected, record_id, details, ip_address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return ActivityLog.execute_insert(query, (user_id, action, table_affected, record_id, details, ip_address))

    @staticmethod
    def get_recent(limit=50):
        """Get recent activity logs"""
        query = """
            SELECT al.*, u.username, u.full_name
            FROM activity_log al
            JOIN users u ON al.user_id = u.id
            ORDER BY al.created_at DESC
            LIMIT %s
        """
        return ActivityLog.execute_query(query, (limit,), fetch_all=True)
