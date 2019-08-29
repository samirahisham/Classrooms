from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import Signup,Signin
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from .models import Classroom,Student
from .forms import ClassroomForm,StudentForm

def signup(request):
    form = Signup()
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("classroom-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)


def signin(request):
    form = Signin()
    if request.method == 'POST':
        form = Signin(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('classroom-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)


def signout(request):
	logout(request)
	return render(request,'signin.html')






def classroom_list(request):
	
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	
	classroom = Classroom.objects.get(id=classroom_id)
	student=Student.objects.all().filter(classroom=classroom)
	context = {
		"classroom": classroom,
		"student":student,
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	if not request.user.is_authenticated:
		messages.warning(request, "Please signin")
		return redirect('signin')
	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			Class=form.save(commit=False)
			Class.teacher=request.user
			Class.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user.is_authenticated or classroom.teacher==request.user.username):
		return redirect('warn')
	else:
		form = ClassroomForm(instance=classroom)
		if request.method == "POST":
			form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
			if form.is_valid():
				form.save()
				messages.success(request, "Successfully Edited!")
				return redirect('classroom-list')
			print (form.errors)
		context = {
		"form": form,
		"classroom": classroom,
		}
		return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user.is_authenticated or request.user==classroom.teacher):
		return redirect('warn')
	Classroom.objects.get(id=classroom_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')


#-----------------------------Student-------------------------------------
def student_create(request,classroom_id):
	classroom=Classroom.objects.get(id=classroom_id)
	if not (request.user.is_authenticated or request.user==classroom.teacher):
		return redirect('warn')
	
	form = StudentForm()
	if request.method == "POST":
		form = StudentForm(request.POST, request.FILES or None)
		if form.is_valid():
			stu=form.save(commit=False)
			stu.classroom=classroom
			stu.save()
			messages.success(request, "Successfully Added!")
			return redirect('classroom-detail',classroom.id)
		print (form.errors)
	context = {
	"form": form,
	'class':classroom,
	}
	return render(request, 'add_student.html', context)


def student_update(request, classroom_id,student_id):
	
	classroom=Classroom.objects.get(id=classroom_id)
	if not (request.user.is_authenticated or request.user==classroom.teacher):
		return redirect('warn')
	student = Student.objects.get(id=student_id)
	form = StudentForm(instance=student)
	if request.method == "POST":
		form = StudentForm(request.POST, request.FILES or None, instance=student)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-detail',classroom_id)
		print (form.errors)
	context = {
	"form": form,
	"student": student,
	"classroom":classroom,
	}
	return render(request, 'update_student.html', context)


def student_delete(request, classroom_id,student_id):
	classroom=Classroom.objects.get(id=classroom_id)
	if not (request.user.is_authenticated or request.user==classroom.teacher):
		return redirect('warn')
	stu=Student.objects.get(id=student_id)
	stu.delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-detail',classroom_id)

def warning(request,):
	
	messages.warning(request, "invaid access!")
	return render(request,"warning.html")