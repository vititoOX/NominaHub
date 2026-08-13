from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required
from .extensions import db
from .models import Employee, Payroll
from .pdf_service import build_payroll_pdf

payrolls_bp = Blueprint('payrolls', __name__, url_prefix='/api/payrolls')

@payrolls_bp.get('')
@jwt_required()
def list_payrolls():
    payrolls = Payroll.query.order_by(Payroll.created_at.desc()).all()
    return jsonify([payroll.to_dict() for payroll in payrolls])

@payrolls_bp.post('')
@jwt_required()
def create_payroll():
    data = request.get_json() or {}
    employee = db.session.get(Employee, data.get('employeeId'))
    if not employee or not data.get('period'):
        return jsonify({'message': 'Empleado y periodo son obligatorios'}), 400
    payroll = Payroll.calculate(employee, data['period'], data.get('extras', 0), data.get('incomeTaxRate', 15))
    db.session.add(payroll)
    db.session.commit()
    return jsonify(payroll.to_dict()), 201

@payrolls_bp.patch('/<int:payroll_id>/status')
@jwt_required()
def change_status(payroll_id):
    payroll = db.session.get(Payroll, payroll_id)
    if not payroll:
        return jsonify({'message': 'Nómina no encontrada'}), 404
    payroll.status = (request.get_json() or {}).get('status', payroll.status)
    db.session.commit()
    return jsonify(payroll.to_dict())

@payrolls_bp.get('/<int:payroll_id>/pdf')
@jwt_required()
def payroll_pdf(payroll_id):
    payroll = db.session.get(Payroll, payroll_id)
    if not payroll:
        return jsonify({'message': 'Nómina no encontrada'}), 404
    pdf = build_payroll_pdf(payroll)
    return send_file(pdf, mimetype='application/pdf', as_attachment=True, download_name=f'nomina-{payroll.period}-{payroll.employee.employee_code}.pdf')
