from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import project, contact, User
from .serializers import projectSerializers, contactSerializers, UserCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from datetime import datetime
from django.db import transaction


# project view
class projectAPI(APIView):
    def get(self, request):
        try:
            queryset = project.objects.all()
            
            # pagination
            paginator = PageNumberPagination()
            paginator.page_size = 6 
            result_page = paginator.paginate_queryset(queryset, request)

            serializer = projectSerializers(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return self.create_error_response(f'An error occurred: {str(e)}')

    
    def create_error_response(self,message):
        return Response({'error': message})
    

    def post(self, request):
        name = request.data.get("name")
        project_description = request.data.get("project_description")
        project_link = request.data.get("project_link")
        project_image = request.FILES.get("project_image")  

      
        # if not name or not project_description or not project_image:
        #     return self.create_error_response("All fields (except image) are required.")

        try:
            project_obj = project.objects.create(
                name=name,
                project_description=project_description,
                project_link=project_link,
                project_image=project_image
            )
            serialized_data = projectSerializers(project_obj).data
            return self.create_success_response(serialized_data)
        except Exception as e:
            return self.create_error_response(f"An error occurred: {str(e)}")

    def create_success_response(self, data):
        return Response({"data": data}, status=status.HTTP_201_CREATED)

    def create_error_response(self, message):
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        id = request.data.get("id")
        name = request.data.get("name")
        project_description = request.data.get("project_description")
        project_link = request.data.get("project_link")
        project_image = request.FILES.get("project_image") 

        try:
            project_obj = project.objects.get(pk=id)

            if name:
                project_obj.name = name
            if project_description:
                project_obj.project_description = project_description
            if project_link:
                project_obj.project_link = project_link
            if project_image:
                project_obj.project_image = project_image

            serializer = projectSerializers(project_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.create_success_response(serializer.data)
            else:
                return self.create_error_response(serializer.errors)

        except project.DoesNotExist:
            return self.create_error_response("Project not found.")
        except Exception as e:
            return self.create_error_response(f"An error occurred: {str(e)}")

    def delete(self,request,pk=None):
        try:
            project_obj = project.objects.get(pk=pk)
            project_obj.delete()
            return self.create_success_response("Project deleted successfully.")
        except project.DoesNotExist:
            return self.create_error_response("Project not found.")
        except Exception as e:
            return self.create_error_response(f"An error occurred: {str(e)}")

    def create_success_response(self, data):
        return Response({"data": data}, status=status.HTTP_200_OK)

    def create_error_response(self, message):
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


# contact view


class contactAPI(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [AllowAny()]
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            data_queryset = contact.objects.all()
            data_queryset = contactSerializers(data_queryset, many=True).data
            return self.create_success_response(data_queryset)
        except Exception as e:
            return self.create_error_response(f"An error occurred: {str(e)}")

    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        suggestion = request.data.get("suggestion")
        rating = request.data.get("rating")

        if not name or not email or not rating:
            return self.create_error_response("Name, email, and rating are required.")

        try:
            contact_obj = contact.objects.create(
                name=name,
                email=email,
                suggestion=suggestion,
                rating=rating
            )
            serialized_data = contactSerializers(contact_obj).data
            return self.create_success_response(serialized_data)
        except Exception as e:
            return self.create_error_response(f"An error occurred: {str(e)}")

    def patch(self, request):
        id = request.data.get("id")
        name = request.data.get("name")
        email = request.data.get("email")
        suggestion = request.data.get("suggestion")
        rating = request.data.get("rating")

        try:
            contact_obj = contact.objects.get(pk=id)

            if name:
                contact_obj.name = name
            if email:
                contact_obj.email = email
            if suggestion is not None:
                contact_obj.suggestion = suggestion
            if rating:
                contact_obj.rating = rating

            serializer = contactSerializers(contact_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return self.create_success_response(serializer.data)
            else:
                return self.create_error_response(serializer.errors)

        except contact.DoesNotExist:
            return self.create_error_response("Contact not found.")
        except Exception as e:
            return self.create_error_response(f"An error occurred: {str(e)}")

    def delete(self, request, pk=None):
        try:
            contact_obj = contact.objects.get(pk=pk)
            contact_obj.delete()
            return self.create_success_response("Contact deleted successfully.")
        except contact.DoesNotExist:
            return self.create_error_response("Contact not found.")
        except Exception as e:
            return self.create_error_response(f"An error occurred: {str(e)}")

    def create_success_response(self, data):
        return Response({"data": data}, status=status.HTTP_200_OK)

    def create_error_response(self, message):
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
    
    
# user view

class LoginView(APIView):
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        otp = request.data.get("otp")
        action = request.data.get("action")
        # domain = request.data.get("domain")
        user = None

        try:
            response = Response()
            response.data = {}
            # OTP login action
            if action == "otp":
                if not email:
                    return Response({"message": "Mobile number is required"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = User.objects.filter(mobile=email).first()
                if not user:
                    return Response({"message": "User does not exist or Check Domain"}, status=status.HTTP_404_NOT_FOUND)

                # If OTP is provided, verify it
                if otp:
                    # url = f"https://control.msg91.com/api/v5/otp/verify?mobile=91{email}&otp={otp}"
                    # response = SendMessage.send_message(url=url)
                    json = response.json()
                    if json["type"] == "success":
                        # Generate tokens for user after successful OTP verification
                        token = self.get_tokens_for_user(user)
                        access_token = token["access"]
                        refresh_token = token["refresh"]
                        response = Response({
                            "refresh_token": refresh_token,
                            "access_token": access_token,
                        })
                        response.set_cookie(
                            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                            value=str(access_token),
                            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]
                        )
                        response.set_cookie(
                            key='refresh_token',
                            value=refresh_token,
                            expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                            httponly=True,
                            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]
                        )
                        user.last_login = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                        user.save()
                        return response
                    else:
                        return Response({"message": json["message"]}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Send OTP if no OTP is provided
                    # url = f"https://control.msg91.com/api/v5/otp?mobile=91{email}&template_id={MSG91_TEMPLATE_ID}"
                    # response = SendMessage.send_message(url=url)
                    json = response.json()
                    if json["type"] == "success":
                        return Response({'message': "OTP sent successfully"})
                    else:
                        return Response({'message': json["message"]}, status=status.HTTP_400_BAD_REQUEST)
            elif email and password:
                if '@' in email:
                    user = User.objects.filter(email=email).first()
                else:
                    user = User.objects.filter(mobile=email).first()
                # # Check if the provided input is an email address
                # if '@' in email:
                #     if domain == "doctor":
                #         user = User.objects.filter(email=email, is_doctor=True).first()
                #     elif domain == "receptionist":
                #         user = User.objects.filter(email=email).first()
                #     else:
                #         return Response({"message": "Invalid domain provided."}, status=status.HTTP_400_BAD_REQUEST)
                # else:
                #     if domain == "doctor":
                #         user = User.objects.filter(mobile=email, is_doctor=True).first()
                #     elif domain == "receptionist":
                #         user = User.objects.filter(mobile=email, is_receptionist=True).first()
                #     else:
                #         return Response({"message": "Invalid domain provided."}, status=status.HTTP_400_BAD_REQUEST)

                if user is not None and user.check_password(password):
                    token = self.get_tokens_for_user(user)
                    access_token = token["access"]
                    refresh_token = token["refresh"]
                    response.data["refresh_token"] = refresh_token
                    response.data["access_token"] = access_token
                    # response.data["user"] = self.get_user(user)
                    response.set_cookie(
                        key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                        value=str(access_token),
                        expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]
                    )
                    response.set_cookie(
                        key='refresh_token',
                        value=refresh_token,
                        expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                        httponly=True,
                        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]
                    )
                    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                    user.last_login = current_time
                    user.save()
                    return response
                else:
                    return Response(data={"message": "Invalid Password or Domain"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={"message": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(data={"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    """New User Registers"""
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def get_user(self, user):
        serialize = UserCreateSerializer(user)  # Replace with your actual Userserializer # noqa
        return serialize.data

    def post(self, request, *args, **kwargs):
        # Your custom logic before creating a new user
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        mobile_number = request.data.get('mobile')
        password = request.data.get("password1")
        password_confirm = request.data.get("password2")
        # language = request.data.get("language", "")
        # otp = request.data.get("otp")  # Assuming OTP is passed in the request
        # if not otp:
        #     return Response({"message": "OTP not provided"}, status=status.HTTP_400_BAD_REQUEST)
        # if len(password) < 6 or len(password) > 12:
        #     return Response({"message": "Password length should be between 6 and 12 characters."}, status=status.HTTP_400_BAD_REQUEST)
        # if password != password_confirm:
        #     return Response({"message": "Password and password_confirm not matching"}, status=status.HTTP_400_BAD_REQUEST)
        # Generate email based on mobile number
        email = request.data.get("email")
        # url = f"https://control.msg91.com/api/v5/otp/verify?otp={otp}&mobile=91{mobile_number}"
        # response = SendMessage.send_message(url=url)
        # json = response.json()
        # if json["type"] == "success" or (json["type"] == "error" and json["message"] == "Mobile no. already verified"):
        if User.objects.filter(email=email).exists():
            return Response({"message": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # User object creation
        try:
            with transaction.atomic():
                user_obj = User(
                    first_name=first_name.title(),
                    last_name=last_name.title(),
                    email=email,
                    mobile=mobile_number,
                    # language=language
                )

                # Set password if provided
                if password == password_confirm:
                    user_obj.set_password(password)

                # Save user object
                user_obj.save()

                # # Add user roles after saving user object
                # roles = Roles.objects.filter(pk__in=role)
                # user_obj.user_role.add(*roles)

                # Add linked doctors and clinics
               
                # if linked_clinics:
                #     user_obj.linked_clinics.add(*linked_clinics)

                # Generate tokens
                token = self.get_tokens_for_user(user_obj)
                # if user_details:
                #     patients_objs = []
                #     for obj in user_details:
                #         # Update family_id with mobile number
                #         obj.update({
                #             "user": user_obj,
                #             "family_id": mobile_number,
                #             "phone": mobile_number
                #         })
                #         patients_objs.append(Patients(**obj))

                #     logger.info(f"User Details:{user_details}")
                #     # Using bulk_create to insert multiple records in a single query
                #     Patients.objects.bulk_create(patients_objs)

            response = Response()
            response.data = {}
            if token:
                response.data.update(token)
            response.data["user"] = self.get_user(user_obj)
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=token["access"],
                expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]
            )
            # Log additional information
            # logger.info(f"User {email} registered successfully.")

            return Response(data={"data": response.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Something went wrong!", "error_msg": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

