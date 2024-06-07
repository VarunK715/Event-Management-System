from django.shortcuts import render,redirect,get_object_or_404
from app_ems.models import EventInfo,Booking
from django.utils import timezone
from datetime import date,timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from . pagination import Pagination

def frontpage(request):
    return render(request,'emsapp/ems_frontpage.html')


@login_required(login_url='users_login')
def home(request):
    # Fetch all event data for GET request or if no specific POST request is handled
    event_data = EventInfo.objects.all().order_by('-event_date')

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
            event_entry_fee= request.POST.get('evententryfee')
            event_image= request.FILES.get('eventimage')
            print(f"events info --{event_name} - {event_type} - {event_location} - {event_date} - {event_max_capacity} ")
            # Create a new event instance
            event_instance = EventInfo(user_id=request.user.id,event_name = event_name,event_type=event_type,event_date=event_date,
                                    event_location=event_location,event_description=event_description,
                                    event_reg_deadline=event_reg_deadline,event_max_capacity=event_max_capacity,event_entry_fee=event_entry_fee)
            # Assign the event image if provided
            if event_image: 
                event_instance.event_image = event_image
            # Save the event instance
            event_instance.save()
            # Redirect to the event home page after saving
            return redirect('event_home')
        # Implement search functionality if needed
        elif 'search' in request.POST:
            keyword_search = request.POST.get('search')
            event_data = EventInfo.objects.filter(event_name__icontains=keyword_search).order_by('-event_date')
    
            
    # Implement pagination for event data
    paginator = Paginator(event_data,5)  # Show No.of events per page
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

@login_required(login_url='users_login')
def About(request):
    return render(request,'emsapp/ems_about.html')

@login_required(login_url='users_login')
def organizer_dashboard(request):
    event_data = EventInfo.objects.filter(user=request.user).order_by('-event_date')
            # Implement pagination for event data
    paginator = Paginator(event_data,5)  # Show No.of events per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
                # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
                # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)
    return render(request,'users/organizer_dashboard.html',{'page_obj':page_obj})


@login_required(login_url='users_login')
def participant_dashboard(request,):
    # Get all bookings for the current user
    user_bookings = Booking.objects.filter(user=request.user)
    # Get all event info for the bookings in a single query
    booked_event_ids = user_bookings.values_list('event_id', flat=True)
    booked_events = EventInfo.objects.filter(id__in=booked_event_ids)
    return render(request,'users/participant_dashboard.html',{'booked_event_info':booked_events})

@login_required(login_url='users_login')
def update_event(request,id):
    update_data = get_object_or_404(EventInfo,id=id)
    formatted_datetime = update_data.event_reg_deadline.strftime('%Y-%m-%dT%H:%M:%S')
    if 'update_eventname' in request.POST:
            update_event_name= request.POST.get('update_eventname')
            update_event_type= request.POST.get('update_eventtype')
            update_event_date= request.POST.get('update_eventdate')
            update_event_location= request.POST.get('update_eventlocation')
            update_event_description= request.POST.get('update_eventdescription')
            update_event_reg_deadline= request.POST.get('update_eventregdeadline')
            update_event_max_capacity= request.POST.get('update_eventmaxcapacity')
            update_event_entry_fee= request.POST.get('update_evententryfee')
            update_event_image= request.FILES.get('update_eventimage')

            update_event_instance = update_data
            update_event_instance.event_name = update_event_name
            update_event_instance.event_type = update_event_type
            update_event_instance.event_date = update_event_date
            update_event_instance.event_location = update_event_location
            update_event_instance.event_description = update_event_description
            update_event_instance.event_reg_deadline = update_event_reg_deadline
            update_event_instance.event_max_capacity = update_event_max_capacity
            update_event_instance.event_entry_fee=update_event_entry_fee

            if update_event_image:
                update_event_instance.event_image = update_event_image
            
            update_event_instance.save()
            messages.success(request,f"Event information updated successfully")
            return redirect('organizer_dashboard')


    print(f"update data -- {update_data}")
    return render(request,'emsapp/update_event.html',{'update_data':update_data,'formatted_datetime':formatted_datetime})

@login_required(login_url='users_login')
def book_event(request,id):
    book_event_data = EventInfo.objects.get(id=id)    
    return render(request,'emsapp/book_event.html',{'book_event_data':book_event_data})

@login_required(login_url='users_login')
def delete_event(request,id):
    EventInfo.objects.filter(id=id).delete()
    return redirect('organizer_dashboard')

@login_required(login_url='users_login')
def cancel_event(request,id):
    Booking.objects.filter(event_id=id).delete()
    return redirect('organizer_dashboard')

@login_required(login_url='users_login')
def payment_page(request,id):
    payment_data = get_object_or_404(EventInfo, id=id)
    if request.method=="POST":
        print(f"erros == {request.POST}")
        booking_instance = Booking(user_id=request.user.id,event_id=payment_data.id)
        booking_instance.save()
        messages.success(request,f"Event is booked successfully.")
        return redirect('participant_dashboard') 

    return render(request,'emsapp/payment_page.html',{'payment_data':payment_data})