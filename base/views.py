
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room, Topic, Message, Event
from .forms import RoomForm, UserForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# -------------------------------------
# Tomendegi commentde kerek narse kishkene logic


# rooms = [
#     {'id': 1, 'name': 'lets learn Python'},
#     {'id': 2, 'name': 'lets learn Django'},
#     {'id': 3, 'name': 'lets learn Database'},
# ]

# def room(request, pk):
#     room = None
#     for i in rooms:
#         if i['id'] == pk:
#             room = i

#     context = {'room': room}
    
#     return render(request, 'room.html', context)


# end end end end 






def loginPage(request):

    page = 'login'

    # tomendegi user login qilgan bolsa jane urlde login jazsa tuwridan
    #home ge baradi sebebi login qilip qaytadan login ge barsa qiziq boladi eken
    
    if request.user.is_authenticated:
        return redirect('/')

    #/////////////////////////////////////

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username = username)

        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome to our site { request.user.username.title() }')
            return redirect('/')

        else:
            messages.error(request, 'Username or Password does not exist')




    context = {'page': page}
    return render(request, 'registration/login-register.html', context)






def registerPage(request):
    page = "register"
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "Register successfully created")
            return redirect('login')
        else:
            messages.error(request, "An error accurred during registration")
            
            


    context = {'page': page, 'form': form}

    return render(request, 'registration/login-register.html', context)








def logout_user(request):
    logout(request)
    return redirect('/')
    



def profile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, "room_message": room_message, "topics": topics}

    return render(request, "profile.html", context)




def home(request):
    

    q = request.GET.get("q") if request.GET.get("q") != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) | # | means or & means and
        Q(description__icontains = q)
    )

    room_count = rooms.count()

    topic = Topic.objects.all()[:5]
    event = Event.objects.get(id = 1)
    

    room_message = Message.objects.filter(Q(room__topic__name__icontains = q))[:5]

    context = {
        'rooms': rooms, 
        'topics': topic, 
        'room_count': room_count, 
        "room_message": room_message,
        'event': event
        }
    return render(request, 'home.html', context)






def moreTopics(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains = q)

    context = {
        "topics": topics
    }

    return render(request, "more_topics.html", context)









def room(request, pk):
    room = Room.objects.get(pk = pk)
    room_message = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    # comment
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body")
        )
        # //
        room.participants.add(request.user)
        # add bul kimdir comment jazsa participants avtomat turde qosiladi
        return redirect('room', pk = room.pk)
    # // comment


    context = {'room': room, 'messagess': room_message, "participants": participants}
    
    return render(request, 'room.html', context)





@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name = topic_name)


        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get("name"),
            description = request.POST.get("description")

        )
        messages.success(request, f"Room succesfully created by {request.user}")
        return redirect('home')

        # if form.is_valid():
        #     # form.save()

        #     # bul jerde user and participant forms 
        #     # korinbeytugin qildiq ozi avtomat save etedi
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()

            

    context = {'form': form, "topics": topics}

    return render(request, 'room_form.html', context)







@login_required(login_url = 'login')
def updateRoom(request, pk):
    room = Room.objects.get(pk = pk)
    form = RoomForm(instance = room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("/")



        # form = RoomForm(request.POST, instance= room)
        # if form.is_valid():
        #     form.save()
            # return redirect("/")


    context = {'form': form, 'room': room}

    return render(request, 'room_form.html', context)





@login_required(login_url = 'login')
def deleteRoom(request, pk):
    room = Room.objects.get(pk = pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!!")

    if request.method == "POST":
        room.delete()
        return redirect('/')

    context = {'obj': room}
    return render(request, 'delete.html', context)









def deleteMessage(request, pk):
    message = Message.objects.get(id = pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here")

    
    if request.method == "POST":
        message.delete()

        return redirect('home')
    
    return render(request, 'delete.html', {'obj': message})









def updateUser(request, pk):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
           form.save()
           messages.success(request, "Your Profile succesfully updated")
           return redirect('update-user', pk = user.id) 

    context = {
        "form": form
    }

    return render(request, 'update_user.html', context)