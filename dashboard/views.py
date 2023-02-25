from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import os
import datetime
import csv
import mimetypes
from rest_framework import generics
from .serializers import *

# Create your views here.
class LoginView(generic.FormView):
    template_name = 'login.html'
    def get(self, request):
        return render(request, self.template_name, {'form': LoginForm, 'message': ''})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            return render(request, template_name=self.template_name, context={'form': LoginForm, 'message': 'Invalid credentials! Try again'})
        return render(request, template_name=self.template_name, context={'form': LoginForm, 'message': 'Fill all fields!'})

class SignupView(generic.FormView):
    template_name = 'signup.html'
    def get(self, request):
        return render(request, self.template_name, {'form': SignupForm, 'message': ''})
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            if (password == confirm_password):
                if User.objects.filter(username=username).exists():
                    return render(request, template_name=self.template_name, context={'form': SignupForm, 'message': 'Username Exists. Try another username'})
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                return redirect('login')
            return render(request, template_name=self.template_name, context={'form': SignupForm, 'message': 'Password Mismatch! Try again'})
        return render(request, template_name=self.template_name, context={'form': SignupForm, 'message': 'Please fill all Fields!'})

class HomeView(LoginRequiredMixin, generic.DetailView):
    login_url = 'login'
    template_name = 'home.html'
    def get(self, request):
        shop_list = Shops.objects.all()
        return render(request, self.template_name, {'shops': shop_list})

class DashboardView(LoginRequiredMixin, generic.FormView):
    login_url = 'login'
    template_name = 'dashboard.html'
    def get(self, request):
        dashboard = Shops.objects.filter(owner=request.user)
        if dashboard.exists():
            dashboard = dashboard.first()
            order_list = Orders.objects.filter(shop=dashboard).order_by('-id')
            if dashboard.order_count == 0:
                delivery_percent = 0
            else:
                delivery_percent = (dashboard.delivered_count / dashboard.order_count) * 100
            return render(request, self.template_name, {'dashboard': dashboard, 'delivery_percent': round(delivery_percent, 2), 'order_list': order_list})
        else:
            return HttpResponse('<br><br><center><h1>No shops registered under logged in user</h1></center>')
    def post(self, request):
        Orders.objects.create(shop= Shops.objects.get(owner=request.user), customer_name= request.POST.get('customer'))
        shop = Shops.objects.filter(owner=request.user)
        shop.update(order_count=shop.first().order_count+1)
        shop.update(pending_count=shop.first().pending_count+1)
        return redirect('dashboard')

class OrderlistView(LoginRequiredMixin, generic.ListView):
    login_url = 'login'
    template_name = 'orderlist.html'
    def get(self, request):
        orderlist = Orders.objects.filter(customer= request.user)
        return render(request, self.template_name, {'orders': orderlist})

class DownloadView(generic.FormView):
    template_name = 'download.html'
    def get(self, request):
        orders = Orders.objects.all()
        users = User.objects.exclude(username = 'admin')
        shop_list = Shops.objects.all()

        customers = request.GET.getlist("user[]")
        shops = request.GET.getlist("shop[]")
        status = request.GET.get('status')

        if customers:
            orders = orders.filter(customer__in=User.objects.filter(username__in=customers))
        if shops:
            orders = orders.filter(shop__in=Shops.objects.filter(shop_name__in=shops))
        if status:
            if status != 'all':
                orders = orders.filter(status = status)

        return render(request, self.template_name, {'orders': orders, 'users': users, 'shops': shop_list})
    def post(self, request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        now = datetime.datetime.now()
        filename = 'Orders '+ now.strftime("%d") + '-' + now.strftime("%m") + '-' + now.strftime("%Y") + '-' + now.strftime("%X") +'.csv'
        filepath = BASE_DIR + '/shop/files/' + filename

        fields = ['Shop', 'Customer Name', 'Delivery Status']
        rows = []

        orders = Orders.objects.all()
        customers = request.GET.getlist("user[]")
        shops = request.GET.getlist("shop[]")
        status = request.GET.get('status')

        if customers:
            orders = orders.filter(customer__in=User.objects.filter(username__in=customers))
        if shops:
            orders = orders.filter(shop__in=Shops.objects.filter(shop_name__in=shops))
        if status:
            if status != 'all':
                orders = orders.filter(status = status)

        for order in orders:
            row = [order.shop.shop_name, order.customer_name, order.status]
            print (row)
            rows.append(row)
        
        with open(filepath, 'w') as csvfile: 
            csvwriter = csv.writer(csvfile) 
            csvwriter.writerow(fields) 
            csvwriter.writerows(rows)

        # Open the file for reading content
        path = open(filepath, 'r')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response

class Order(generic.RedirectView):
    def get(self, request):
        shop_name = request.GET.get('shop')
        Orders.objects.create(shop= Shops.objects.get(shop_name=shop_name), customer=request.user, customer_name=request.user.username)
        shop = Shops.objects.filter(shop_name=shop_name)
        shop.update(order_count=shop.first().order_count+1)
        shop.update(pending_count=shop.first().pending_count+1)
        return redirect('home')

class ChangeDeliveryStatus(generic.RedirectView):
    def get(self, request):
        order = Orders.objects.filter(id=request.GET.get('order'))
        order_status = order.first().status
        shop = Shops.objects.filter(id=order.first().shop.id)
        if order_status == 'Delivery Pending':
            shop.update(delivered_count=shop.first().delivered_count+1)
            shop.update(pending_count=shop.first().pending_count-1)
            order.update(status = 'Order Delivered')
        else:
            shop.update(delivered_count=shop.first().delivered_count-1)
            shop.update(pending_count=shop.first().pending_count+1)
            order.update(status = 'Delivery Pending')
        return redirect('dashboard')

# API View
class ShopAPIView(generics.ListCreateAPIView):
    queryset = Shops.objects.all()
    serializer_class = ShopSerializer
    name = 'Shop-List'

    search_fields = [
        '^shop_name'
    ]
    ordering_fields = [
        'order_count'
    ]

class OrderAPIView(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    name = 'Order-List'

    filterset_fields = (
        'status',
    )
    ordering_fields = [
        'id'
    ]
    