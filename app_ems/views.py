from django.shortcuts import render,redirect
from app_ems.models import EventInfo
from django.utils import timezone
from datetime import date,timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def frontpage(request):
    return render(request,'emsapp/ems_frontpage.html')

def home(request):
    if request.method =="POST":
         # Extract event data from the POST request
        if 'eventname' in request.POST:
            event_name= request.POST.get('eventname')
            event_type= request.POST.get('eventtype')
            event_date= request.POST.get('eventdate')
            event_location= request.POST.get('eventlocation')
            event_description= request.POST.get('eventdescription')
            event_reg_deadline= request.POST.get('eventregdeadline')
            event_max_capacity= request.POST.get('eventmaxcapacity')
            event_image= request.FILES.get('eventimage')
            print(f"events info --{event_name} - {event_type} - {event_location} - {event_date} - {event_max_capacity} ")
            # Create a new event instance
            event_instance = EventInfo(user_id=request.user.id,event_name = event_name,event_type=event_type,event_date=event_date,
                                    event_location=event_location,event_description=event_description,
                                    event_reg_deadline=event_reg_deadline,event_max_capacity=event_max_capacity)
            # Assign the event image if provided
            if event_image: 
                event_instance.event_image = event_image
            # Save the event instance
            event_instance.save()
            # Redirect to the event home page after saving
            return redirect('event_home')
        # Implement search functionality if needed
        elif 'search' in request.POST:
            pass
        # Implement filtering by event type if needed
        


    # Fetch all event data for GET request or if no specific POST request is handled
    event_data = EventInfo.objects.all().order_by('-event_date')
            
    # Implement pagination for event data
    paginator = Paginator(event_data,2)  # Show No.of events per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)

    # Render the home page with paginated event data
    return render(request,'emsapp/ems_home.html',{'page_obj':page_obj})



def eventype(request,event_type):
    if event_type == 'latest':
        event_data = EventInfo.objects.all().order_by('-created_at')
    elif event_type == "tomorrow":
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        event_data = EventInfo.objects.filter(event_date=tomorrow).order_by('event_date')
    else:
        event_data = EventInfo.objects.filter(event_type=event_type).order_by('-event_date')
    
            # Implement pagination for event data
    paginator = Paginator(event_data,2)  # Show No.of events per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
                # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
                # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)

            # Render the home page with paginated event data
    return render(request,'emsapp/ems_home.html',{'page_obj':page_obj})

def About(request):
    return render(request,'emsapp/ems_about.html')