
from email import message
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import DestroyAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rooms.models import RoomType
from random import randint
from .models import User,RoomComment,FoodComment
from .utils import send_code_mail,send_mail
from food.models import Food
from .serializers import *
from .permissions import *
#-----------------------------------------------------------
messages_for_front = {
    'csrf_set' : 'اعتبارسنجی شد.',
    'national_duplicated' : 'کد ملی تکراری است.',
    'email_duplicated' : 'ایمیل تکراری است.',
    'user_create' : 'کاربر ساخته شد و کد اعتبارسنجی ارسال شد.',
    'user_not_found' : 'کاربر پیدا نشد.',
    'image_updated' : 'عکس پروفایل اپدیت شد.',
    'code_sent' : 'کد ارسال شد.',
    'password_changed' : 'پسورد با موفقیت تغییر کرد.',
    'wrong_coode' : 'کد اعتبارسنجی نامعتبر است.',
    'right_code' : 'کد اعتبارسنجی صحیح است.',
    'employee_create' : 'اکانت کارمند با موفقیت ساخته شد.',
    'sent_to_admin' : 'برای ادمین ارسال شد.',
    'room_not_found' : 'اتاق پیدا نشد.',
    'food_not_found' : 'غذا پیدا نشد.',
    'comment_create' : 'کامنت با موفقیت ایجاد شد.',
}
#-----------------------------------------------------------
"""
    api's in api_views.py :
    1- GetCSRFToken --> get crrf token for login

    2- UserCreateView --> Create User with Post Api
    3- UserDeleteView  --> delete a user with pk only for admins
    4- UserUpdateView --> update user information
    5- UserDetailPKView --> get a informations of a user with pk for admins
    6- UserDetailView --> get a informations of a user for self
    7- ProfileImageUpdateView  --> Update user image profile.

    8- PasswordChangeRequest  --> Password change request
    9- ChangePassword  --> It change user password if can_change_password is active.
    10- code_validation --> It checks whether the code is the same as the code in the database

    11- DashboardView  --> Dashboard api
    12- EmployeeListView --> Get all of employee informations.
    13- EmployeeCreateView  --> Create Employee with Post Api.
    14- UpdateRoleView --> Update role of user.

    15- ContactUs --> Update role of user.

    16- RoomCommentCreateView --> Create RoomComment with Post Api
    17- FoodCommentCreateView  --> Create FoodComment with Post Api
    18- CommentDeleteView --> Delete Comment with pk
    19- CommentUpdateView --> Update Comment with pk

    in urls for login:
    20- TokenObtainPairView
    21- TokenRefreshView
    
"""
#-----------------------------------------------------------
@method_decorator(ensure_csrf_cookie, name='dispatch')
class get_csrf_token(APIView):
    """
        Get And Set csrf cookie for FrontEnd(React)
        urls : domain.com/..../csrf/
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({'success': messages_for_front['csrf_set']})
#-----------------------------------------------------------
class UserCreateView(APIView):
    def post(self, request):
        """
        Create User with Post Api
        urls : domain.com/..../users/create/

        Sample json :
        {
        "email" : "TahaM8000@gmail.com",
        "nationalCode" : "0112037754",
        "firstName" : "Taha",
        "lastName" : "Mousavi",
        "password" : "1234jj5678"
        }

        """

        info = UserSerializer(data=request.data)
        code = randint(1000, 9999)

        if info.is_valid():
            # Check if the nationalCode is duplicated
            if User.objects.filter(nationalCode=info.validated_data['nationalCode']).exists():
                return Response({'message': messages_for_front['national_duplicated']}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the email is duplicated
            if User.objects.filter(email=info.validated_data['email']).exists():
                return Response({'message': messages_for_front['email_duplicated']}, status=status.HTTP_400_BAD_REQUEST)

            User(nationalCode=info.validated_data['nationalCode'],
                 email=info.validated_data['email'],
                 is_active=False,
                 firstName=info.validated_data['firstName'],
                 lastName=info.validated_data['lastName'],
                 code=code).save()

            user = User.objects.get(email=info.validated_data['email'])
            user.set_password(info.validated_data['password'])
            user.save()

            # send Code to User
            send_code_mail(info.validated_data['email'], code)

            return Response({'message': messages_for_front['user_create']}, status=status.HTTP_201_CREATED)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------
class UserDeleteView(DestroyAPIView):
    """
        delete a user with pk only for admins
        urls : domain.com/..../users/delete/<int:pk>/
    """
    permission_classes = [IsManager]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
#-----------------------------------------------------------
class UserUpdateView(UpdateAPIView):
    """
        update user information
        urls : domain.com/..../users/update/<int:pk>/
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        if 'password' in serializer.validated_data:
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()
#-----------------------------------------------------------
class UserDetailPKView(APIView):
    """
        get a informations of a user with pk for admins
        urls : domain.com/..../users/detail/<int:pk>/
    """
    permission_classes = [IsAuthenticated,IsManager]
    def get(self, request,pk):
        try:
            user = User.objects.get(id=pk)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_404_NOT_FOUND)
