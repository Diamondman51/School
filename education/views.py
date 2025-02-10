import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views import View
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login, logout

from education.forms import AddManagerForm
from teacher.models import Group, GroupSpec, Student


@login_required(login_url='login')
def home(request):
    """
    This method handles the GET request for displaying the home page.

    Parameters:
    request (HttpRequest): The incoming request object containing user data and metadata.

    Returns:
    HttpResponse: A response object that renders the home page with recent students, total students, and courses.
    """
    query_set = Student.objects.all()
    new_students = query_set.order_by('-created_at')[:7]
    total_students = query_set.count()
    courses = GroupSpec.objects.all()
    context = {
        "new_students": new_students,
        "total_students": total_students,
        "courses": courses,
    }
    # time.sleep(50)
    return render(request, "home.html", context)


class Login(View):
    """
    This method handles the GET request for displaying the login form.

    Parameters:
    request (HttpRequest): The incoming request object containing user data and metadata.

    Returns:
    HttpResponse: A response object that renders the login page with the form.
    """
    def get(self, request):
        form = AuthenticationForm()
        context = {
            'form': form
        }
        return render(request, 'page-login.html', context)

    
    def post(self, request):
        """
        Handle POST request for user login.

        This method processes the submitted login form data, authenticates the user,
        and logs them in if the credentials are valid. If authentication is successful,
        the user is redirected to the home page. Otherwise, the login page is re-rendered
        with form errors.

        Parameters:
        request (HttpRequest): The HTTP POST request containing the form data.

        Returns:
        HttpResponse: A redirect to the home page if login is successful, or a rendered
                      login page with form errors if authentication fails.
        """
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():    
            email = form.cleaned_data.get("username", "")
            password = form.cleaned_data.get("password", "")
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request=request, user=user)
                return redirect("home")
        context = {
            'form': form
        }
        print(form.errors)
        return render(request, "page-login.html", context)



class AddManagerViewset(View):
    def get(self, request):
        """
        Handle GET request for displaying the manager registration form.

        This method renders the registration page with an empty form for adding a new manager.

        Parameters:
        request (HttpRequest): The HTTP GET request object.

        Returns:
        TemplateResponse: A response object that renders the registration page with the form.
        """
        form = AddManagerForm()
        context = {
            "form": form,
        }
        return TemplateResponse(request, "page-register.html", context)


    def post(self, request):
        """
        Handle POST request for adding a new manager.

        This method processes the submitted form data for creating a new manager account.
        If the form is valid, it saves the new manager and redirects to the login page.
        Otherwise, it re-renders the registration page with the form errors.

        Parameters:
        request (HttpRequest): The HTTP POST request containing the form data.

        Returns:
        HttpResponse: A redirect to the login page if successful, or a rendered
                      registration page with form errors if validation fails.
        """
        form = AddManagerForm(request.POST)
        if form.is_valid():
            # user = form.save(commit=False)
            # user.is_staff = True
            # user.save()
            form.save()
            return redirect('login')
        context = {
            'form': form,
        }
        return TemplateResponse(request, "page-register.html", context)



class LogOut(View):
    def get(self, request):
        """
        This method handles the GET request for logging out the user.

        Parameters:
        request (HttpRequest): The incoming request object containing user data and metadata.

        Returns:
        HttpResponseRedirect: A redirect response to the login page after successful logout.
        """
        logout(request)
        return redirect("login")

    