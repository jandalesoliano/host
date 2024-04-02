from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .forms import UserCredentialsForm, AddResultForm
from .models import UserCredentials
from .models import AddResult
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib import messages

# from django.contrib.auth.decorators import login_required


# Create your views here.

SESSION_KEY = 'is_admin_logged_in'
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

# @login_required
def home(request):
    username = request.session.get('username')
    if username is not None and username == DEFAULT_ADMIN_USERNAME:
        return redirect("admin-dashboard")
    elif  username is not None and UserCredentials.objects.filter(application_idU=username):
        username = request.session["username"]
        studentcreds = UserCredentials.objects.get(application_idU=username)
        f_name = studentcreds.first_name
        l_name = studentcreds.last_name
        return render(request, "student/dashboard.html", {'username': username, 'f_name': f_name, 'l_name': l_name})
    else:
        return render(request, 'login.html')
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not (username and password):  # Check if username or password is empty
            error_message = "Username or password cannot be empty."
            return render(request, "login.html", {"error_message": error_message})

        if username == DEFAULT_ADMIN_USERNAME and password == DEFAULT_ADMIN_PASSWORD:
            # Redirect to the admin dashboard
            request.session['username'] = username
            return redirect("admin-dashboard")
        elif UserCredentials.objects.filter(application_idU=username, password=password).exists():
            # Redirect to the user dashboard
            request.session['username'] = username
            studentcreds = UserCredentials.objects.get(application_idU=username, password=password)
            f_name = studentcreds.first_name
            l_name = studentcreds.last_name
            return render(request, "student/dashboard.html", {'username': username, 'f_name': f_name, 'l_name': l_name})
        else:
            # If credentials don't match, display an error message
            error_message = "Invalid username or password. Please try again."
            return render(request, "login.html", {"error_message": error_message})
    else:
        return render(request, "login.html")
    # if request.session.get('username') is not None and username == DEFAULT_ADMIN_USERNAME:
    #     return redirect("admin-dashboard")

    # if request.method == "POST":
        
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")

    #     # Kani nga code kay nag set ug session 
    #     request.session['username'] = username
    #     studentusername = request.session['username']
        
    #     # Check if the entered credentials match the default admin credentials
    #     if username == DEFAULT_ADMIN_USERNAME and password == DEFAULT_ADMIN_PASSWORD :
    #         # Redirect to the admin dashboard
    #         return redirect("admin-dashboard")
        
    #     else:
    #         # Check if the entered username exists in the database
    #         if UserCredentials.objects.filter(application_idU=username , password=password).exists():
    #             # Redirect to the user dashboard
    #             studentcreds = UserCredentials.objects.get(application_idU=username , password=password)
    #             f_name = studentcreds.first_name
    #             l_name = studentcreds.last_name                
                
    #             return render(request, "student/dashboard.html", {'username':studentusername, 'f_name':f_name, 'l_name':l_name})
    #         else:
    #             # If credentials don't match the admin's or user's, display an error message
    #             error_message = "Invalid username or password. Please try again."
    #             return render(request, "login.html", {"error_message": error_message})
    # else:
    #     return render(request, "login.html")
    


def admin_dashboard(request):
    # Your admin dashboard logic here
    
    # username = request.session.get('username')  # Using parentheses () instead of square brackets [] for get method
    # if username == DEFAULT_ADMIN_USERNAME and username is not None:  # Correcting syntax error "is not" instead of "and is not"
    #     return render(request, 'adminUser/dashboard.html')
    # else:
    #     return redirect('login')
    username = request.session.get('username')  # Using parentheses () instead of square brackets [] for get method
    
    if 'username' in request.session and username == DEFAULT_ADMIN_USERNAME:
        username = request.session['username']
        # Set a flag in the session to indicate the user is in the admin dashboard
        request.session['admin_dashboard'] = True

        courses = ['BEED', 'BSED-MATH', 'BTLED-HE', 'BSCS', 'BSES-CRM', 'BSHM']
        
        # Create a dictionary to store the counts of users for each course
        course_counts = {}

        # Query the database to get the count of users for each course
        for course in courses:
            course_counts[course] = UserCredentials.objects.filter(course_applied__iexact=course).count()
        print(course_counts)
        # Pass the course counts as context to the template
        context = {
            'username': username,
            'course_counts': course_counts,
        }

        
        return render(request, 'adminUser/dashboard.html', context)
    else:
        # Redirect to login if not authenticated
        return redirect('login')

        
def add_user(request):
    try:
        username = request.session.get('username')
        if username is not None and username == DEFAULT_ADMIN_USERNAME:
            users = UserCredentials.objects.all()
            return render(request, 'adminUser/addUser.html', {'users': users})    
        else:
            return redirect('login')  # Redirect to login if username is None
    except ObjectDoesNotExist:
        return redirect('login')
    
def handle_add_user(request):
    if request.method == "POST":
        form = UserCredentialsForm(request.POST)
        if form.is_valid():
            application_idU = form.cleaned_data['application_idU']
            if UserCredentials.objects.filter(application_idU=application_idU).exists():
                form.add_error('application_idU', 'User with the entered Application ID already exists.')
            else:
                form.save()
                # Add success message
                messages.success(request, 'User added successfully!')
                # After successfully adding a user, redirect back to the add_user view
                return redirect('add-user')
        else:
            print(form.errors)
    else:
        form = UserCredentialsForm()

    return render(request, 'adminUser/addUser.html', {'form': form})


def add_res(request):
    # Check if the user is authenticated
    username = request.session.get('username')
    if 'username' in request.session and username == DEFAULT_ADMIN_USERNAME:
        results = AddResult.objects.all()
        return render(request, 'adminUser/addResult.html', {'results': results})
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect('login')

def handle_add_res(request):

    if request.method == "POST":
        form = AddResultForm(request.POST)
        if form.is_valid():
            application_idR = request.POST.get('application_idR')
            if UserCredentials.objects.filter(application_idU=application_idR).exists():
                if AddResult.objects.filter(application_idR=application_idR).exists():
                    form.add_error('application_idR', 'Application ID already exists in the result database.')
                else:
                    form.save()
                    messages.success(request, 'result added successfully!')
                    return redirect('add-res')
                    
            else:
                form.add_error('application_idR', 'User with the entered Application ID does not exist.')
        else:
            return render(request, 'adminUser/addResult.html', {'form': form})
    else:
        form = AddResultForm()

    return render(request, 'adminUser/addResult.html', {'form': form})

        
def admin_logout(request):
    # Clear the session
    request.session.flush()
    logout(request)
    # Redirect to the login page
    return redirect("login")

def user_logout(request):
    # Clear the session
    logout(request)
    request.session.flush()
    # Redirect to the login page
    return redirect("login")