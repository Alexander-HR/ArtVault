from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


def register(request):
    if request.method == "POST":
        print(1)
    else:
        return render(request, "user/register.hrml", {
            "form": UserCreationForm()
        })

@login_required
def profile_view(request):
    return render(request, "profile.html")
