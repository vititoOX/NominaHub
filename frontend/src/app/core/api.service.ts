import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Employee { id:number; employeeCode:string; firstName:string; lastName:string; fullName:string; email:string; department:string; position:string; hireDate:string; annualSalary:number; active:boolean; }
export interface Payroll { id:number; employeeId:number; employeeName:string; period:string; baseSalary:number; extras:number; incomeTaxRate:number; grossSalary:number; deductions:number; netSalary:number; status:string; createdAt:string; }
export interface Dashboard { activeEmployees:number; payrollCount:number; totalNetPayroll:number; departments:{name:string;count:number}[]; }

@Injectable({providedIn:'root'})
export class ApiService {
  private readonly base = 'http://localhost:5000/api';
  constructor(private http: HttpClient) {}
  login(email:string,password:string){ return this.http.post<any>(`${this.base}/auth/login`,{email,password}); }
  dashboard():Observable<Dashboard>{ return this.http.get<Dashboard>(`${this.base}/dashboard`); }
  employees():Observable<Employee[]>{ return this.http.get<Employee[]>(`${this.base}/employees`); }
  createEmployee(data:any):Observable<Employee>{ return this.http.post<Employee>(`${this.base}/employees`,data); }
  payrolls():Observable<Payroll[]>{ return this.http.get<Payroll[]>(`${this.base}/payrolls`); }
  createPayroll(data:any):Observable<Payroll>{ return this.http.post<Payroll>(`${this.base}/payrolls`,data); }
  setPayrollStatus(id:number,status:string){ return this.http.patch<Payroll>(`${this.base}/payrolls/${id}/status`,{status}); }
  payrollPdf(id:number){ return this.http.get(`${this.base}/payrolls/${id}/pdf`,{responseType:'blob'}); }
}
