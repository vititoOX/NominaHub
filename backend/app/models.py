from datetime import date, datetime
from decimal import Decimal
from werkzeug.security import check_password_hash, generate_password_hash
from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='rrhh')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    hire_date = db.Column(db.Date, nullable=False, default=date.today)
    annual_salary = db.Column(db.Numeric(12, 2), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    payrolls = db.relationship('Payroll', backref='employee', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id, 'employeeCode': self.employee_code, 'firstName': self.first_name,
            'lastName': self.last_name, 'fullName': f'{self.first_name} {self.last_name}',
            'email': self.email, 'department': self.department, 'position': self.position,
            'hireDate': self.hire_date.isoformat(), 'annualSalary': float(self.annual_salary),
            'active': self.active,
        }

class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    period = db.Column(db.String(7), nullable=False)
    base_salary = db.Column(db.Numeric(12, 2), nullable=False)
    extras = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    income_tax_rate = db.Column(db.Numeric(5, 2), nullable=False, default=15)
    social_security_rate = db.Column(db.Numeric(5, 2), nullable=False, default=6.35)
    gross_salary = db.Column(db.Numeric(12, 2), nullable=False)
    deductions = db.Column(db.Numeric(12, 2), nullable=False)
    net_salary = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='draft')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def calculate(cls, employee, period, extras=0, income_tax_rate=15):
        base = Decimal(employee.annual_salary) / Decimal('12')
        extras_d = Decimal(str(extras))
        irpf = Decimal(str(income_tax_rate))
        ss = Decimal('6.35')
        gross = base + extras_d
        deductions = gross * ((irpf + ss) / Decimal('100'))
        return cls(employee=employee, period=period, base_salary=base.quantize(Decimal('0.01')),
                   extras=extras_d, income_tax_rate=irpf, social_security_rate=ss,
                   gross_salary=gross.quantize(Decimal('0.01')),
                   deductions=deductions.quantize(Decimal('0.01')),
                   net_salary=(gross-deductions).quantize(Decimal('0.01')))

    def to_dict(self):
        return {
            'id': self.id, 'employeeId': self.employee_id, 'employeeName': f'{self.employee.first_name} {self.employee.last_name}',
            'period': self.period, 'baseSalary': float(self.base_salary), 'extras': float(self.extras),
            'incomeTaxRate': float(self.income_tax_rate), 'grossSalary': float(self.gross_salary),
            'deductions': float(self.deductions), 'netSalary': float(self.net_salary), 'status': self.status,
            'createdAt': self.created_at.isoformat(),
        }
