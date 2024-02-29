import { Component, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { VehicleService } from '../services/vehicle.service';
import { CustomerService } from '../services/customer.service';

@Component({
  selector: 'app-vehicle',
  templateUrl: './vehicle.component.html',
  styleUrl: './vehicle.component.css'
})
export class VehicleComponent {
  id?: number = undefined;
  form: FormGroup;
  customers: any[] = []
  customerFc = new FormControl<any>('');

  displayedColumns = [
    'id',
    'plate',
    'model',
    'description',
    'customer',
    'action'
  ]

  dataSource!: MatTableDataSource<any>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(
    private fb: FormBuilder,
    private vehicleService: VehicleService,
    private customerService: CustomerService,
  ) {
    this.form = this.fb.group({
      plate: '',
      model: '',
      description: ''
    })
  }

  ngOnInit(): void {
    this.getVehiclesList();
    this.getCustomersList();
  }

  getVehiclesList() {
    this.vehicleService.all().subscribe({
      next: (res) => {
        this.dataSource = new MatTableDataSource(res);
        this.dataSource.paginator = this.paginator;
      },
      error: console.log
    })
  }

  getCustomersList() {
    this.customerService.all().subscribe({
      next: (res) => {
        this.customers = res
      },
      error: console.log
    })
  }

  displayFn(data: any): string {
    return data && data.name ? data.name : '';
  }

  onFormSubmit() {
    if (!this.form.value.plate) {
      alert('Informe a placa do veículo!')
      return
    }

    if (!this.form.value.model) {
      alert('Informe o modelo do veículo!')
      return
    }

    if (!this.form.value.description) {
      alert('Informe a descrição do veículo!')
      return
    }

    if (this.form.valid) {
      const data = {
        ...this.form.value,
        customer: null,
        customer_id: this.customerFc.value.id
      }

      if (!this.id) {
        this.vehicleService.create(data)
          .subscribe({
            next: (val: any) => {
              alert('Veículo cadastrado com sucesso!')
              this.form.reset();
              this.getVehiclesList();
            },
            error: (err: any) => {
              console.error(err)
            }
          })
      } else {
        this.vehicleService.update(data, this.id)
          .subscribe({
            next: (val: any) => {
              alert('Veículo atualizado com sucesso!');
              this.form.reset();
              this.getVehiclesList();
            },
            error: (err: any) => {
              console.error(err)
            }
          })
      }
    }
  }

  fillEditForm(data: any) {
    this.id = data.id;
    this.form.patchValue({
      plate: data.plate,
      model: data.model,
      description: data.description,
    });
    this.customerFc.patchValue(data.customer)
  }

  cancelEditForm() {
    this.id = undefined;
    this.form.reset()
    this.customerFc.reset()
  }
}
