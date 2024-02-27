from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Customer
from .serializers import CustomerSerializer

class ListCustomers(APIView):
    def get(self, request: Request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)

        return Response(serializer.data)
    
class CreateCustomers(APIView):
    def post(self, request: Request):
        customer = Customer.objects.create(
            name=request.data['name'],
            card_id=request.data['card_id']
        )

        serializer = CustomerSerializer(customer, many=False)
        
        return Response(serializer.data)