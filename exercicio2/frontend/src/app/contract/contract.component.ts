import { Component, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { ContractService } from '../services/contract.service';

@Component({
  selector: 'app-contract',
  templateUrl: './contract.component.html',
  styleUrl: './contract.component.css'
})
export class ContractComponent {
  id?: number = undefined;
  form: FormGroup;
  formRule: FormGroup;

  displayedColumns = [
    'id',
    'description',
    'max_value',
    'action',
  ]

  displayedColumnsRules = [
    'id',
    'until',
    'value',
  ]

  dataSource!: MatTableDataSource<any>;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(
    private fb: FormBuilder,
    private contractService: ContractService,
  ) {
    this.form = this.fb.group({
      description: '',
      max_value: '',
      contract_rules: []
    })

    this.formRule = this.fb.group({
      until: '',
      value: ''
    })
  }

  ngOnInit(): void {
    this.getContractsList();
  }

  getContractsList() {
    this.contractService.all().subscribe({
      next: (res) => {
        this.dataSource = new MatTableDataSource(res);
        this.dataSource.paginator = this.paginator;
      },
      error: console.log
    })
  }

  onFormSubmit() {
    if (!this.form.value.description) {
      alert('Informe a descrição do contrato!')
      return
    }

    if (!this.form.value.max_value) {
      alert('Informe o valor máximo do contrato!')
      return
    }

    if (this.form.valid) {
      if (!this.id) {
        this.contractService.create(this.form.value)
        .subscribe({
          next: (val: any) => {
            alert('Contrato cadastrado com sucesso!')
            this.form.reset();
            this.getContractsList();
          },
          error: (err: any) => {
            if (err.error.error) {
              alert(err.error.error)
            }
            console.error(err)
          }
        })
      } else {
        this.contractService.update({ ...this.form.value, id: this.id })
        .subscribe({
          next: (val: any) => {
            alert('Contrato atualizado com sucesso!')
            this.form.reset();
            this.getContractsList();
          },
          error: (err: any) => {
            if (err.error.error) {
              alert(err.error.error)
            }
            console.error(err)
          }
        })
      }
    }
  }

  onFormRuleSubmit() {
    if (!this.formRule.value.until || !this.formRule.value.value) {
      alert('Preencha todos os campos para adicionar uma regra!')
      return
    }

    const { contract_rules } = this.form.value
    const rules = contract_rules ? [...contract_rules, this.formRule.value] : [this.formRule.value]

    this.form.patchValue({
      contract_rules: rules
    })
    this.formRule.reset()
  }


  fillEditForm(data: any) {
    this.id = data.id;
    this.form.patchValue({
      max_value: data.max_value,
      description: data.description,
      contract_rules: data.contract_rules
    });
  }

  deleteRule(rule: any) {
    const filteredRules = this.form.value.contract_rules.filter((r: any) => r.id != rule.id)
    this.form.patchValue({
      contract_rules: filteredRules
    })
  }

  cancelEditForm() {
    this.id = undefined;
    this.form.reset();
    this.formRule.reset()
  }
}
