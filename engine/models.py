from django.db import models
from django.db import transaction




class Student(models.Model):
    seat_number = models.CharField(max_length=10)
    registration_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Seat: {self.seat_number}, Registration: {self.registration_number}"
    
    @classmethod
    def student_create(cls, data_list):
        with transaction.atomic():
            try:
                for data in data_list:
                    print(data, 'data')
                    seat_number, registration_number = data
                    cls.objects.create(seat_number=seat_number, registration_number=registration_number)
            except Exception as e:
                # Handle the exception here (e.g., logging, error message)
                error_message = str(e)
                return {'error': error_message}
        return {'success': 'Students created successfully.'}
    
    
    @classmethod
    def get_seat_number(cls, registration_number):
        try:
            student = cls.objects.get(registration_number=registration_number)
            print(student, 'student============')
            return student
        except cls.DoesNotExist:
            return None
        except Exception as e:
            print(e, 'error')
            return None

# Create your models here.

# class StudentManager(models.Manager):
#     def create_student(self, seat_number, registration_number):
#         student = self.create(seat_number=seat_number, registration_number=registration_number)
#         return student


# class Student(models.Model):
#     seat_number = models.CharField(max_length=3)
#     registration_number = models.CharField(max_length=20)

#     objects = StudentManager()

#     def __str__(self):
#         return f"Seat: {self.seat_number}, Registration: {self.registration_number}"
   
#     @classmethod
#     def get_seat_number(cls, registration_number):
#         try:
#             student = cls.objects.get(registration_number=registration_number)
#             print(student)
#             return student.seat_number
#         except cls.DoesNotExist:
#             return None
    
