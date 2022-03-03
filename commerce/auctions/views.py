from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import User, listing, bids, comments


def index(request):
    activelistings = listing.objects.all()
    return render(request, "auctions/index.html", {'listings': activelistings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def create(request): 
    if request.method == 'POST':
        # Retrieve inputs from form data
        name = request.POST["listingname"]
        value = request.POST["initialvalue"]
        desc = request.POST["description"]
        if not request.POST["imageurl"]:
            img = "/static/auctions/noimg.png"
        else:
            img = request.POST["imageurl"]

        # Retrieve user's current ID
        user = request.user
        id = user.id
        print(id)
        
        # Commit values to database
        dbcommit = listing(listingname=name, initialvalue = value, description = desc, imgurl = img, ownerid = id)
        dbcommit.save()
        return render(request, "auctions/index.html")
    else:
        form = listingform()
        return render(request, "auctions/create.html", {'form': form})

def display(request, id):
    return render(request, "auctions/display.html")



# Form classes

class listingform(forms.Form):
    listingname = forms.CharField(label='listing name', max_length='50', widget=forms.Textarea(attrs={'class':'form-control textbox', 'rows':1}))
    initialvalue = forms.DecimalField(label='initial price', decimal_places=2, max_digits=4000000, widget=forms.Textarea(attrs={'class':'form-control', 'rows':1}))
    description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class':'form-control', 'rows':1}))
    imageurl = forms.URLField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':1}), required=False)

class bidform(forms.Form):
    bidvalue = forms.DecimalField(decimal_places=2, max_digits=9)

class commentform(forms.Form):
    comment = forms.CharField(max_length=200)