#-----------------------------------------------------------
class UserDetailView(APIView):
    """
        Get a informations of a user for self
        urls : domain.com/..../users/detail/
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_404_NOT_FOUND)
#-----------------------------------------------------------
class ProfileImageUpdateView(APIView):
    """
        Update user image profile.
        urls : domain.com/..../users/update/image/<int:pk>/
    """
    def put(self, request,pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'message': messages_for_front['user_not_found']},status=status.HTTP_404_NOT_FOUND) 
        serializer = UserImageSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': messages_for_front['image_updated'],'link':f"https://hotelback.iran.liara.run{user.image.url}"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------
class PasswordChangeRequest(APIView):
    def post(self, request):
        """
            Password change request
            urls : domain.com/..../users/update/password/
            Sample json :
            {
            "email" : "TahaM8000@gmail.com",
            }

        """

        info = PasswordChangeRequestSerializer(data=request.data)
        

        if info.is_valid():
            user = User.objects.get(email=info.validated_data['email'])

            user.can_change_password = True
            code = randint(1000, 9999)
            user.code = code
            user.save()

            # send Code to User
            send_code_mail(info.validated_data['email'], code)
            
            return Response({'message': messages_for_front['code_sent']}, status=status.HTTP_201_CREATED)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------
class ChangePassword(APIView):
    """
            It change user password if can_change_password is active.
            urls : domain.com/..../users/change/password/
            Sample json :
            {
            "email" : "TahaM8000@gmail.com",
            "password" : "338dsfs3fsaengh7",
            "code" : 7676
            }

    """
    def post(self, request):
        info = PasswordChangeSerializer(data=request.data)    

        if info.is_valid():
            user = User.objects.get(email=info.validated_data['email'])
            if (user.can_change_password):
                if(user.code == int(info.validated_data['code'])):
                    print(info.validated_data.get('password'))
                    user.set_password(info.validated_data.get('password'))
                    user.can_change_password = False
                    user.code = randint(1000, 9999)
                    user.save()

                    return Response({'message': messages_for_front['password_changed']}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': messages_for_front['wrong_coode']}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def code_validation(request):
    """
        It checks whether the code is the same as the code in the database
        urls : domain.com/..../users/validation/
        Sample json :
        {
        "email" : "TahaM8000@gmail.com",
        "code" : "8817"
        }

    """
    info = CodeValidationSerializers(data=request.data)

    if info.is_valid():
        user = User.objects.get(email=info.validated_data['email'])
        if (user.code == int(info.validated_data['code'])):
            
            user.is_active = True
            user.save()
            return Response({'message': messages_for_front['right_code']}, status=status.HTTP_200_OK)
        return Response({'message': messages_for_front['wrong_coode']}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------
class DashboardView(APIView):
    """
        dashboard api
        urls : domain.com/..../dashboard/
        Sample json :
            {
            "email" : "TahaM8000@gmail.com"
            }

    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        info = PasswordChangeRequestSerializer(data=request.data)    

        if info.is_valid():
            try:
                user = User.objects.get(email=info.validated_data['email'])
                serializer = UserDetailSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'detail': messages_for_front['user_not_found']}, status=status.HTTP_404_NOT_FOUND)
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------
class EmployeeListView(APIView):
    """
        get all of employee informations.
        urls : domain.com/..../employees/
        
    """
    permission_classes = [IsAuthenticated,IsHotelManager]

    def get(self, request):
        employees = User.objects.filter(Q(role='m') | Q(role='d') | Q(role='a')| Q(role='r'))
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#-----------------------------------------------------------
class EmployeeCreateView(APIView):
    """
        Create Employee with Post Api.
        urls : domain.com/..../employees/create/
        Sample json :
        {
        "email" : "TahaM8000@gmail.com",
        "nationalCode" : "0112037754",
        "firstName" : "Taha",
        "lastName" : "Mousavi",
        "password" : "1234jj5678",
        "role" : "m"
        }

    """
    permission_classes = [IsAuthenticated,IsHotelManager]
    def post(self, request):
        info = EmployeeCreateSerializer(data=request.data)

        if info.is_valid():
            # Check if the nationalCode is duplicated
            if User.objects.filter(nationalCode=info.validated_data['nationalCode']).exists():
                return Response({'message': messages_for_front['national_duplicated']}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the email is duplicated
            if User.objects.filter(email=info.validated_data['email']).exists():
                return Response({'message': messages_for_front['email_duplicated']}, status=status.HTTP_400_BAD_REQUEST)

            

            User(nationalCode=info.validated_data['nationalCode'],
                 email=info.validated_data['email'],
                 is_active=True,
                 is_admin=True,
                 firstName=info.validated_data['firstName'],
                 lastName=info.validated_data['lastName'],
                 role=info.validated_data['role'],
                ).save()

            user = User.objects.get(email=info.validated_data['email'])
            user.set_password(info.validated_data['password'])
            user.employee_id = user.id 
            user.save()


            return Response({'message': messages_for_front['employee_create']}, status=status.HTTP_201_CREATED)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#-----------------------------------------------------------
class UpdateRoleView(UpdateAPIView):
    """
        Update role of user.
        urls : domain.com/..../users/role/update/<int:pk>/
        Sample json :
        {
        "role" : "m"     
        }

    """
    permission_classes = [IsAuthenticated,IsHotelManager]
    queryset = User.objects.all()
    serializer_class = UpdateRoleSerializer
    lookup_field = 'pk'
#-----------------------------------------------------------
class ContactUs(APIView):
    """
        Update role of user.
        urls : domain.com/..../contact/email/
        Sample json :
        {
        'name' : 'ali',
        'email': 'alivahdani@gmail.com,
        'subject': 'bugs',
        'text': "bug description.'   
        }

    """
    def post(self,request):
        info = ContactUsSerializer(data=request.data)

        if info.is_valid():
           info.save()
           send_mail(info.validated_data['name'],info.validated_data['subject'],info.validated_data['text'],info.validated_data['email'])

           return Response({'message': messages_for_front['sent_to_admin']}, status=status.HTTP_201_CREATED) 

        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)

