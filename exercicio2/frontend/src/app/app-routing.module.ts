import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ParkMovementComponent } from './parkmovement/parkmovement.component';
import { CustomerComponent } from './customer/customer.component';
import { VehicleComponent } from './vehicle/vehicle.component';

const routes: Routes = [
  { path: '', redirectTo: 'operacao', pathMatch: 'full' },
  { path: 'operacao', component: ParkMovementComponent },
  { path: 'cliente', component: CustomerComponent },
  { path: 'veiculo', component: VehicleComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
