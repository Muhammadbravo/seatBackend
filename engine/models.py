from django.db import models
from django.db import transaction, IntegrityError
from datetime import datetime


class Course(models.Model):
    code = models.CharField(max_length=30, unique=True)

class Exam(models.Model):
    exam_date = models.DateField()
    exam_time = models.CharField(max_length=100)
    invigilators = models.CharField(max_length=200)
    enrolment = models.PositiveIntegerField()
    venue = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.course} - {self.exam_date}"



class Student(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    registration_number = models.CharField(max_length=20)

    class Meta:
        unique_together = ('exam', 'registration_number')

    def __str__(self):
        return f"Seat: {self.seat_number}, Registration: {self.registration_number}"
    
   
    @classmethod
    def student_create(cls, **kwargs):
        with transaction.atomic():
            try:
                exam_date = kwargs.pop("exam_date")
                update_date = datetime.strptime(exam_date, '%A %d-%m-%Y').date()
                course_code = kwargs["course"]
                exam = Exam.objects.create(
                    exam_date=update_date,
                    exam_time=kwargs["exam_time"],
                    invigilators=kwargs["invigilators"],
                    enrolment=kwargs["enrolment"],
                    venue=kwargs["venue"],
                )

                course = Course.objects.create(code=course_code)

                if exam and course:
                    registration_numbers = []
                    for data in kwargs["students"]:
                        seat_number, registration_number = data
                        if registration_number in registration_numbers:
                            return {'error': f"Duplicate registration number: {registration_number}."}
                        registration_numbers.append(registration_number)

                        existing_student = cls.objects.filter(registration_number=registration_number, course__code=course_code)
                        if existing_student.exists():
                            return {'error': f"Student with registration number {registration_number} already exists in the same course."}
                        cls.objects.create(exam=exam, seat_number=seat_number, registration_number=registration_number, course=course)
            except IntegrityError:
                return {'error': 'A student with the same registration number already exists.'}
            except Exception as e:
                # Handle other exceptions here
                error_message = str(e)
                return {'error': error_message}
        return {'success': 'Students created successfully.'}
    
    
    @classmethod
    def get_seat_number(cls, registration_number, course_code):
        try:
            student = cls.objects.select_related('exam', 'course').get(registration_number=registration_number, course__code=course_code)
            print(student, 'student', student, student.exam.exam_date)
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
    
