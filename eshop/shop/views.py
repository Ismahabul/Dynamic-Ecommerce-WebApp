from django.shortcuts import render,redirect
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'Your-Merchant-Key-Here'

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)
def searchMatch(query, item):
    '''return true onlyif query matches the item'''
    if query in item.desc.lower() or query in item.Product_name.lower() or query in item.category.lower():
        return True
    else:    
        return False    

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds':allProds, "msg":""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg':"Please make sure  to enter relevant query"}
    return render(request, 'shop/search.html', params)
    


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')





def productView(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')


def register(request):
    thank = False
    if request.method=='POST':
       fname = request.POST['fname']
       lname = request.POST['lname']
       username = request.POST['username']
       email = request.POST['email']
       pass1 = request.POST['pass1']
       pass2 = request.POST['pass2']
      #check Error
       if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters')
            return redirect('index')
       if pass1 != pass2:
            messages.error(request, 'Password not match')
            return redirect('index')
       if User.objects.filter(username = username).first():
        messages.error(request, "This username is already taken")
        return redirect('home')
     #create a user
       myuser = User.objects.create_user(username, email, pass1)
       myuser.first_name = fname
       myuser.last_name = lname
       myuser.save()
       messages.success(request, 'Your Account has been Successfully Created')
       return redirect('index')
    else:
         return render(request, 'shop/register.html')

def login(request):
    if request.method=='POST':
       loginusername = request.POST['loginusername']
       loginpassword = request.POST['loginpassword']
       user = authenticate(username=loginusername, password=loginpassword)
       if user is not None:
           login(request, user)
           messages.success(request, 'Successfully Logged In')
           return redirect('index')
       else:
           messages.error(request, 'Invalid Credentials, Please Try Again')
           return redirect('index')

    return render(request, 'shop/login.html')

def Logout(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out')
    return redirect('index')