from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Room,Topic,Message,User,Bookmark   # importing the Room and Topic and Message models from models which is in the same directory
from django.contrib import messages  # importing the flash messages 

from .forms import RoomForm , UserForm, MyUserCreationForm  # importing the RoomForm  and UserFOrm from the Forms.py file which is in the same directory
# from .Forms import RoomForm , UserForm, MyUserCreationForm  # importing the RoomForm  and UserFOrm from the Forms.py file which is in the same directory
from django.contrib.auth import authenticate,login,logout  
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # here we get Q because it will help us to insert query operations AND,OR,NOT




def UserLogout(request):  # creating this view to so that 
      
    try:
        logout(request)
        messages.success(request,"Successfully Logged Out")
    
    except Exception as e:
        messages.error(request,"An error occured during logging out")
    return redirect('home')


def registerUser(request):  
    # page = 'register' 
    # form = UserCreationForm()
    form = MyUserCreationForm()
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = MyUserCreationForm(request.POST)   # using MyUserCreationForm because it has our custom user model form
        if form.is_valid():
            user = form.save(commit=False)#commit = False means that we are not saving the form yet
            user.username = user.username
            user.save()
            login(request,user)
            messages.success(request,'Successfully registered')
            
            return redirect('UserLogin')
        else:
            messages.error(request,'An error occured during registration')

    return render(request,'base/UserLogin.html',{'form':form})


def UserLogin(request):
    page  = 'login'
    if request.user.is_authenticated: # if a authenticated user try to manually enter "/login" in the browser then we will restrict the Login page
        return redirect('home') # and rediredct the user to the home page because uer is already logged in
    
    if request.method == "POST":  
        email = request.POST.get('email') # getting the email from the login form in lowercase
        password = request.POST.get('password')  # getting the password from the login form
        
        try:
            user = User.objects.get(email=email) # getting the user with the specific username
        except:
            messages.error(request,"email does not exist")
        
        user = authenticate(request,email =email,password= password )
        if user is not None:
            login(request,user)
            messages.success(request,f"Successfully Logged In as {request.user.username}")
            return redirect('home')
        else:
            messages.error(request,"email or Password is incorrect")

    context={'page':page}
    return render(request,'base/UserLogin.html',context)

# rooms = [
#     {'id': 1, 'name': 'Lets learn Python'},
#     {'id': 2, 'name': 'Designing a Django App'},
#     {'id': 3, 'name': 'Frontend Development'},
# ]


from django.views.generic import TemplateView

from django.shortcuts import render
from django.db.models import Q

def homepage(request):
        participants = User.objects.filter(id__in=Room.objects.values_list('participants', flat=True).distinct())

    # if request.user.is_authenticated:
        # Logged-in user logic
        q = request.GET.get('q') if request.GET.get('q') else ''
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) | 
            Q(name__icontains=q) | 
            Q(description__icontains=q)
        )
        topics = Topic.objects.all()
        UserMessages = Message.objects.filter(Q(room__topic__name__icontains=q))
        room_count = rooms.count()
        context = {
            'rooms': rooms,
            'topics': topics,
            'UserMessages': UserMessages,
            'room_count': room_count,
            'participants': participants,
        }
        return render(request, 'base/home.html', context)
    # else:
    #     # Guest user logic
    #     context = {
    #         "participants": participants,
    #         "rooms": Room.objects.all(),
    #         "topics": Topic.objects.all(),
    #         "UserMessages": Message.objects.all(),
    #         "room_count": Room.objects.count(),
    #     }
    #     return render(request, 'base/homepageBeforeLogin.html', context)




