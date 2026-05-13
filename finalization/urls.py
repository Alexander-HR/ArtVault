from django.urls import path
from . import views

app_name = "finalization"

urlpatterns = [
    path("<int:bid_id>/contact/", views.contact_step,name="contact_step"),
    path("<int:bid_id>/review/", views.review_step, name="review_step"),
    path("<int:bid_id>/payment/", views.payment_step, name="payment_step"),
    path("<int:bid_id>/confirm/", views.confirmation_step, name="confirmation_step"),

]