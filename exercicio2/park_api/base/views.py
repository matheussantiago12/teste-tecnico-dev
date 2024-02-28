from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.http import Http404
import datetime

from .models import Customer, Vehicle, Plan, Contract, ParkMovement
from .serializers import CustomerSerializer, VehicleSerializer, PlanSerializer, ContractSerializer, ParkMovementSerializer

class CustomersView(APIView):
    def get(self, request: Request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)

        return Response(serializer.data)
    
    def post(self, request: Request):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomersDetailView(APIView):
    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404
    
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
        serializer = ContractSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ContractDetailView(APIView):
    def put(self, request, pk):
        try:
            contract = Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            raise Http404
    
        serializer = ContractSerializer(contract, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ParkMovementView(APIView):
    def get(self, request: Request):
        movements = ParkMovement.objects.all()
        serializer = ParkMovementSerializer(movements, many=True)

        return Response(serializer.data)
    
    def post(self, request: Request):
        if not 'plate' in request.data:
            return Response({'error': 'plate is null or empty'}, status=status.HTTP_400_BAD_REQUEST)

        vehicle = Vehicle.objects.filter(plate=request.data['plate']).first()

        if not vehicle:
            print(1)
            vehicle_serializer = VehicleSerializer(data={'plate': request.data['plate']})

            if not vehicle_serializer.is_valid():
                return Response(vehicle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            vehicle_serializer.save()
            vehicle = vehicle_serializer.data
            print(2)
    
        current_date = datetime.datetime.now()

        movement = {
            'exit_date': None,
            'value': None,
            'entry_date': current_date,
            'vehicle': vehicle['id']
        }

        serializer = ParkMovementSerializer(data=movement)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)