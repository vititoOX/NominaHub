from io import BytesIO
from weasyprint import HTML

def build_payroll_pdf(payroll):
    employee = payroll.employee
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
    body{{font-family:Arial,sans-serif;color:#152238;padding:36px}} .header{{display:flex;justify-content:space-between;border-bottom:3px solid #4f46e5;padding-bottom:16px}}
    h1{{margin:0;color:#312e81}} table{{width:100%;border-collapse:collapse;margin-top:28px}} td,th{{padding:12px;border-bottom:1px solid #e5e7eb;text-align:left}}
    .total{{font-size:20px;font-weight:700;color:#166534}} .muted{{color:#64748b}}
    </style></head><body><div class="header"><div><h1>NominaHub</h1><div class="muted">Recibo de nómina · {payroll.period}</div></div><div>{employee.employee_code}</div></div>
    <h2>{employee.first_name} {employee.last_name}</h2><p>{employee.position} · {employee.department}</p>
    <table><tr><th>Concepto</th><th>Importe</th></tr><tr><td>Salario base</td><td>{payroll.base_salary:.2f} €</td></tr><tr><td>Complementos</td><td>{payroll.extras:.2f} €</td></tr><tr><td>Bruto</td><td>{payroll.gross_salary:.2f} €</td></tr><tr><td>Deducciones</td><td>-{payroll.deductions:.2f} €</td></tr><tr class="total"><td>Neto</td><td>{payroll.net_salary:.2f} €</td></tr></table></body></html>'''
    output = BytesIO()
    HTML(string=html).write_pdf(output)
    output.seek(0)
    return output
