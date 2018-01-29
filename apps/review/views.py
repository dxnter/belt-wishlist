from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from models import User, Item

# Display the registration and login 
def index(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    return render(request, 'review/index.html')

# Register a new validated user and store their ID in session
def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    hashed_password = bcrypt.hashpw(request.POST['registration_password'].encode(), bcrypt.gensalt())
    user = User.objects.create(name=request.POST['registration_name'], username=request.POST['registration_username'], date_hired=request.POST['date_hired'], password=hashed_password)
    user.save()
    request.session['id'] = user.id
    return redirect('/dashboard')

# Login a validated user and store their ID in session
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    if (User.objects.filter(username=request.POST['login_username']).exists()):
        user = User.objects.filter(username=request.POST['login_username'])[0]
        if (bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode())):
            request.session['id'] = user.id
            return redirect('/dashboard')
    return redirect('/')

# Successfully registered or logged in users will be sent to a list of their trips and other plans
def dashboard(request):
    if not 'id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    items = Item.objects.filter(id=user.id)
    other = Item.objects.all().exclude(user__id=user.id)
    context = {
        "user": user,
        "items": items,
        "other": other
    }
    return render(request, 'review/dashboard.html', context)

# Add other user's created trips to their own schedules
def wish(request):
    item = Item.objects.filter(id=request.POST['item_id']).first()
    user = User.objects.get(id=request.session['id'])
    user.items.add(item)
    user.save()
    return redirect('/dashboard')

# Detailed information about a specific destination
def item(request, id):
    if not 'id' in request.session:
        return redirect('/')
    item = Item.objects.get(id=id)
    context = {
        "item": item
    }
    return render(request, 'review/item.html', context)
    
# Render the app a trip page
def add(request):
    if not 'id' in request.session:
        return redirect('/')
    return render(request, 'review/add.html')

# Post a new trip into the database and return to the travels page
def create(request):
    if request.method == "GET":
        return redirect('/add')
    errors = User.objects.item_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/add')
    user = User.objects.get(id=request.session['id'])
    item = Item.objects.create(
        item=request.POST.get('item'),
        added_by=user
    )
    user.items.add(item)
    user.save()
    return redirect('/dashboard')

# Remove an item from a wishlist that wasn't created by the logged in user
def remove(request, id):
    item = Item.objects.get(id=id)
    user = User.objects.get(id=request.session['id'])
    user.items.remove(item)
    return redirect('/dashboard')


# Deletes items added to a wishlist created by the logged in user
def delete(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('/dashboard')

# Remove a logged in user from session and redirects to /
def logout(request):
    request.session.clear()
    return redirect('/')