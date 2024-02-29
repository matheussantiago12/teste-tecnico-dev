import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { ParkMovementComponent } from './parkmovement/parkmovement.component';
import { CustomerComponent } from './customer/customer.component';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { VehicleComponent } from './vehicle/vehicle.component';
import { CommonModule } from '@angular/common';
import { MatSelectModule } from '@angular/material/select';
import { PlanComponent } from './plan/plan.component';
import { ContractComponent } from './contract/contract.component';
import { MatAutocompleteModule } from '@angular/material/autocomplete';

export const BASE_URL = "http://localhost:8000/api/v1"

@NgModule({
  declarations: [
    AppComponent,
    CustomerComponent,
    ParkMovementComponent,
    VehicleComponent,
    PlanComponent,
    ContractComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    HttpClientModule,
    ReactiveFormsModule,
    MatPaginatorModule,
    MatTableModule,
    MatFormFieldModule,
    MatInputModule,
    CommonModule,
    MatSelectModule,
    MatAutocompleteModule
  ],
  providers: [
    provideAnimationsAsync()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
