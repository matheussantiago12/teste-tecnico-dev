import { Component, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { CustomerService } from '../services/customer.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { PlanService } from '../services/plan.service';

@Component({
  selector: 'app-customer',
  templateUrl: './customer.component.html',
  styleUrl: './customer.component.css'
})
export class CustomerComponent {
  id?: number = undefined;
  form: FormGroup;
  plans: any[] = [];

  displayedColumns = [
    'id',
    'name',
    'card_id',
    'action'
  ]

  dataSource!: MatTableDataSource<any>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(
    private fb: FormBuilder,
    private customerService: CustomerService,
    private planService: PlanService,
  ) {
    this.form = this.fb.group({
      name: '',
      card_id: '',
      plans: []
    })
  }

  ngOnInit(): void {
    this.getCustomersList();
    this.getPlansList();
  }

  getCustomersList() {
    this.customerService.all().subscribe({
      next: (res) => {
        this.dataSource = new MatTableDataSource(res);
        this.dataSource.paginator = this.paginator;
      },
      error: console.log
    })
  }

  getPlansList() {
    this.planService.all().subscribe({
      next: (res) => {
        this.plans = res
      },
      error: console.log
    })
  }

  onFormSubmit() {
    const plans_ids = this.form.value.plans
    console.log('plans_ids:: ', plans_ids)
    // if (this.form.valid) {
      if (!this.id) {
        this.customerService.create({ ...this.form.value, plans_ids})
          .subscribe({
            next: (val: any) => {
              alert('Cliente cadastrado com sucesso!')
              this.getCustomersList();
            },
            error: (err: any) => {
              console.error(err)
            }
          })
      } else {
        this.customerService.update({ ...this.form.value, plans_ids }, this.id)
          .subscribe({
            next: (val: any) => {
              alert('Cliente atualizado com sucesso!')
              this.getCustomersList();
            },
            error: (err: any) => {
              console.error(err)
            }
          })
      }
    // }
  }

  fillEditForm(data: any) {
    this.id = data.id;
    this.form.patchValue({})
    this.form.patchValue({
      name: data.name,
      card_id: data.card_id,
      plans: data.plans.map((plan: any) => plan.plan.id)
    });
  }

  cancelEditForm() {
    this.id = undefined;
    this.form.reset()
  }
}
