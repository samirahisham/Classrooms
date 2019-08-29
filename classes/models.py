from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import datetime


class Classroom(models.Model):
	name = models.CharField(max_length=120)
	subject = models.CharField(max_length=120)
	year = models.IntegerField()
	teacher=models.ForeignKey(User,on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('classroom-detail', kwargs={'classroom_id':self.id})
		
class Student(models.Model):
	name = models.CharField(max_length=120)
	date_of_birth = models.DateField()
	FEMALE="Female"
	MALE="Males"
	GENDERS=((FEMALE,"Female"),(MALE,"Male"))
	gender = models.CharField(max_length=9,choices=GENDERS) # a CharField with choices
	exam_grade= models.IntegerField()
	classroom= models.ForeignKey(Classroom,on_delete=models.CASCADE)#Foreignkey to the Classroom model