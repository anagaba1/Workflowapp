
# Create your views here.
# school/views.py
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_student')  # Redirect to a success URL after successful registration
    else:
        form = StudentRegistrationForm()
    return render(request, 'register_student.html', {'form': form})
