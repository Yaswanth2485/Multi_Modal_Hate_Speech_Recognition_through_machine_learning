from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from users.models import registrationmodel
from django.db.models import Q

# Create your views here.
def AdminLogin(request):
    print("Rendering AdminLogin Page")  # Debug
    return render(request, 'AdminLogin.html', {})

def adminlogout(request):
    print("Rendering base Page")
    return render(request,'base.html')      


def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print(f"AdminLoginCheck: Received login attempt with User ID = {usrid}")  # Debug

        if usrid == 'admin' and pswd == 'admin':
            request.session['user_name'] = usrid
            print(f"AdminLoginCheck: Login successful for User ID = {usrid}")  # Debug
            return redirect(AdminHome)
        else:
            print(f"AdminLoginCheck: Login failed for User ID = {usrid}")  # Debug
            messages.success(request, 'Please Check Your Login Details')

    return render(request, 'adminlogin.html', {})


def AdminHome(request):
    user_name = request.session.get('user_name', None)
    print(f"AdminHome: Logged-in User = {user_name}")  # Debug
    return render(request, 'admins/AdminHome.html', {'user_name': user_name})


def RegisterUsersView(request):
    # Retrieve the search query from the GET request
    search_query = request.GET.get('search', '').strip()  # Get the search query and strip extra spaces
    print(f"RegisterUsersView: Search Query = {search_query}")  # Debug

    # Filter the data based on the search query
    if search_query:
        data = registrationmodel.objects.filter(
            Q(name__icontains=search_query) |  # Match name
            Q(email__icontains=search_query) |  # Match email
            Q(mobile__icontains=search_query)  # Match mobile
        ).order_by('-id')  # Order results by ID in descending order
        print(f"RegisterUsersView: Filtered Data Count = {data.count()}")  # Debug
    else:
        data = registrationmodel.objects.all().order_by('-id')  # Fetch all data if no search query
        print(f"RegisterUsersView: Total Data Count = {data.count()}")  # Debug

    # Pagination: Display 5 users per page
    paginator = Paginator(data, 6)  
    page_number = request.GET.get('page')  # Get the current page number from the URL
    data_page = paginator.get_page(page_number)  # Get the paginated data for the current page
    print(f"RegisterUsersView: Current Page = {data_page.number}, Total Pages = {paginator.num_pages}")  # Debug

    # Determine the starting index for the current page
    start_index = (data_page.number - 1) * paginator.per_page

    # Retrieve 'user_name' from the session for personalized experience
    user_name = request.session.get('user_name', None)

    # Render the template with the data and pagination info
    return render(request, 'admins/viewregisterusers.html', {
        'data': data_page,  # Pass paginated data
        'user_name': user_name,  # Pass user name
        'start_index': start_index,  # Pass starting index for display
        'search_query': search_query  # Pass the search query back to the template
    })



def activate_user(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        user_name = request.session.get('user_name')

        print(f"activate_user: Received activation request for User ID = {id}")  # Debug

        if not user_name:
            print("activate_user: Session expired.")  # Debug
            messages.error(request, "Session expired. Please log in again.")
            return redirect('admin_login')

        if not id:
            print("activate_user: User ID is missing in the request.")  # Debug
            messages.error(request, "User ID is missing.")
            return redirect('admins/viewregisterusers')

        try:
            id = int(id)
        except ValueError:
            print(f"activate_user: Invalid User ID = {id}")  # Debug
            messages.error(request, "Invalid User ID.")
            return redirect('admins/viewregisterusers')

        updated = registrationmodel.objects.filter(id=id, status='waiting').update(status='activated')

        if updated:
            print(f"activate_user: User ID = {id} activated successfully.")  # Debug
            messages.success(request, f"User with ID {id} has been activated and can now log in.")
        else:
            print(f"activate_user: User ID = {id} activation failed.")  # Debug
            messages.error(request, f"User with ID {id} is either not found or already activated.")

        return redirect('RegisterUsersView')


def BlockUser(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        print(f"BlockUser: Received block request for User ID = {id}")  # Debug

        if not id:
            print("BlockUser: User ID is missing in the request.")  # Debug
            messages.error(request, "User ID is missing.")
            return redirect('admins/viewregisterusers')

        try:
            id = int(id)
        except ValueError:
            print(f"BlockUser: Invalid User ID = {id}")  # Debug
            messages.error(request, "Invalid User ID.")
            return redirect('admins/viewregisterusers')

        updated = registrationmodel.objects.filter(id=id, status='activated').update(status='blocked')

        if updated:
            print(f"BlockUser: User ID = {id} blocked successfully.")  # Debug
            messages.success(request, f"User with ID {id} has been blocked.")
        else:
            print(f"BlockUser: User ID = {id} block failed.")  # Debug
            messages.error(request, f"User with ID {id} cannot be blocked or is not activated.")

        return redirect('RegisterUsersView')


def UnblockUser(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        print(f"UnblockUser: Received unblock request for User ID = {id}")  # Debug

        if not id:
            print("UnblockUser: User ID is missing in the request.")  # Debug
            messages.error(request, "User ID is missing.")
            return redirect('admins/viewregisterusers')

        try:
            id = int(id)
        except ValueError:
            print(f"UnblockUser: Invalid User ID = {id}")  # Debug
            messages.error(request, "Invalid User ID.")
            return redirect('admins/viewregisterusers')

        updated = registrationmodel.objects.filter(id=id, status='blocked').update(status='activated')

        if updated:
            print(f"UnblockUser: User ID = {id} unblocked successfully.")  # Debug
            messages.success(request, f"User with ID {id} has been unblocked.")
        else:
            print(f"UnblockUser: User ID = {id} unblock failed.")  # Debug
            messages.error(request, f"User with ID {id} cannot be unblocked or is not blocked.")

        return redirect('RegisterUsersView')


