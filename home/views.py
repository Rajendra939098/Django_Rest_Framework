from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.Serializer import *
from home.models import Person
from rest_framework.views import APIView
from rest_framework import viewsets,status 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token



class RegisterAPI(APIView):

    def post(self,request):
        data=request.data
        serializer=RegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status':False,
                'message':serializer.errors
            },status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'status':True , 'message':'user created'} , status.HTTP_201_CREATED)


class LoginAPI(APIView):

    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status':False,
                'message':serializer.errors
            },status.HTTP_400_BAD_REQUEST) 
        
        user=authenticate(username=serializer.data['username'],password=serializer.data['password'])
        if not user:
            return Response({
                'status':False,
                'message':"Invalid Crendtials..."
            },status.HTTP_400_BAD_REQUEST) 
        token,_=Token.objects.get_or_create(user=user)
        return Response({'status':True , 'message':'user Login', 'Token':str(token)} , status.HTTP_201_CREATED)



@api_view(['GET'])
def index(request):
    courses={
        'course_name':'Python',
        'learn':['flask','Django','Django_restframework'],
        'course_provider':'scaler'
    }
    return Response(courses)

# Create your views here.


@api_view(['POST'])
def login(request):
    data=request.data
    serializer=LoginSerializer(data=data)
    if serializer.is_valid():
        data=serializer.validated_data
        return Response({'message':'Success'})

    return Response(serializer.errors)

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method == 'GET':
        obj=Person.objects.all()
        serializer=PeopleSerializer(obj, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == "PUT":
        data=request.data
        obj2 = Person.objects.get(id=request.data.get('id'))  # Replace 'id' with the correct identifier
        data = request.data
        serializer = PeopleSerializer(instance=obj2, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method == "PATCH":
        data=request.data
        obj1=Person.objects.get(id=data['id'])
        serializer=PeopleSerializer(obj1,data=data , partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    else:
        data=request.data
        obj2=Person.objects.get(id=data['id'])
        obj2.delete()
        return Response({'Message':'Person Deleted Succesfully..'})

class PersonAPI(APIView):
    def get(self,request):
        obj=Person.objects.all()
        serializer=PeopleSerializer(obj, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def put(self,request):
        data=request.data
        obj2 = Person.objects.get(id=request.data.get('id'))  # Replace 'id' with the correct identifier
        data = request.data
        serializer = PeopleSerializer(instance=obj2, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    def patch(self,request):
        data=request.data
        obj1=Person.objects.get(id=data['id'])
        serializer=PeopleSerializer(obj1,data=data , partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request):
        data=request.data
        obj2=Person.objects.get(id=data['id'])
        obj2.delete()
        return Response({'Message':'Person Deleted Succesfully..'})


class Peopleview(viewsets.ModelViewSet):
    queryset=Person.objects.all()
    serializer_class=PeopleSerializer

    def list(self,request):
        search=request.GET.get('search')
        queryset=self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)
        serializer=PeopleSerializer(queryset,many=True)
        return Response({'status':200, 'data':serializer.data})
    