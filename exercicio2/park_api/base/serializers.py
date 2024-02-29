from rest_framework import serializers
from .models import Customer, Vehicle, Plan, Contract, ContractRule, ParkMovement, CustomerPlan
    
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'description', 'value']

class CustomerPlanSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    class Meta:
        model = CustomerPlan
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    plans = CustomerPlanSerializer(source='customerplan_set', many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'card_id', 'plans']

class VehicleSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    customer = CustomerSerializer(read_only = True)

    class Meta:
        model = Vehicle
        fields = '__all__'

class ContractRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractRule
        fields = '__all__'

class ContractRuleOfContractSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ContractRule
        fields = ['until', 'value', 'id']
    
class ContractSerializer(serializers.ModelSerializer):
    contract_rules = ContractRuleOfContractSerializer(many=True)

    class Meta:
        model = Contract
        fields = ['id', 'description', 'max_value', 'contract_rules']

    def create(self, validated_data):
        rules = validated_data.pop('contract_rules')
        contract = super().create(validated_data)
        for rule in rules:
            rule['contract'] = contract
        
        self.fields['contract_rules'].create(rules)
        return contract
    
    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.max_value = validated_data.get('max_value', instance.max_value)
        instance.update_rules(validated_data.pop('contract_rules'))
        instance.save()
        return instance

class ParkMovementSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.IntegerField(write_only=True, required=True, allow_null=False)
    customer_id = serializers.IntegerField(write_only=True, required=True, allow_null=False)

    class Meta:
        model = ParkMovement
        fields = '__all__'
        depth = 1