from django.db import models
from django.db import transaction, IntegrityError
from datetime import datetime
from cloudinary.models import CloudinaryField
from django.core.files.base import ContentFile
import base64

class Course(models.Model):
    code = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.code

class Exam(models.Model):
    exam_date = models.CharField(max_length=200)
    exam_time = models.CharField(max_length=100)
    invigilators = models.CharField(max_length=200)
    enrolment = models.PositiveIntegerField()
    venue = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.exam_date}"



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
        print(kwargs, 'kwargs')
        with transaction.atomic():
            try:
                # exam_date = kwargs.pop("exam_date")
                course = None
                image = kwargs.pop("uploaded_file")
                course_selected = kwargs.pop("course_code")
                # update_date = datetime.strptime(exam_date, '%A %d-%m-%Y').date()
                course_code = kwargs['data_list']["course"]
                exam = Exam.objects.create(
                    # exam_date=exam_date,
                    exam_date=kwargs['data_list']["exam_date"],
                    exam_time=kwargs['data_list']["exam_time"],
                    invigilators=kwargs['data_list']["invigilators"],
                    enrolment=kwargs['data_list']["enrolment"],
                    venue=kwargs['data_list']["venue"],
                )

                print("hety", course)
                if not course:
                    course = Course.objects.create(code=course_code)
                else:
                    course = Course.objects.get(code=course_code)

                image = ImageCourse.save_uploaded_image(uploaded_file=image, course_code=course)
                print('==BEFORE IF=======')
                print(course)
                if exam and course:
                    print(course, 'after')
                    registration_numbers = []
                    for data in kwargs['data_list']["students"]:
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


class ImageCourse(models.Model):
    # image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    image = CloudinaryField(blank=True, null=True)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


    @classmethod
    def save_uploaded_image(cls, **kwargs):
        # Extract the necessary parameters from kwargs
        uploaded_file = kwargs.get("uploaded_file")
        course_code = kwargs.get("course_code")
        course = Course.objects.get(code=course_code)
        image_course = cls(image=uploaded_file, course=course)

            # Save the model instance
        image_course.save()

        return image_course

    @classmethod
    def get_image_url_by_course_code(cls, course_code):
        try:
            image_course = cls.objects.get(course__code=course_code)
            return image_course.image_url()
        except cls.DoesNotExist:
            return None
        # else:
        #     raise ValueError("Missing required parameters: uploaded_file and course_code.")
    # @classmethod
    # def save_uploaded_image(cls, **kwargs):
    #     # Extract the necessary parameters from kwargs
    #     uploaded_file = kwargs.get("uploaded_file")
    #     course_code = kwargs.get("course_code")

    #     print(uploaded_file, 'upload', 'course code', course_code, type(uploaded_file))

    #     if uploaded_file and course_code:
    #         file_chunks = uploaded_file.chunks()
    #         first_chunk = next(file_chunks)
            
    #         # Retrieve the course instance
    #         try:
    #             course = Course.objects.get(code=course_code)
    #         except Course.DoesNotExist:
    #             raise ValueError("Course with code '{}' does not exist.".format(course_code))

    #         # Create an instance of ImageCourse
    #         image_course = cls(image=first_chunk, course=course)

    #         # Save the model instance
    #         image_course.save()

    #         return image_course
    #     else:
    #         raise ValueError("Missing required parameters: uploaded_file and course_code.")
    
    # @classmethod
    # def save_uploaded_image(cls, **kwargs):
    #     # Read the file content
    #     print(kwargs)
    #     uploaded_file = kwargs["uploaded_file"]
    #     course_code = kwargs["course_code"]
    #     file_content = uploaded_file.read()

    #     # Create a ContentFile object from the file content
    #     content_file = ContentFile(file_content)

    #     # Create an instance of ImageCourse
    #     course = Course.objects.get(code=course_code)
    #     get_item = dict(image=content_file, course=course)
    #     image_course = cls.objects.create(**get_item)
        # print('course', course)
        # image_course = cls(course=course)
        # print(image_course)

        # # Assign the content file to the image field
        # image_course.image.save(uploaded_file.name, content_file)

        # # Save the model instance
        # image_course.save()
        
        # return image_course
    
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
    
