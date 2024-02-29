import { Component, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { PlanService } from '../services/plan.service';

@Component({
  selector: 'app-plan',
  templateUrl: './plan.component.html',
  styleUrl: './plan.component.css'
})
export class PlanComponent {
  id?: number = undefined;
  form: FormGroup;

  displayedColumns = [
    'id',
    'description',
    'value',
    'action',
  ]

  dataSource!: MatTableDataSource<any>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(
    private fb: FormBuilder,
    private planService: PlanService,
  ) {
    this.form = this.fb.group({
      description: '',
      value: ''
    })
  }

  ngOnInit(): void {
    this.getPlansList();
  }

  getPlansList() {
    this.planService.all().subscribe({
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
        this.planService.create(this.form.value)
          .subscribe({
            next: (val: any) => {
              alert('Plano cadastrado com sucesso!');
              this.form.reset();
              this.getPlansList();
            },
            error: (err: any) => {
              console.error(err)
            }
          })
      } else {
        this.planService.update(this.form.value, this.id)
          .subscribe({
            next: (val: any) => {
              alert('Plano atualizado com sucesso!');
              this.form.reset();
              this.getPlansList();
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
      value: data.value,
      description: data.description,
    });
  }

  cancelEditForm() {
    this.id = undefined;
    this.form.reset()
  }
}
