from django.db import models
# abstractbaseuser is used for creating a custom user model in django, there is a need to define custom user field
# permissionsmixin is used to add permission to admin, user to your custom model
# used like use email instead of username for login
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name , password=None):
        """create a new user"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        # it will save encypyted password
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, name, password):
        user=self.create_user(email, name, password)

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self.db)

        return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email
