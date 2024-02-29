from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.http import Http404
from datetime import datetime, timezone

from .models import Customer, Vehicle, Plan, Contract, ParkMovement, ContractRule, CustomerPlan
from .serializers import CustomerSerializer, VehicleSerializer, PlanSerializer, ContractSerializer, ParkMovementSerializer

class CustomersView(APIView):
    def get(self, request: Request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)

        return Response(serializer.data)
    
    def post(self, request: Request):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            customer = serializer.save()

            if request.data.get('plans_ids'):
                current_date = datetime.now(timezone.utc)
                for id in request.data.get('plans_ids'):
                    CustomerPlan.objects.create(customer_id=customer.id, plan_id=id, due_date=current_date)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomersDetailView(APIView):
    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

        customer.update_plans(request.data.get('plans_ids'))

        serializer = CustomerSerializer(customer, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VehiclesView(APIView):
    def get(self, request: Request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)

        return Response(serializer.data)
    
    def post(self, request: Request):
        serializer = VehicleSerializer(data=request.data)

        if serializer.is_valid():
            plate_exists = Vehicle.objects.filter(plate=request.data.get('plate')).first()

            if (plate_exists):
                return Response({'error': 'Um veículo com essa placa já existe!'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VehiclesDetailView(APIView):
    def put(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            raise Http404
    
        serializer = VehicleSerializer(vehicle, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PlansView(APIView):
    def get(self, request: Request):
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)

        return Response(serializer.data)
    
    def post(self, request: Request):
        serializer = PlanSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PlansDetailView(APIView):
    def put(self, request, pk):
        try:
            plan = Plan.objects.get(pk=pk)
        except Plan.DoesNotExist:
            raise Http404
    
        serializer = PlanSerializer(plan, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ContractView(APIView):
    def get(self, request: Request):
        contracts = Contract.objects.all()
        serializer = ContractSerializer(contracts, many=True)

        return Response(serializer.data)
    
    def post(self, request: Request):
        if not request.data.get('id'):
            already_has_contract = Contract.objects.all().count() >= 1
            if already_has_contract:
                return Response({'error': 'Já existe um contrato cadastrado. Máximo: 1'}, status=status.HTTP_400_BAD_REQUEST)
            
        if not request.data.get('contract_rules'):
            return Response({'error': 'O contrato deve ter ao menos 1 regra.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ContractSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            contract = Contract.objects.get(pk=request.data['id'])
        except Contract.DoesNotExist:
            raise Http404
        
        if not request.data.get('contract_rules'):
            return Response({'error': 'O contrato deve ter ao menos 1 regra.'}, status=status.HTTP_400_BAD_REQUEST)
    
        serializer = ContractSerializer(contract, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ParkMovementView(APIView):
    def create_or_find_vehicle(self, plate):
        vehicle = Vehicle.objects.filter(plate__iexact=plate).first()

        if not vehicle:
            vehicle_serializer = VehicleSerializer(data={'plate': plate})

            if not vehicle_serializer.is_valid():
                return Response(vehicle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

            vehicle_serializer.save()
            vehicle = vehicle_serializer.data
            vehicle_id = vehicle['id']
        else :
            vehicle_id = vehicle.id

        return vehicle_id

    def get(self, request: Request):
        movements = ParkMovement.objects.filter(exit_date__isnull=True)
        serializer = ParkMovementSerializer(movements, many=True)

        return Response(serializer.data)
    
    def post(self, request: Request): # Entrada no estacionamento
        if not request.data.get('plate'):
            return Response({'error': 'Informe a placa!'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.data.get('card_id'):
            return Response({'error': 'Informe o card ID!'}, status=status.HTTP_400_BAD_REQUEST)
        
        vehicle_id = self.create_or_find_vehicle(request.data['plate'])

        try:
            customer = Customer.objects.get(card_id=request.data['card_id'])
        except Customer.DoesNotExist:
            return Response({'error': 'Um cliente com o card ID informado não existe.'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_customer_on_the_park = ParkMovement.objects.filter(customer_id=customer.id,exit_date__isnull=True).first()
        is_car_on_the_park = ParkMovement.objects.filter(vehicle_id=vehicle_id,exit_date__isnull=True).first()

        if is_car_on_the_park:
            return Response({'error': 'O carro já está no estacionamento.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if is_customer_on_the_park:
            return Response({'error': 'O cliente já está no estacionamento.'}, status=status.HTTP_400_BAD_REQUEST)
    
        current_date = datetime.now(timezone.utc)

        movement = {
            'exit_date': None,
            'value': None,
            'entry_date': current_date,
            'vehicle_id': vehicle_id,
            'customer_id': customer.id
        }

        serializer = ParkMovementSerializer(data=movement)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
class ParkMovementDetailView(APIView):
    def get_time_difference(self, final_date: datetime, initial_date: datetime):
        diff = final_date - initial_date

        return diff.total_seconds() / 60

    def put(self, request, pk): # Saída do estacionamento
        try:
            park_movement = ParkMovement.objects.get(pk=pk)
        except ParkMovement.DoesNotExist:
            raise Http404
        
        has_plan = bool(Plan.customers.through.objects.filter(customer_id=park_movement.customer.id).count())
        current_datetime = datetime.now(timezone.utc)

        if has_plan:
            value = 0
        else :
            minutes = self.get_time_difference(current_datetime, park_movement.entry_date) # Tempo gasto no estacionamento

            contract = Contract.objects.all().first()
            contract_rule = ContractRule.objects.filter(contract_id=contract.id,until__gte=minutes).order_by('until').first() # Pega a regra correspondente ao tempo gasto

            if not contract_rule:
                contract_rule = ContractRule.objects.all().order_by('-until').first() # Caso o 'until' seja superior ao tempo gasto, pega a regra com o maior 'until'

            value = contract_rule.value

            if value > contract.max_value:
                value = contract.max_value
        
        new_data = {
            'exit_date': current_datetime,
            'value': value
        }
    
        serializer = ParkMovementSerializer(park_movement, data=new_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)