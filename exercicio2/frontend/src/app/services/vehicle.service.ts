import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BASE_URL } from '../app.module';

@Injectable({
  providedIn: 'root'
})
export class VehicleService {
  constructor(private http: HttpClient) {}

  all(): Observable<any> {
    return this.http.get(`${BASE_URL}/vehicle/`)
  }

  create(data: any): Observable<any> {
    return this.http.post(`${BASE_URL}/vehicle/`, data)
  }

  update(data: any, id: number): Observable<any> {
    return this.http.put(`${BASE_URL}/vehicle/${id}/`, data)
  }
}
