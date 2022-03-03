import http, re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import User, listing, bids, comments, watchlist


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
        dbcommit = listing(listingname=name, initialvalue = value, description = desc, imgurl = img, ownerid = id, active = "True")
        dbcommit.save()
        activelistings = listing.objects.all()
        return render(request, "auctions/index.html", {'listings': activelistings})
    else:
        form = listingform()
        return render(request, "auctions/create.html", {'form': form})

def display(request, id):
    # Query table using listing ID
    item = listing.objects.filter(id=id)
    # Create bid form
    form = bidform()
    # Query listing creator's username
    owner = User.objects.filter(id=item[0].ownerid)
    # Check if the owner is also the currently logged in user
    user = request.user
    userid = user.id
    # Check if listing is currently active, if so display option to close listing
    if item[0].active == False:
        archive = ""
        pass
    else:
        if userid == item[0].ownerid:
            archive = "Click here to close listing"
        else:
            archive = ""
    # Check if listing is on watchlist and change text appropiately 
    try:
        query=watchlist.objects.get(listingid = id, userid = userid)
        if query.active == True:
            watch = "Remove from watchlist" 
        else:
            watch = "Add to watchlist" 
    except:
        watch = "Add to watchlist"

    # If bid is submitted, validate response and update bid value.
    if request.method == "POST":
        newbid = float(request.POST["bidvalue"])
        # Retrieve current bid value
        bidquery = listing.objects.get(id=id)
        currentbid = float(bidquery.initialvalue)
        # If newbid is higher than current bid, update value
        if newbid > currentbid:
            bidquery.initialvalue = request.POST["bidvalue"]
            bidquery.save()
        # Otherwise, return an error
        else:     
            form = bidform()
            return render(request, "auctions/display.html", {'item': item[0], 'form': form, 'owner': owner[0].username, 'watch': watch, 'id': id, 'error': "Error: Please enter a bid greater than the current value", 'archive': archive})

        
        # Retrieve updated info for listing
        item = listing.objects.filter(id=id)      
        form = bidform()
        return render(request, "auctions/display.html", {'item': item[0], 'form': form, 'owner': owner[0].username, 'watch': watch, 'id': id, 'archive': archive})

    else:
        # Query table using listing ID
        item = listing.objects.filter(id=id)
        # Create bid form
        form = bidform()
        return render(request, "auctions/display.html", {'item': item[0], 'form': form, 'owner': owner[0].username, 'watch': watch, 'id': id, 'archive': archive})

@login_required(login_url='login')
def watch(request):
    # Take the Listing ID that watchlist was visited from
    # https://stackoverflow.com/questions/27325505/django-getting-previous-url
    page = str(request.META.get('HTTP_REFERER'))
    # Split string to access only the ID
    # https://www.kite.com/python/answers/how-to-remove-all-non-numeric-characters-from-a-string-in-python
    listingid = page.rsplit("/", 1)[1]

    # Get current user ID 
    user = request.user
    userid = user.id
    # Check if User has a watchlist entry, if not create it.
    # If the user has a watchlist entry for this listing, toggle the boolean value
    # Then return user to previous page
    try:
        query=watchlist.objects.get(listingid = listingid, userid = userid)
        if query.active == True:
            query.active= "False"
            query.save() 
        else:
            query.active= "True"
            query.save()
        print(query.active)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        entry = watchlist(listingid=listingid, userid=userid, active=True)
        entry.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def close(request):
    # Take the Listing ID that watchlist was visited from
    # https://stackoverflow.com/questions/27325505/django-getting-previous-url
    page = str(request.META.get('HTTP_REFERER'))
    # Split string to access only the ID
    # https://www.kite.com/python/answers/how-to-remove-all-non-numeric-characters-from-a-string-in-python
    listingid = page.rsplit("/", 1)[1]

    # Get current user ID 
    user = request.user
    userid = user.id

    # Query the current listing
    query = listing.objects.get(id = listingid, ownerid = userid)

    # Change the current query to closed
    query.active = "False"
    query.save()

    # Redirect to previous page 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




    

# Form classes

class listingform(forms.Form):
    listingname = forms.CharField(label='listing name', max_length='50', widget=forms.Textarea(attrs={'class':'form-control textbox', 'rows':1}))
    initialvalue = forms.DecimalField(label='initial price', decimal_places=2, max_digits=4000000, widget=forms.Textarea(attrs={'class':'form-control', 'rows':1}))
    description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'class':'form-control', 'rows':1}))
    imageurl = forms.URLField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':1}), required=False)

class bidform(forms.Form):
    bidvalue = forms.DecimalField(decimal_places=2, max_digits=9, label="Place a new bid", widget=forms.NumberInput(attrs={'class':'form-control'}))

class commentform(forms.Form):
    comment = forms.CharField(max_length=200)

