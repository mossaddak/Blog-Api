from .models import (
    Blog,
    Comment
)
from rest_framework.viewsets import (
    ModelViewSet
)
from .serializer import (
    BlogSerializer,
    CommentSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import (
    permissions
)
from rest_framework.response import (
    Response
)
from rest_framework import (
    status
)
from django.db.models import (
    Q
)
from rest_framework.views import (
    APIView
)
from django.core.paginator import Paginator
from django.http import Http404


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True
        return obj.user == request.user

    # def has_permission(self, request, view):
    #     user = request.user

    #     if request.method == 'GET':
    #         return True

    #     if request.method in['POST','PUT','DELETE'] and user.is_superuser:
    #         return True
    #     return False


class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)
            serializer = BlogSerializer(blogs, many=True)
            return Response(
                    {
                        'blogs':serializer.data,
                        'message':"blogs fetch successfully"
                    },status = status.HTTP_200_OK
                    
                )

        except Exception as e:
            print(e)

    
    def post(self, request):
        try:
            data = request.data
            data['user']=request.user.id
            serializer = BlogSerializer(data=data)

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
                    'data':serializer.data,
                    'message':"blog created"
                },status = status.HTTP_201_CREATED
            )


        except Exception as e:
            return Response(
                    {
                        'data':{},
                        'message':"something Went Wrong"
                    },status = status.HTTP_400_BAD_REQUEST
                    
                )
        
    

    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(id=data.get('id'))

            if not blog.exists():
                return Response(
                    {
                        'data':{},
                        'message':"invalid blog id"
                    },status = status.HTTP_400_BAD_REQUEST
                )


            if request.user != blog[0].user:

                return Response(
                    {
                        'data':{},
                        'message':"you're not authorized to this"
                    },status = status.HTTP_400_BAD_REQUEST
                )
            
            serializer = BlogSerializer(blog[0], data=data, partial=True)

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
                    'data':serializer.data,
                    'message':"blog updated"
                },status = status.HTTP_201_CREATED
            )


            
            
        except Exception as e:
            return Response(
                    {
                        'data':{},
                        'message':"something Went Wrong"
                    },status = status.HTTP_400_BAD_REQUEST
                    
                )
        

    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(id=data.get('id'))

            if not blog.exists():
                return Response(
                    {
                        'data':{},
                        'message':"invalid blog id"
                    },status = status.HTTP_400_BAD_REQUEST
                )


            if request.user != blog[0].user:

                return Response(
                    {
                        'data':{},
                        'message':"you're not authorized to this"
                    },status = status.HTTP_400_BAD_REQUEST
                )
            
            blog[0].delete()
            return Response(
                {
                    'data':{},
                    'message':"blog deleted"
                },status = status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return Response(
                    {
                        'data':{},
                        'message':"something Went Wrong"
                    },status = status.HTTP_400_BAD_REQUEST
                    
                )
        

class PublicBlog(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.all()

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(desc__icontains=search))

            page_number = request.GET.get('page', 1)
            pagiantor = Paginator(blogs, 6)
            serializer = BlogSerializer(pagiantor.page(page_number), many=True)

            # Generate absolute URL for image
           

            return Response(
                    {
                        'blogs':serializer.data,
                        'message':"blogs fetch successfully"
                    },status = status.HTTP_200_OK
                    
                )

        except Exception as e:
            print(e)

            return Response(
                    {
                        'blogs':[],
                        'message':"Error occurred while fetching blogs"
                    },status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            


class BlogDetails(APIView):
    
    def get(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
            serializer = BlogSerializer(blog)
            return Response(
                {
                    'data':serializer.data,
                    'message':"blogs fetch successfully"
                },status = status.HTTP_200_OK
            
            )
             
        except Blog.DoesNotExist:
            raise Http404
        

class Comment(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    authentication_classes=[JWTAuthentication]
    permission_classes = [IsOwnerOrAdminOrReadOnly]