#-----------------------------------------------------------
class RoomCommentCreateView(APIView):
    """
        Create RoomComment with Post Api
        urls : domain.com/..../comments/room/create/
        Sample json :
        {
            'user_id': 2,
            'room_id': 3,
            'text': "text",
            'rating': 3   
        }        
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        info = RoomCommentCreateSerializer(data=request.data)

        if info.is_valid():
            try:
                user = User.objects.get(id=info.validated_data['user_id'])
            except User.DoesNotExist:
                return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_404_NOT_FOUND)

            try:
                room = RoomType.objects.get(id=info.validated_data['room_id'])
            except RoomType.DoesNotExist:
                return Response({'message': messages_for_front['room_not_found']}, status=status.HTTP_404_NOT_FOUND)

            
            room_cm = RoomComment(
                user = user,
                room = room,
                rating = info.validated_data['rating'],
                text = info.validated_data['text'],
            )
            room_cm.save()

            return Response({'message': messages_for_front['comment_create']}, status=status.HTTP_201_CREATED)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)    
#-----------------------------------------------------------
class FoodCommentCreateView(APIView):
    """
        Create FoodComment with Post Api
        urls : domain.com/..../comments/food/create/
        Sample json :
        {
            'user_id': 2,
            'food_id': 3,
            'text': "text",
            'rating': 3   
        } 
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        info = FoodCommentCreateSerializer(data=request.data)

        if info.is_valid():
            try:
                user = User.objects.get(id=info.validated_data['user_id'])
            except User.DoesNotExist:
                return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_404_NOT_FOUND)

            try:
                food = Food.objects.get(id=info.validated_data['food_id'])
            except Food.DoesNotExist:
                return Response({'message': messages_for_front['food_not_found']}, status=status.HTTP_404_NOT_FOUND)

            
            food_cm = FoodComment(
                user = user,
                food = food,
                rating = info.validated_data['rating'],
                text = info.validated_data['text'],
            )
            food_cm.save()

            return Response({'message': messages_for_front['comment_create']}, status=status.HTTP_201_CREATED)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST) 
#-----------------------------------------------------------
class CommentDeleteView(DestroyAPIView):
    """
        Delete Comment with pk
        urls : domain.com/..../comments/delete/pk/
    """
    permission_classes = [IsManager]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
#-----------------------------------------------------------
class CommentUpdateView(UpdateAPIView):
    """
        Update Comment with pk
        urls : domain.com/..../comments/update/pk/
    """
    permission_classes = [IsManager]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
#-----------------------------------------------------------