import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from engine.forms import AddImageForm
from .models import *
from rest_framework.parsers import MultiPartParser, FormParser

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
        form = AddImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            deta = dict(uploaded_file=form.cleaned_data["image"], course_code=form.cleaned_data["course"], data_list=form.cleaned_data["exam_details"])
            result = Student.student_create(**deta)
            print(result, 'eeeRRRORRR')
            if 'error' in result:
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                {'success': 'Students created successfully.'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'error' : form.errors
                },
                status=status.HTTP_200_OK
            )
            
        # image_file = request.FILES.get('image')
        # # print(data_list, 'data_list_str', 'internal', image_file, type(image_file), dir(image_file))
        # if form.is_valid():
        #     print('eeeee', form.cleaned_data["image"], data_list)
        #     deta = dict(uploaded_file=form.cleaned_data["image"], course_code="ELE5205")
        #     img = ImageCourse.save_uploaded_image(**deta)
        #     print(img)
        # else:
        #     print(form.errors)

        # if not data_list:
        #     return Response(
        #         {'error': 'Data list is required.'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # try:
        #     data_list = json.loads(data_list_str)
        # except json.JSONDecodeError:
        #     return Response(
        #         {'error': 'Invalid data list format.'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # result = Student.student_create(**data_list)
        # print("=========ERRROR========")
        # print(result)

        # if 'error' in result:
        #     return Response(
        #         {'error': result['error']},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )

        # return Response(
        #     {'success': 'Students created successfully.'},
        #     status=status.HTTP_201_CREATED
        # )


class StudentSeatAPIView(APIView):
    def get(self, request, format=None):
        registration_number = request.query_params.get('registration_number')
        course_code = request.query_params.get('course_code')

        print(registration_number, 'registration_number', 'course_code', course_code)

        if not registration_number:
            return Response(
                data={
                    'error': 'Registration number is a required field.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            student = Student.get_seat_number(registration_number=registration_number, course_code=course_code)
            image_course = ImageCourse.get_image_url_by_course_code(course_code=course_code)
            print(student, 'student============', student.exam.exam_date, image_course, 'PPPPPPPPPPPPP')
            if student:
                return Response(
                    data={
                        "student_seat_number": student.seat_number,
                        "student_registration_number": student.registration_number,
                        "exam_venue": student.exam.venue,
                        "exam_date": student.exam.exam_date,
                        "exam_time": student.exam.exam_time,
                        "course": student.course.code,
                        "image": image_course,
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