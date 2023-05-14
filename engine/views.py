import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student

# class StudentCreateAPIView(APIView):
#     def post(self, request, format=None):
#         registration_number = request.data.get('registration_number')
#         seat_number = request.data.get('seat_number')

#         if not registration_number or not seat_number:
#             return Response(
#                 {'error': 'Registration number and seat number are required fields.'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         student = Student(registration_number=registration_number, seat_number=seat_number)
#         student.save()

#         return Response(
#             {'success': 'Student created successfully.'},
#             status=status.HTTP_201_CREATED
#         )
# class StudentCreateAPIView(APIView):
#     def post(self, request, format=None):
#         data_list = request.data.get('data_list')
#         print(data_list, 'data_list')

#         if not data_list:
#             return Response(
#                 {'error': 'Data list is required.'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         result = Student.student_create(data_list)

#         if 'error' in result:
#             return Response(
#                 {'error': result['error']},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         return Response(
#             {'success': 'Students created successfully.'},
#             status=status.HTTP_201_CREATED
#         )

class StudentCreateAPIView(APIView):
    def post(self, request, format=None):
        data_list = request.data.get('data_list')
        print(data_list, 'data_list_str')

        if not data_list:
            return Response(
                {'error': 'Data list is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # try:
        #     data_list = json.loads(data_list_str)
        # except json.JSONDecodeError:
        #     return Response(
        #         {'error': 'Invalid data list format.'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        result = Student.student_create(data_list)

        if 'error' in result:
            return Response(
                {'error': result['error']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {'success': 'Students created successfully.'},
            status=status.HTTP_201_CREATED
        )


class StudentSeatAPIView(APIView):
    def get(self, request, format=None):
        registration_number = request.query_params.get('registration_number')

        print(registration_number, 'registration_number')

        if not registration_number:
            return Response(
                data={
                    'error': 'Registration number is a required field.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            student = Student.get_seat_number(registration_number=registration_number)
            print(student, 'student============')
            if student:
                return Response(
                    data={
                        "student_seat_number": student.seat_number,
                        "student_registration_number": student.registration_number,
                        "message": "Student registration number retrieved.",
                        'status': True
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data={
                        'error': 'Student not found.',
                        'status': False
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                data={
                    'error': 'An error occurred.',
                    'status': False
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )