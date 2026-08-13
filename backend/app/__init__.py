from flask import Flask, jsonify
from flask_cors import CORS
from .config import Config
from .extensions import db, jwt
from .auth import auth_bp
from .employees import employees_bp
from .payrolls import payrolls_bp
from .dashboard import dashboard_bp
from .models import Employee, Payroll, User

def seed_demo_data():
    if User.query.count() == 0:
        admin = User(email='admin@nominahub.local', name='Víctor Pérez', role='admin')
        admin.set_password('Admin123!')
        db.session.add(admin)
    if Employee.query.count() == 0:
        db.session.add_all([
            Employee(employee_code='NH-001', first_name='Laura', last_name='García', email='laura@nominahub.local', department='Tecnología', position='Desarrolladora Full Stack', annual_salary=33000),
            Employee(employee_code='NH-002', first_name='Carlos', last_name='Martín', email='carlos@nominahub.local', department='Operaciones', position='Responsable de Operaciones', annual_salary=36000),
            Employee(employee_code='NH-003', first_name='Marta', last_name='Rodríguez', email='marta@nominahub.local', department='RRHH', position='Técnica de RRHH', annual_salary=29000),
        ])
    db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r'/api/*': {'origins': app.config['CORS_ORIGINS']}}, allow_headers=['Content-Type', 'Authorization'])
    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(payrolls_bp)
    app.register_blueprint(dashboard_bp)

    @app.get('/api/health')
    def health():
        return jsonify({'status': 'ok', 'service': 'NominaHub API'})

    with app.app_context():
        db.create_all()
        seed_demo_data()
    return app