@login_required(login_url="UserLogin") 
def UserProfile(request,pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()  # getting all the rooms of the user
    topics = Topic.objects.all()
    UserMessages = user.message_set.all()

    context = {"user": user,"rooms":rooms , "topics":topics , "UserMessages":UserMessages}
    return render(request,'base/userProfile.html',context)


@login_required(login_url="UserLogin") 
def UpdateUser(request):
    form = UserForm(instance = request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance= request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile was Updated ')
            return redirect('UserProfile',pk = request.user.id)
        else:
            messages.error(request, 'An error occured during updating your profile')
        

    context= {"form":form}
    return render(request,'base/UpdateUser.html',context)


# @login_required(login_url="UserLogin") 
def room(request, pk):     
    room = Room.objects.get(id=pk) 
    UserMessages = room.message_set.all()  # Getting all the messages of the room we write set because we are getting all the messages of the room for relation ( one to many)  one room can have many messages
    UserMessagesCount = UserMessages.count()  # getting the count of the messages
    participants = room.participants.all()  # Getting all the participants of the room

    # Form for sending the message in the room.html page
    if request.method == 'POST':  # If the method in the form is POST
        body = request.POST.get('body')  # Get the message body from the form
        
        # Check if the message body is empty or contains only whitespace
        if body and body.strip():
            message = Message.objects.create(  # Create the message object only if valid
                user=request.user,            # The user who is logged in
                room=room,                    # The room in which the message is sent
                body=body.strip()             # Use the stripped message body
            )
            room.participants.add(request.user)  # Add the user to the room participants

        return redirect('room', pk=room.id)  # Redirect to the same room after handling the form submission
       
    context = { 
        'room': room,
        'UserMessages': UserMessages,
        'participants': participants,
        'UserMessagesCount': UserMessagesCount,
    }

    return render(request, 'base/room.html', context)  # Render the room.html page

  

@login_required(login_url="UserLogin")     # login will be required to access this page
# def CreateRoom(request):
#     form = RoomForm()   # This line creates an instance of the RoomForm class.
#     topics = Topic.objects.all( )          # Getting all the topics from the database

#     if request.method =='POST':   # This line checks if the HTTP request method is 'POST'
#         topic_name = request.POST.get('topic')  # getting the topic name from the form
#         topic, created = Topic.objects.get_or_create(name=topic_name)  # getting the topic from the database if it is already there otherwise create the topic
#         Room.objects.create(  # creating the room object
#             host = request.user,  # the host will be the user who is logged in
#             topic = topic,     
#             name = request.POST.get('name'),  # getting the name of the room from the form
#             description = request.POST.get('description'),  # getting the description of the room from the form
#         )
#         room.participants.add(request.user)

#         # form = RoomForm(request.POST)  #  passing all the values into the form ,, adding the date to form
#         # if form.is_valid():   # this check if all the form submitted values are valid

#         #     room = form.save(commit= False)  # here we save the form, getting the instance of the form 
#         #     room.host = request.user
            
#             # room.save()
#         messages.success(request, f'Room created for {request.user.username}')  # showing the success message after creating the room
        
#         return redirect('home')    # here we redirect the user (who submit the form) to the listed Page(home) note that we are using the Name of the 'HOME' html file which we declared in the urls. 

#     context = {'form':form,'topics':topics}
#     return render(request,'base/room_form.html',context)
@login_required(login_url="UserLogin") 
def CreateRoom(request):
    form = RoomForm() # This line creates an instance of the RoomForm class.
    topics = Topic.objects.all() # Getting all the topics from the database

    if request.method == 'POST': # This line checks if the HTTP request method is 'POST'
        topic_name = request.POST.get('topic') # getting the topic name from the form
        topic, created = Topic.objects.get_or_create(name=topic_name) # getting the topic from the database if it is already there otherwise create the topic

        room = Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )

        # Add the user to the participants set
        room.participants.add(request.user)#  passing all the values into the form ,, adding the date to form

        messages.success(request, f'Room created for {request.user.username}')
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url="UserLogin")
def UpdateRoom(request,pk):  # here we get the pk also to update the specific room
    room = Room.objects.get(id = pk)  # getting the room with the specific id
    form = RoomForm(instance= room)  # here we get the instance of the room that we want to update. THis will also show  the data of the room that we want to update in the form fields... so it would be easy for update keeping in view the previous data
    topics = Topic.objects.all()  # getting all the topics from the database
    if request.user != room.host:
        return HttpResponse("You are not allowed to Edit this page")
    
    # if request.method == 'POST':
    #     form = RoomForm(request.POST, instance= room)  # Updating the form according to the the room.  The instance=room tells the request to update the attributes.. if we do not do this then django will simply make another room with our updated values

    if request.method == 'POST':
        topic__name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic__name)
        room.name= request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        # if form.is_valid():
        #     form.save()
        messages.success(request, f'"{room.name}" Updated')
        return redirect('home')  # going back to the home page 
    context = {'form':form,'topics': topics,'room':room}

    return render(request,'base/room_form.html',context)


@login_required(login_url="UserLogin")
def DeleteRoom(request,pk):
    room = Room.objects.get(id = pk)   # getting the specific room 
    if request.method == 'POST': # if the method is to POST (form is filled)then
        room.delete() 
        messages.success(request, f'Room {room.name} Deleted ')
        return redirect('home')   # redirect the user to home. after deleting the room 
    context = {'obj':room}  # using obj instead of "room" because we will use obj in our template to show a delete message also if the message isn't about the room 
    
    return render(request,'base/delete.html',context)

