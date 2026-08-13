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
    missing = [key for key in required if not data.get(key)]
    if missing:
        return jsonify({'message': 'Completa todos los campos obligatorios del empleado.'}), 400

    email = str(data['email']).strip().lower()
    if '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'message': 'Introduce un email válido.'}), 400

    try:
        annual_salary = float(data['annualSalary'])
    except (TypeError, ValueError):
        return jsonify({'message': 'El salario anual debe ser un número válido.'}), 400

    if annual_salary <= 0:
        return jsonify({'message': 'El salario anual debe ser mayor que 0.'}), 400

    employee_code = str(data['employeeCode']).strip().upper()
    if Employee.query.filter_by(employee_code=employee_code).first():
        return jsonify({'message': 'Ya existe un empleado con ese código.'}), 409
    if Employee.query.filter_by(email=email).first():
        return jsonify({'message': 'Ya existe un empleado con ese email.'}), 409

    try:
        hire_date = date.fromisoformat(data.get('hireDate') or date.today().isoformat())
    except ValueError:
        return jsonify({'message': 'La fecha de alta no tiene un formato válido.'}), 400

    employee = Employee(
        employee_code=employee_code,
        first_name=str(data['firstName']).strip(),
        last_name=str(data['lastName']).strip(),
        email=email,
        department=str(data['department']).strip(),
        position=str(data['position']).strip(),
        hire_date=hire_date,
        annual_salary=annual_salary
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify(employee.to_dict()), 201
