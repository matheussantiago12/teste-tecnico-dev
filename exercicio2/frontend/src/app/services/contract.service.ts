import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BASE_URL } from '../app.module';

@Injectable({
  providedIn: 'root'
})
export class ContractService {
  constructor(private http: HttpClient) {}

  all(): Observable<any> {
    return this.http.get(`${BASE_URL}/contract/`)
  }

  create(data: any): Observable<any> {
    return this.http.post(`${BASE_URL}/contract/`, data)
  }

  update(data: any): Observable<any> {
    return this.http.put(`${BASE_URL}/contract/`, data)
  }
}
