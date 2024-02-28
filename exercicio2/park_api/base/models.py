from django.db import models
from datetime import datetime, timezone

class Customer(models.Model):
    name = models.CharField(max_length=50)
    card_id = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name
    
    def update_plans(self, plans_ids): # Atualiza a lista de regras vinculadas ao contrato
        # deletados = CustomerPlan.objects.filter(customer_id=self.id).exclude(plan_id__in=plans_ids)
        # print('deletados', deletados)
        CustomerPlan.objects.filter(customer_id=self.id).exclude(plan_id__in=plans_ids).delete() # Tira o vínculo com o cliente dos planos que não estão na lista de IDs
        # a = CustomerPlan.objects.filter(customer_id=self.id).exclude(plan_id__in=plans_ids)
        # print('deletados2', a)
        existing_ids = CustomerPlan.objects.filter(plan_id__in=plans_ids,customer_id=self.id).values_list('plan_id', flat=True) # Lista dos planos que não serão alterados
        print('existing_ids', existing_ids)
        new_plans_ids = [id for id in plans_ids if id not in existing_ids] # Lista de IDs dos planos novos
        print('new_plans_ids', new_plans_ids)



        if new_plans_ids:
            due_date = datetime.now(timezone.utc)

            for id in new_plans_ids:
                CustomerPlan.objects.create(customer_id=self.id, plan_id=id, due_date=due_date) # Insere os novos planos
    
class Vehicle(models.Model):
    plate = models.CharField(max_length=10)
    model = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=50, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.plate
    
class Plan(models.Model):
    description = models.CharField(max_length=50)
    value = models.FloatField()
    customers = models.ManyToManyField(Customer, through='CustomerPlan')

    def __str__(self):
        return self.description

# Tabela intermediária da relação entre Customer e Plan
class CustomerPlan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    due_date = models.DateTimeField()

class Contract(models.Model):
    description = models.CharField(max_length=50)
    max_value = models.FloatField(null=True)

    def __str__(self):
        return self.description
    
    def update_rules(self, rules): # Atualiza a lista de regras vinculadas ao contrato
        current_rules_ids = [item['id'] for item in rules if 'id' in item] # Lista de IDs das regras que permanecerão (não foram alteradas)
        ContractRule.objects.exclude(id__in=current_rules_ids).delete() # Exclui as regras que não estão na lista de IDs

        def has_id(dictionary: dict):
            return 0 if "id" in dictionary else 1

        rules_without_id = filter(has_id, rules) # Filtra as regras que deverão ser criadas (que não tem ID)

        for rule_wihout_id in rules_without_id: # Cria as regras novas
            rule_wihout_id['contract'] = self
            ContractRule.objects.create(**rule_wihout_id)

class ContractRule(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='contract_rules')
    until = models.IntegerField()
    value = models.FloatField()

    def __str__(self):
        return str(self.id)

class ParkMovement(models.Model):
    entry_date = models.DateTimeField()
    exit_date = models.DateTimeField(null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    value = models.FloatField(null=True)
