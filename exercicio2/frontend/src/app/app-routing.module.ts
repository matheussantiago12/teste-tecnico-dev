import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ParkMovementComponent } from './parkmovement/parkmovement.component';
import { CustomerComponent } from './customer/customer.component';
import { VehicleComponent } from './vehicle/vehicle.component';
import { PlanComponent } from './plan/plan.component';
import { ContractComponent } from './contract/contract.component';

const routes: Routes = [
  { path: '', redirectTo: 'operacao', pathMatch: 'full' },
  { path: 'operacao', component: ParkMovementComponent },
  { path: 'cliente', component: CustomerComponent },
  { path: 'veiculo', component: VehicleComponent },
  { path: 'plano', component: PlanComponent },
  { path: 'contrato', component: ContractComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
