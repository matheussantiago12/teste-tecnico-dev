import { Component, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { VehicleService } from '../services/vehicle.service';

@Component({
  selector: 'app-vehicle',
  templateUrl: './vehicle.component.html',
  styleUrl: './vehicle.component.css'
})
export class VehicleComponent {
  id?: number = undefined;
  form: FormGroup;

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
  ) {
    this.form = this.fb.group({
      plate: '',
      model: '',
      description: '',
      customer_id: '',
    })
  }

  ngOnInit(): void {
    this.getCustomersList();
  }

  getCustomersList() {
    this.vehicleService.all().subscribe({
      next: (res) => {
        this.dataSource = new MatTableDataSource(res);
        this.dataSource.paginator = this.paginator;
      },
      error: console.log
    })
  }

  onFormSubmit() {
    if (this.form.valid) {
      if (!this.id) {
        this.vehicleService.create(this.form.value)
          .subscribe({
            next: (val: any) => {
              alert('Veículo cadastrado com sucesso!')
              this.getCustomersList();
            },
            error: (err: any) => {
              console.error(err)
            }
          })
      } else {
        this.vehicleService.update(this.form.value, this.id)
          .subscribe({
            next: (val: any) => {
              alert('Veículo atualizado com sucesso!')
              this.getCustomersList();
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
      customer_id: data.customer_id,
    });
  }

  cancelEditForm() {
    this.id = undefined;
    this.form.reset()
  }
}
