import re
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required
from .extensions import db
from .models import Employee, Payroll
from .pdf_service import build_payroll_pdf

payrolls_bp = Blueprint('payrolls', __name__, url_prefix='/api/payrolls')
PERIOD_RE = re.compile(r'^\d{4}-(0[1-9]|1[0-2])$')

@payrolls_bp.get('')
@jwt_required()
def list_payrolls():
    payrolls = Payroll.query.order_by(Payroll.created_at.desc()).all()
    return jsonify([payroll.to_dict() for payroll in payrolls])

@payrolls_bp.post('')
@jwt_required()
def create_payroll():
    data = request.get_json() or {}
    employee_id = data.get('employeeId')
    period = str(data.get('period') or '').strip()

    if not employee_id or not period:
        return jsonify({'message': 'Selecciona un empleado e indica el periodo de la nómina.'}), 400
    if not PERIOD_RE.match(period):
        return jsonify({'message': 'El periodo debe tener el formato AAAA-MM.'}), 400

    employee = db.session.get(Employee, employee_id)
    if not employee:
        return jsonify({'message': 'El empleado seleccionado no existe.'}), 404

    try:
        extras = float(data.get('extras', 0) or 0)
        income_tax_rate = float(data.get('incomeTaxRate', 15))
    except (TypeError, ValueError):
        return jsonify({'message': 'IRPF y complementos deben ser valores numéricos.'}), 400

    if extras < 0:
        return jsonify({'message': 'Los complementos no pueden ser negativos.'}), 400
    if not 0 <= income_tax_rate <= 50:
        return jsonify({'message': 'El IRPF debe estar entre 0 y 50 %.'}), 400

    existing = Payroll.query.filter_by(employee_id=employee.id, period=period).first()
    if existing:
        return jsonify({'message': 'Ya existe una nómina para este empleado en ese periodo.'}), 409

    payroll = Payroll.calculate(employee, period, extras, income_tax_rate)
    db.session.add(payroll)
    db.session.commit()
    return jsonify(payroll.to_dict()), 201

@payrolls_bp.patch('/<int:payroll_id>/status')
@jwt_required()
def change_status(payroll_id):
    payroll = db.session.get(Payroll, payroll_id)
    if not payroll:
        return jsonify({'message': 'Nómina no encontrada'}), 404
    status = (request.get_json() or {}).get('status', payroll.status)
    if status not in {'draft', 'paid'}:
        return jsonify({'message': 'Estado de nómina no válido.'}), 400
    payroll.status = status
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
