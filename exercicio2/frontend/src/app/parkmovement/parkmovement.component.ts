import { Component, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { ParkMovementService } from '../services/parkmovement.service';
import Swal from 'sweetalert2'
import moment from 'moment'

@Component({
  selector: 'app-parkmovement',
  templateUrl: './parkmovement.component.html',
  styleUrl: './parkmovement.component.css'
})
export class ParkMovementComponent {
  form: FormGroup;

  displayedColumns = [
    'entry_date',
    'plate',
    'card_id',
    'action'
  ]

  dataSource!: MatTableDataSource<any>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(
    private fb: FormBuilder,
    private parkMovementService: ParkMovementService,
  ) {
    this.form = this.fb.group({
      plate: '',
      value: '',
      card_id: '',
    })
  }

  ngOnInit(): void {
    this.getParkMovementList();
  }

  getParkMovementList() {
    this.parkMovementService.all().subscribe({
      next: (res) => {
        this.dataSource = new MatTableDataSource(res);
        this.dataSource.paginator = this.paginator;
      },
      error: console.log
    })
  }

  onFormSubmit() {
    if (this.form.valid) {
      this.parkMovementService.create(this.form.value)
        .subscribe({
          next: (val: any) => {
            alert('Entrada cadastrado com sucesso!');
            this.form.reset();
            this.getParkMovementList();
          },
          error: (err: any) => {
            console.error('error:', err)
            if (err.error.error) {
              alert(err.error.error)
            }
          }
        })
    }
  }

  exitFromPark(data: any) {
    Swal.fire({
      title: `Saída do carro com placa ${data.vehicle.plate}`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#4758B8",
      cancelButtonColor: "#aaa",
      confirmButtonText: "Confirmar",
      cancelButtonText: "Cancelar"
    }).then((result) => {
      if (result.isConfirmed) {
        this.parkMovementService.update(data.id)
          .subscribe({
            next: (val: any) => {
              Swal.fire({
                title: "Saída efetuada com sucesso!",
                html: `
                  <p><b>Valor: ${val.value.toLocaleString('pt-br',{style: 'currency', currency: 'BRL'})}</b></p>
                  <p><b>Entrada</b>: ${moment(val.entry_date).format('DD/MM/YYYY')} <b class="bold">${moment(val.entry_date).format('HH:mm:ss')}</b></p>
                  <p><b>Saída</b>: ${moment(val.exit_date).format('DD/MM/YYYY')} <b class="bold">${moment(val.exit_date).format('HH:mm:ss')}</b></p>
                `,
                icon: "success"
              });

              this.getParkMovementList();
            },
            error: (err: any) => {
              console.error('error:', err)
              if (err.error.error) {
                alert(err.error.error)
              }
            }
          })
      }
    });
  }

  cancelEditForm() {
    this.form.reset()
  }
}
