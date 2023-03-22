from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import (
    RegisterSerializer,
    LoginSerializer
)
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework_simplejwt.authentication import (
    JWTAuthentication
)
from django.db import IntegrityError

class RegisterView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response(
                    {
                        'data':serializer.errors,
                        'message':"something Went Wrong"
                    },status = status.HTTP_400_BAD_REQUEST
                    
                )
            
            serializer.save()
            return Response(
                {
                    'data':{},
                    'message':"Your account is created"
                },status = status.HTTP_201_CREATED
            )
        

        except Exception as e:
            print(e)
            return Response(
                    {
                        'data':{},
                        'message':"something Went Wrong"
                    },status = status.HTTP_400_BAD_REQUEST
                    
                )
        
    
        
    

        


class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response(
                    {
                        'data':serializer.errors,
                        'message':"something Went Wrong"
                    },status = status.HTTP_400_BAD_REQUEST
                    
                )
            response = serializer.get_jwt_token(serializer.data)
            return Response(response,status = status.HTTP_200_OK)
        
        except Exception as e:
            print("error=================",e)
            return Response(
                    {
                        'data':{},
                        'message':"something Went Wrong"
                    },status = status.HTTP_400_BAD_REQUEST
                    
                )
        
class Profile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        users = User.objects.all()
        user = request.user
        serializer = RegisterSerializer(user)
        return Response(serializer.data)
    


    def patch(self, request):
        try:
            #data = 0
            #user = request.user
            #user = User.objects.filter(id=data.get('id'))
            userid = request.user.id
            user = User.objects.get(pk=userid)
            data = request.data
            serializer = RegisterSerializer(user, data=data, partial=True, context={'request': request})

            #print("error=========================================",serializer.errors)
            print("new=============================", user)
            print("==================",serializer)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'user': serializer.data,
                        'message': "Your profile has been updated"
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'user': serializer.errors,
                        'message': "Your profile could not be updated"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )



            
        except IntegrityError:
            return Response(
                {
                    'user': None,
                    'message': "A user with that username already exists"
                },
                status=status.HTTP_409_CONFLICT
            )
        
        except Exception as e:
            print(e)
            return Response(
                {
                    'user': None,
                    'message': "An error occurred while updating your profile"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 
    


    
    # def patch(self, request):
    #     try:
            
    #         data = request.data
    #         user = User.objects.filter(id=request.user.id)
    #         serializer = RegisterSerializer(data = request.data)

    #         print("==================",serializer)

    #         if not user.exists():
    #             return Response(
    #                 {
    #                     'data':{},
    #                     'message':"invalid user"
    #                 },status = status.HTTP_400_BAD_REQUEST
    #             )


    #         if request.user != user.first():
    #             return Response(
    #                 {
    #                     'data':{},
    #                     'message':"you're not authorized to this"
    #                 },status = status.HTTP_400_BAD_REQUEST
    #             )
            
    #         serializer = RegisterSerializer(user[0], data=data, partial=True)
    #         if not serializer.is_valid():

    #             return Response(
    #                 {
    #                     'data':serializer.errors,
    #                     'message':"something Went Wrong"
    #                 },status = status.HTTP_400_BAD_REQUEST
                    
    #             )
            
    #         serializer.save()
    #         return Response(
    #             {
    #                 'user':{serializer.data},
    #                 'message':"Your prfile is updated"
    #             },status = status.HTTP_201_CREATED
    #         )
        

        
            
    #     except Exception as e:
    #         print(e)
    #         return Response(
    #                 {
    #                     'user':{},
    #                     'message':"something Went Wrong"
    #                 },status = status.HTTP_400_BAD_REQUEST
                    
    #             )
    