@login_required(login_url="UserLogin")
def JoinRoom(request,pk):
    room = Room.objects.get(id = pk)
    if request.user in room.participants.all():
        messages.info(request,'You are already in this room')
        return redirect('room',pk=pk)
    room.participants.add(request.user)
    messages.success(request,f'Welcome to the room \"{room.name}\"')
    return redirect('room',pk=pk)



@login_required
def bookmarks(request):
    user = request.user
    bookmarks = Bookmark.objects.filter(user=user).select_related('room')
    return render(request, 'base/bookmarks.html', {'bookmarks': bookmarks})
    
# @login_required
# def add_bookmark(request, room_id):
#     room = get_object_or_404(Room, id=room_id)
#     user = request.user
    
#     # Check if the user has already bookmarked the room
#     if not Bookmark.objects.filter(user=request.user, room=room).exists():
#         Bookmark.objects.create(user=request.user, room=room)
    
#     return redirect('home')  # Redirect to the bookmarks page or room detail page



@login_required
def add_bookmark(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    user = request.user
    
    # Check if the user has already bookmarked the room
    if not Bookmark.objects.filter(user=user, room=room).exists():
        Bookmark.objects.create(user=user, room=room)
        message = 'Room bookmarked successfully!'
        bookmarked = True
    else:
        # Optional: If you want to allow unbookmarking
        Bookmark.objects.filter(user=user, room=room).delete()
        message = 'Room removed from bookmarks.'
        bookmarked = False
    
    # Check if the request is AJAX
    if request.is_ajax():
        return JsonResponse({
            'message': message,
            'bookmarked': bookmarked
        })
    
    # If it's not an AJAX request, we can still redirect to the home page (or any other page)
    return redirect('home')




@login_required
def remove_bookmark(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    # Delete the bookmark if it exists
    Bookmark.objects.filter(user=request.user, room=room).delete()

    return redirect('bookmarks_page')  # Redirect to the bookmarks page or room detail page
    
@login_required
def bookmarked_rooms(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('room')
    return render(request, 'bookmarks.html', {'bookmarks': bookmarks})

    
    
    
    
    
@login_required(login_url="UserLogin")
def DeleteMessage(request,pk):
    messages = Message.objects.get(id = pk)   

    if( request.user != messages.user ): 
        return HttpResponse("You are not allowed to delete this message")

    if request.method == 'POST': 
        messages.delete()
        # messages.success(request, f'Room {room.name} Deleted ')
        return redirect('room',pk=messages.room.id)   # redirecting the user to the same room after deleting the message
    
    context = {'obj':messages} 
    
    return render(request,'base/delete.html',context)


# def topicsPage(request):
#     q = request.GET.get('q') if request.GET.get('q') != None else ''
#     topics = Topic.objects.filter(name__icontains=q)
#     return render(request, 'base/topics.html', {'topics': topics})






from django.core.paginator import Paginator
from django.http import JsonResponse
from base.models import Topic

def topicsPage(request):
    q = request.GET.get('q', '')  # Filter by search query
    topics_list = Topic.objects.filter(name__icontains=q)  # Filter topics by search query
   

    # Pagination setup (10 topics per page)
    paginator = Paginator(topics_list, 10)
    page_number = request.GET.get('page')  # Get the page number from the query string
    page_obj = paginator.get_page(page_number)

    # Check if the request is AJAX by inspecting the request header
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # If this is an AJAX request, return only the list of topics
        topics_data = [{'name': topic.name, 'count': topic.room_set.all().count()} for topic in page_obj]
        
        return JsonResponse({'topics': topics_data, 'has_next': page_obj.has_next()})

    return render(request, 'base/topics.html', {'topics': page_obj})




# def load_more_topics(request):
#     # Get the last topic name passed from the frontend
#     last_topic_name = request.GET.get('last_topic', '')
    
#     # Fetch the next set of topics after the last one shown
#     topics = Topic.objects.filter(name__gt=last_topic_name).order_by('name')[:10]

#     # Prepare data for response
#     topics_data = [
#         {
#             'name': topic.name,
#             'room_count': topic.room_set.count(),
#         }
#         for topic in topics
#     ]
    
#     # Return JSON response with new topics
#     return JsonResponse({'topics': topics_data})






def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})