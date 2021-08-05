from django.urls import path
from .views import index, Dashboard, NewLaundry, PastBasket, LaundryRequest, LaundryOffice,\
    accept_request, reject_request, RequestView, completed, NewIronBoard, ProfileView, new_laundry,\
    LaundryProfileView, map_request, choose_laundry_man, random_select

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/<slug>', Dashboard.as_view(), name='dashboard'),
    path('profile/<slug>', ProfileView.as_view(), name='profile'),
    path('laundry', NewLaundry.as_view(), name='laundry'),
    path('new_laundry/', new_laundry, name='new_laundry'),
    path('basket/<slug>', PastBasket.as_view(), name='basket'),
    path('request', LaundryRequest.as_view(), name='request'),
    path('laundry_office/<slug>', LaundryOffice.as_view(), name='office'),
    path('laundry_profile/<slug>', LaundryProfileView.as_view(), name='laundry_profile'),
    path('accept_request/<slug>', accept_request, name='accept_request'),
    path('reject_request/<slug>', reject_request, name='reject_request'),
    path('request/<slug>', RequestView.as_view(), name='request_view'),
    path('completed/<slug>', completed, name='completed'),
    path('Ironing_Board', NewIronBoard.as_view(), name='ironing_board'),
    path('map/select', map_request, name='map_select'),
    path('random/', random_select, name='random_select'),
    path('request/<slug>', choose_laundry_man, name='request_laundry'),
]