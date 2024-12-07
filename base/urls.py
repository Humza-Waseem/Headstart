from django.urls import path
from . import views  # we have imported views from base/views.py  that is in the same directory, so we used "." to import from the same directory
# import class based views
# from .views import homepageBeforeLogin
from django.conf import settings
from django.conf.urls.static import static
# from .views import homepageBeforeLogin



############  here we have made a list of url paterns    ###############
urlpatterns  = [
    path('login/',views.UserLogin,name = "UserLogin"),
    path('logout/'   ,views.UserLogout,name = "UserLogout"),
    path('register/' , views.registerUser,name = 'register'),
    
    # path('', views.homepageBeforeLogin, name='homepageBeforeLogin'),
    # the path() function takes 3 arguments: 1st is the url, 2nd is the view function, 3rd is the name of the url  #  the name is optional, but it is good to use it
    # path('', homepageBeforeLogin.as_view(), name='homepageBeforeLogin'),
    # path('home', views.home, name='home'),
    path('', views.homepage,name = 'home'),
    path('Update-User', views.UpdateUser, name='UpdateUser'),
    

    path('room/<str:pk>/',views.room, name ="room"),   # 'pk' stands for Primary Key  and it is set as string.......
    path('UserProfile/<str:pk>',views.UserProfile, name = "UserProfile"),  # url of the user profile page
    path('create-room/',views.CreateRoom, name = "create-room"),  # url of the create room page
    path('update-room/<str:pk>',views.UpdateRoom, name = "update-room") , # url of the update room page
    path('delete-room/<str:pk>',views.DeleteRoom, name = "delete-room"),  # url of the deleteRoom page
    path('join-room/<str:pk>',views.JoinRoom, name = "join-room"),  
    
    path('add-bookmark/<int:room_id>/', views.add_bookmark, name='add-bookmark'),
    path('remove-bookmark/<int:room_id>/', views.remove_bookmark, name='remove_bookmark'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    # path('',views.DeleteRoom, name = "delete-room"),  # url of the deleteRoom page
    path('delete-message/<str:pk>',views.DeleteMessage, name = "delete-message"),  # url of the deleteMessage
    path('topics/', views.topicsPage, name="topics"),
    # path('topics/load_more/', views.load_more_topics, name='load_more_topics'),

    ]
