
from django.urls import path

from .views import (
    home,
    room,
    createRoom,
    updateRoom,
    deleteRoom,
    loginPage,
    logout_user,
    registerPage,
    deleteMessage,
    profile,
    updateUser,
    moreTopics,

)


urlpatterns = [
    path('login/', loginPage, name = 'login'),
    path('logout/', logout_user, name = 'logout'),
    path('register/', registerPage, name = 'register'),
    path('profile/<int:pk>/', profile, name = 'profile'),
    
    path('', home, name="home"),
    path('room/<int:pk>/', room, name = 'room'),
    path('create-room/', createRoom, name = 'create-room'),
    path('update-room/<int:pk>/', updateRoom, name = 'update-room'),
    path('delete-room/<int:pk>/', deleteRoom, name = 'delete-room'),
    path('delete-message/<int:pk>/', deleteMessage, name = 'delete-message'),
    path('updateUser/<int:pk>/', updateUser, name = 'update-user'),
    path('more-topics/', moreTopics, name = 'more-topics'),

]