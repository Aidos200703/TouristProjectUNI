from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('destinations/', views.destinations, name='destinations'),
    path('tours/', views.tours, name='tours'),
    path('guides/', views.guides, name='guides'),
    path('booking/', views.booking, name='booking'),
    path('weather/', views.weather_view, name='weather'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    re_path(r'^destinations/(?P<pk>[0-9]+)/$', views.destination_detail, name='destination_detail'),
    re_path(r'^tours/(?P<pk>[0-9]+)/$', views.tour_detail, name='tour_detail'),
    re_path(r'^guides/(?P<pk>[0-9ы]+)/$', views.guide_detail, name='guide_detail'),
    re_path(r'^search/(?P<query>[a-zA-Z0-9\-]+)/$', views.search_view, name='search'),

    path('manage/destinations/', views.destination_list, name='destination_list'),
    path('manage/destinations/add/', views.destination_create, name='destination_create'),
    path('manage/destinations/<int:pk>/edit/', views.destination_update, name='destination_update'),
    path('manage/destinations/<int:pk>/delete/', views.destination_delete, name='destination_delete'),

    path('manage/tours/', views.tour_list, name='tour_list'),
    path('manage/tours/add/', views.tour_create, name='tour_create'),
    path('manage/tours/<int:pk>/edit/', views.tour_update, name='tour_update'),
    path('manage/tours/<int:pk>/delete/', views.tour_delete, name='tour_delete'),

    path('manage/guides/', views.guide_list, name='guide_list'),
    path('manage/guides/add/', views.guide_create, name='guide_create'),
    path('manage/guides/<int:pk>/edit/', views.guide_update, name='guide_update'),
    path('manage/guides/<int:pk>/delete/', views.guide_delete, name='guide_delete'),

    path('manage/bookings/', views.booking_list, name='booking_list'),
    path('manage/bookings/add/', views.booking_create, name='booking_create'),
    path('manage/bookings/<int:pk>/edit/', views.booking_update, name='booking_update'),
    path('manage/bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'),

    path('manage/reviews/', views.review_list, name='review_list'),
    path('manage/reviews/add/', views.review_create, name='review_create'),
    path('manage/reviews/<int:pk>/edit/', views.review_update, name='review_update'),
    path('manage/reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),

    path('manage/customers/', views.customer_list, name='customer_list'),
    path('manage/customers/add/', views.customer_create, name='customer_create'),
    path('manage/customers/<int:pk>/edit/', views.customer_update, name='customer_update'),
    path('manage/customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
]