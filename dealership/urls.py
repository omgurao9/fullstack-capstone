from django.contrib import admin
from django.urls import path
from cars import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("login/submit/", views.form_login, name="form_login"),
    path("logout/", views.logout_page, name="logout"),
    path("dealer/<int:dealer_id>/", views.dealer_detail, name="dealer_detail"),
    path("review/<int:dealer_id>/", views.review_page, name="review_page"),
    path("api/login/", views.api_login, name="api_login"),
    path("api/logout/", views.api_logout, name="api_logout"),
    path("api/register/", views.api_register, name="api_register"),
    path("api/dealers/", views.api_dealers, name="api_dealers"),
    path("api/dealers/state/<str:state>/", views.api_dealers_by_state, name="api_dealers_by_state"),
    path("api/dealers/<int:dealer_id>/", views.api_dealer_detail, name="api_dealer_detail"),
    path("api/dealers/<int:dealer_id>/reviews/", views.api_dealer_reviews, name="api_dealer_reviews"),
    path("api/carmakes/", views.api_carmakes, name="api_carmakes"),
    path("api/analyze-review/", views.api_analyze_review, name="api_analyze_review"),
]
