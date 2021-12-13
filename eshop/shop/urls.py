from django.urls import path
from shop import views


urlpatterns = [
    path("", views.index, name="ShopHme"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="checkout"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),





]
