import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';
import { InputNumberModule } from 'primeng/inputnumber';
import { SelectModule } from 'primeng/select';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';
import { ApiService, Dashboard, Employee, Payroll } from './core/api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, ButtonModule, CardModule, DialogModule, InputTextModule, InputNumberModule, SelectModule, TableModule, TagModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  email = 'admin@nominahub.local';
  password = 'Admin123!';
  loginError = '';
  loading = false;
  user: any = null;
  view: 'dashboard' | 'employees' | 'payrolls' = 'dashboard';
  dashboardData: Dashboard | null = null;
  employees: Employee[] = [];
  payrolls: Payroll[] = [];
  employeeDialog = false;
  payrollDialog = false;
  employeeError = '';
  payrollError = '';
  notice = '';
  savingEmployee = false;
  savingPayroll = false;
  employeeForm: any = { department: 'Tecnología', annualSalary: 30000 };
  payrollForm: any = { incomeTaxRate: 15, extras: 0 };
  departments = ['Tecnología', 'RRHH', 'Operaciones', 'Finanzas', 'Comercial'];
  periodLabel = new Intl.DateTimeFormat('es-ES', { month: 'long', year: 'numeric' }).format(new Date());

  constructor(private api: ApiService) {}

  ngOnInit() {
    const raw = localStorage.getItem('nh_user');
    if (raw) {
      this.user = JSON.parse(raw);
      this.refresh();
    }
  }

  login() {
    this.loading = true;
    this.loginError = '';
    this.api.login(this.email, this.password).subscribe({
      next: r => {
        localStorage.setItem('nh_token', r.accessToken);
        localStorage.setItem('nh_user', JSON.stringify(r.user));
        this.user = r.user;
        this.loading = false;
        this.refresh();
      },
      error: () => {
        this.loginError = 'Email o contraseña incorrectos';
        this.loading = false;
      }
    });
  }

  logout() {
    localStorage.removeItem('nh_token');
    localStorage.removeItem('nh_user');
    this.user = null;
  }

  refresh() {
    this.api.dashboard().subscribe(v => this.dashboardData = v);
    this.api.employees().subscribe(v => this.employees = v);
    this.api.payrolls().subscribe(v => this.payrolls = v);
  }

  money(v: number | undefined) {
    return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(v || 0);
  }

  openEmployeeDialog() {
    this.employeeError = '';
    this.employeeForm = { department: 'Tecnología', annualSalary: 30000 };
    this.employeeDialog = true;
  }

  openPayrollDialog() {
    this.payrollError = '';
    this.payrollForm = { incomeTaxRate: 15, extras: 0 };
    this.payrollDialog = true;
  }

  saveEmployee() {
    const f = this.employeeForm;
    if (!f.employeeCode?.trim() || !f.firstName?.trim() || !f.lastName?.trim() || !f.email?.trim() || !f.department || !f.position?.trim() || !f.annualSalary) {
      this.employeeError = 'Completa todos los campos obligatorios antes de guardar el empleado.';
      return;
    }
    if (!/^\S+@\S+\.\S+$/.test(f.email)) {
      this.employeeError = 'Introduce un email válido.';
      return;
    }
    if (Number(f.annualSalary) <= 0) {
      this.employeeError = 'El salario anual debe ser mayor que 0 €.';
      return;
    }
    this.savingEmployee = true;
    this.employeeError = '';
    this.api.createEmployee(f).subscribe({
      next: () => {
        this.employeeDialog = false;
        this.savingEmployee = false;
        this.notice = 'Empleado guardado correctamente.';
        this.refresh();
        setTimeout(() => this.notice = '', 3500);
      },
      error: err => {
        this.employeeError = this.errorMessage(err, 'No se pudo guardar el empleado. Revisa los datos e inténtalo de nuevo.');
        this.savingEmployee = false;
      }
    });
  }

  savePayroll() {
    const f = this.payrollForm;
    if (!f.employeeId || !f.period?.trim()) {
      this.payrollError = 'Selecciona un empleado e indica el periodo de la nómina.';
      return;
    }
    if (!/^\d{4}-(0[1-9]|1[0-2])$/.test(f.period)) {
      this.payrollError = 'El periodo debe tener el formato AAAA-MM, por ejemplo 2026-08.';
      return;
    }
    if (Number(f.incomeTaxRate) < 0 || Number(f.incomeTaxRate) > 50) {
      this.payrollError = 'El IRPF debe estar entre 0 % y 50 %.';
      return;
    }
    if (Number(f.extras || 0) < 0) {
      this.payrollError = 'Los complementos no pueden ser negativos.';
      return;
    }
    this.savingPayroll = true;
    this.payrollError = '';
    this.api.createPayroll(f).subscribe({
      next: () => {
        this.payrollDialog = false;
        this.savingPayroll = false;
        this.notice = 'Nómina generada correctamente.';
        this.refresh();
        setTimeout(() => this.notice = '', 3500);
      },
      error: err => {
        this.payrollError = this.errorMessage(err, 'No se pudo generar la nómina. Revisa los datos e inténtalo de nuevo.');
        this.savingPayroll = false;
      }
    });
  }

  markPaid(p: Payroll) {
    this.api.setPayrollStatus(p.id, 'paid').subscribe({
      next: () => {
        this.notice = 'Nómina marcada como pagada.';
        this.refresh();
        setTimeout(() => this.notice = '', 3500);
      }
    });
  }

  download(p: Payroll) {
    this.api.payrollPdf(p.id).subscribe(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `nomina-${p.period}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  private errorMessage(err: any, fallback: string) {
    return err?.error?.message || fallback;
  }
}
