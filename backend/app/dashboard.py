from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from .extensions import db
from .models import Employee, Payroll

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.get('')
@jwt_required()
def dashboard():
    active = Employee.query.filter_by(active=True).count()
    departments = db.session.query(Employee.department, func.count(Employee.id)).filter(Employee.active.is_(True)).group_by(Employee.department).all()
    payroll_count = Payroll.query.count()
    total_net = db.session.query(func.coalesce(func.sum(Payroll.net_salary), 0)).scalar()
    return jsonify({'activeEmployees': active, 'payrollCount': payroll_count, 'totalNetPayroll': float(total_net),
                    'departments': [{'name': name, 'count': count} for name, count in departments]})
