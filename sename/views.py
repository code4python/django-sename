from django.shortcuts import render
from .models import *
from django.http.response import JsonResponse 
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status , filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics , mixins ,viewsets
from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

# Create your views here.
#1 rest-no-db and no model query:
def rest_no_model(request):
    guest = [
        {
           'name':'ahmed',
           'mobile':'1255444',
        },
        {
            'name':'omer',
            'mobile':'258487'   
        },
        {
            'name':'ali',
            'mobile':'2584287'   
        }
        
    ]
    return JsonResponse(guest ,safe=False)

#2 model date defult django without rest
def model_no_rest(request):
    date = Guest.objects.all()
    response = {
        'guests': list(date.values('name','mobile'))
    }
    return JsonResponse(response)

#List == GET
#Create == POST
#Pk query == GET
#Update == PUT
#Delete destroy == DELETE


#3 Function based views
#3.1 GET POST

@api_view(['GET','POST'])
def FBV_List(request):   

    #GET
    if request.method =='GET':
        guests = Guest.objects.all()
        data = GuestSerializer(guests , many=True).data
        return Response({'data':data})
    
    elif request.method == 'POST':
        data = GuestSerializer(data= request.data)
        if data.is_valid():
            data.save()
            return Response(data.data , status= status.HTTP_201_CREATED)
        return Response(data.data , status=status.HTTP_400_BAD_REQUEST)

#3.2 GET PUT DELETE
@api_view(['GET','PUT' ,'DELETE'])
def FBV_pk(request ,id):
    try: 
        guest = Guest.objects.get(id=id)
    except Guest.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    #GET
    if request.method =='GET':
        data = GuestSerializer(guest)
        return Response(data.data)
    #PUT
    elif request.method == 'PUT':
        data = GuestSerializer(guest ,data= request.data)
        if data.is_valid():
            data.save()
            return Response(data.data)
        return Response(data.errors,status=status.HTTP_400_BAD_REQUEST)
    #DELETE
    if request.method =='DELETE': 
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#4.1 Class Based Views as ApiViews:

class Cbv_List(APIView):
    def get(self, request):
        data = Guest.objects.all()
        serializer = GuestSerializer(data , many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = GuestSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


#4.2 GET PUT DELETE
class CVB_pk(APIView):
    def get_object(self ,id):
        try:
            return Guest.objects.get(id=id)
        except Guest.DoesNotExist:
            raise Http404
    #get
    def get(self ,request ,id):
        guest = self.get_object(id)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    #put
    def put(self, request, id):
        guest = self.get_object(id)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    #delete
    def delete(self, request, id):
        serializer = self.get_object(id)
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
 
#5 mixins
#5.1 mixins list
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)

#5.2 mixins get put delete:
class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
    def get(self, request ,pk):
        return self.retrieve(request)
    def put(self, request, pk):
        return self.update(request)
    def delete(self, request, pk):
        return self.destroy(request)

    
#6 Genarics
#6.1 get and post

class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]    
#6.2 get put delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    

#7 viewsets

class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    
   
   
class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    filter_backends = [filters.SearchFilter]  
      
      
class viewsets_resv(viewsets.ModelViewSet):
    queryset = Reservtion.objects.all()
    serializer_class = ReservationSerializer
  
  
    
# find movie
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies ,many =True)
    return Response(serializer.data)

#Create Reservation

@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    guest = Guest()
    guest.name = request.data['name'],
    guest.mobile = request.data['mobile'],
    guest.save()
    
    reservation = Reservtion()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    return Response(status=status.HTTP_201_CREATED)


#10 post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer