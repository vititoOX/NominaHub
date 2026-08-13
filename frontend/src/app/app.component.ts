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
  selector:'app-root', standalone:true,
  imports:[CommonModule,FormsModule,ButtonModule,CardModule,DialogModule,InputTextModule,InputNumberModule,SelectModule,TableModule,TagModule],
  templateUrl:'./app.component.html', styleUrl:'./app.component.css'
})
export class AppComponent implements OnInit {
  email='admin@nominahub.local'; password='Admin123!'; loginError=''; loading=false;
  user:any=null; view:'dashboard'|'employees'|'payrolls'='dashboard'; dashboardData:Dashboard|null=null;
  employees:Employee[]=[]; payrolls:Payroll[]=[]; employeeDialog=false; payrollDialog=false;
  employeeForm:any={department:'Tecnología',annualSalary:30000}; payrollForm:any={incomeTaxRate:15,extras:0};
  departments=['Tecnología','RRHH','Operaciones','Finanzas','Comercial'];
  constructor(private api:ApiService){}
  ngOnInit(){ const raw=localStorage.getItem('nh_user'); if(raw){this.user=JSON.parse(raw);this.refresh();} }
  login(){ this.loading=true;this.loginError='';this.api.login(this.email,this.password).subscribe({next:r=>{localStorage.setItem('nh_token',r.accessToken);localStorage.setItem('nh_user',JSON.stringify(r.user));this.user=r.user;this.loading=false;this.refresh();},error:()=>{this.loginError='Email o contraseña incorrectos';this.loading=false;}}); }
  logout(){ localStorage.removeItem('nh_token');localStorage.removeItem('nh_user');this.user=null; }
  refresh(){ this.api.dashboard().subscribe(v=>this.dashboardData=v);this.api.employees().subscribe(v=>this.employees=v);this.api.payrolls().subscribe(v=>this.payrolls=v); }
  money(v:number|undefined){return new Intl.NumberFormat('es-ES',{style:'currency',currency:'EUR'}).format(v||0);}
  saveEmployee(){this.api.createEmployee(this.employeeForm).subscribe(()=>{this.employeeDialog=false;this.employeeForm={department:'Tecnología',annualSalary:30000};this.refresh();});}
  savePayroll(){this.api.createPayroll(this.payrollForm).subscribe(()=>{this.payrollDialog=false;this.payrollForm={incomeTaxRate:15,extras:0};this.refresh();});}
  markPaid(p:Payroll){this.api.setPayrollStatus(p.id,'paid').subscribe(()=>this.refresh());}
  download(p:Payroll){this.api.payrollPdf(p.id).subscribe(blob=>{const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`nomina-${p.period}.pdf`;a.click();URL.revokeObjectURL(url);});}
}
