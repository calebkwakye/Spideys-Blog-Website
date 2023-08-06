from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()

            # Send the welcome email
            subject = "Welcome to Spidey's Dispatch"
            email_template = 'email/welcome_email.html'
            context = {'user': user}
            message = render_to_string(email_template, context)
            plain_message = strip_tags(message)

            send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=message)

            return redirect('login')  # Redirect to a success page or login page
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
