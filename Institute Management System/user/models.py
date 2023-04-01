from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#   "Choice fields for Models"
choices = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7)
)

gender_choices = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others')
)
religion_choices = (
    ('Islam', 'Islam'),
    ('Hindu', 'Hindu'),
    ('Buddhist', 'Buddhist'),
    ('Christan', 'Christan')
)

department_choices = (
    ('Computer Science and Technology(85)', 'Computer Science and Technology(85)'),
    ('Computer Technology(66)', 'Computer Technology(66)'),
    ('Architecture and Interior Design Technology(87)', 'Architecture and Interior Design Technology(87)'),
    ('Civil Technology(64)', 'Civil Technology(64)'),
    ('Electrical  Technology(67)', 'Electrical  Technology(67)')
)

#   "End Choice Fields"


class UserManager(BaseUserManager):

    """Abstracting BaseUserManager for creating custom user system and
        custom login/superuser creating system."""

    def create_user(self, name, email, phone, password=None):
        if not name:
            raise ValueError('Name is required')
        if not email:
            raise ValueError('Email is required')
        user = self.model(
            name=name,
            email=self.normalize_email(email),
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, phone, password=None):
        user = self.create_user(
            name=name,
            email=self.normalize_email(email),
            phone=phone,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.is_teacher = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    """Abstracting BaseUser model to add custom fields to user model for System Quest."""

    name = models.CharField(verbose_name='Name', max_length=22)
    email = models.EmailField(verbose_name='Email Address', max_length=50, unique=True)
    phone = models.CharField(verbose_name='Phone Number', max_length=11, unique=True)

    # student data

    roll = models.CharField(verbose_name='Roll Number', max_length=6, unique=True, null=True)
    registration = models.CharField(verbose_name='Registration Number', max_length=15, null=True, unique=True)
    semester = models.IntegerField(verbose_name='Semester', choices=choices, null=True)
    department = models.CharField(verbose_name='Department', max_length=100, choices=department_choices, null=True)
    gender = models.CharField(verbose_name='Gender', max_length=20, choices=gender_choices, null=True)
    religion = models.CharField(verbose_name='Religion', max_length=20, choices=religion_choices, null=True)
    mother = models.CharField(verbose_name='Mother name', max_length=30, null=True, blank=True)
    father = models.CharField(verbose_name='Father name', max_length=30, null=True, blank=True)
    session = models.CharField(verbose_name='Session', max_length=20, null=True, blank=True)

    # permissions
    is_student = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    # staff permissions
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_hostel_manager = models.BooleanField(default=False)
    is_accountant = models.BooleanField(default=False)

    # extra facility
    in_hostel = models.BooleanField(default=False)
    father_is_dead = models.BooleanField(default=False)
    has_disability = models.BooleanField(default=False)
    special_discount = models.BooleanField(default=False)

    # if someone has quited or finished their diploma
    is_deafen = models.BooleanField(default=False)

    # for teacher only
    education = models.CharField(verbose_name='Education', max_length=100, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = UserManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):

    """Profile model to store user profile picture"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='profile_images')

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        image = Image.open(self.image.path)

        if image.width > 400 or image.height > 300:
            output_size = (400, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)


# Create your models here.

class AuthCodes(models.Model):

    """This model is for storing generated auth codes.
        When the code gets authorized , it flashes it's data automatically."""

    code = models.IntegerField()


class StudentList(models.Model):

    """This model will store roll number and registration number
        of all existing student in college."""

    roll = models.CharField(max_length=6, unique=True)
    registration = models.CharField(max_length=15)

    def __str__(self):
        return f'Roll {self.roll} Registration {self.registration}'
