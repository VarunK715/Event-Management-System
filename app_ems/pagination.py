from urllib import request
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger



def Pagination(inpt,no_per_page):
    # Implement pagination for event data
    paginator = Paginator(inpt,no_per_page)  # Show No.of events per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)
    
    return page_obj
