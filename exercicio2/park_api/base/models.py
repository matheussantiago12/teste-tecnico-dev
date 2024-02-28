from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=50)
    card_id = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name
    
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
        current_rules_ids = [item['id'] for item in rules if 'id' in item] # Lista de IDs das regras permanecerão (não foram alteradas)
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

class ParkMovement(models.Model):
    entry_date = models.DateTimeField()
    exit_date = models.DateTimeField(null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    value = models.FloatField(null=True)
