import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BASE_URL } from '../app.module';

@Injectable({
  providedIn: 'root'
})
export class PlanService {
  constructor(private http: HttpClient) {}

  all(): Observable<any> {
    return this.http.get(`${BASE_URL}/plan/`)
  }

  create(data: any): Observable<any> {
    return this.http.post(`${BASE_URL}/plan/`, data)
  }

  update(data: any, id: number): Observable<any> {
    return this.http.put(`${BASE_URL}/plan/${id}/`, data)
  }
}
