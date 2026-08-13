from datetime import date
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from .extensions import db
from .models import Employee

employees_bp = Blueprint('employees', __name__, url_prefix='/api/employees')

@employees_bp.get('')
@jwt_required()
def list_employees():
    employees = Employee.query.order_by(Employee.last_name, Employee.first_name).all()
    return jsonify([employee.to_dict() for employee in employees])

@employees_bp.post('')
@jwt_required()
def create_employee():
    data = request.get_json() or {}
    required = ['employeeCode', 'firstName', 'lastName', 'email', 'department', 'position', 'annualSalary']
    if any(not data.get(key) for key in required):
        return jsonify({'message': 'Faltan campos obligatorios'}), 400
    employee = Employee(
        employee_code=data['employeeCode'], first_name=data['firstName'], last_name=data['lastName'],
        email=data['email'].lower(), department=data['department'], position=data['position'],
        hire_date=date.fromisoformat(data.get('hireDate') or date.today().isoformat()), annual_salary=data['annualSalary']
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify(employee.to_dict()), 201
