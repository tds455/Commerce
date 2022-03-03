from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # Path for creating a new listing
    path("create", views.create, name="create"),
    # Path for viewing individual listings
    path("<int:id>", views.display, name="display"),
    # Path for adding / removing to watchlist
    path("watch", views.watch, name="watch")
]
