from django.db import models
from django.core.validators import RegexValidator


class Companys(models.Model):

    name = models.CharField(
        verbose_name = 'Company',
        max_length=100, 
        blank=False,
        null=False)
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companys'

    def __str__(self):
        return self.name

class Clients(models.Model):

    phone_regex = RegexValidator(regex=r'^\+?1?\d{11}$', message="Phone number must be entered in the format: '+99999999999'. Up to 15 digits allowed.")

    name = models.CharField(
        verbose_name = 'Name', 
        max_length=100, 
        blank=False,
        null=False)
    company = models.ForeignKey(
        Companys,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    email = models.EmailField(
        verbose_name = 'Email', 
        blank=True,
        null=True)
    phone = models.CharField(
        verbose_name = 'Phone', 
        validators=[phone_regex], 
        max_length=12, 
        blank=True,
        null=True)
    interests = models.CharField(
        verbose_name = 'Interests', 
        max_length=100, 
        blank=True,
        null=True)    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.name

    @classmethod
    def get_field_names_gen(cls):
        return filter(lambda x: x != 'id',[item.name for item in cls._meta.get_fields()])