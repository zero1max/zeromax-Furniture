from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, FurnitureModelForm, ShippingAddressForm, CustomerForm
from .models import Furniture, Category, Discount, News, WeHelp, Benefits, Customer
import random
from .utils import get_cart_data, CartForAuthenticatedUser
from django.conf import settings
from django.utils.text import slugify


import stripe


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'furniture/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Signup'
        return context

class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'furniture/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('home')

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    furnitures = list(Furniture.objects.filter(is_published=True))
    random.shuffle(furnitures)
    categories = Category.objects.all()
    news = News.objects.filter(is_published=True)
    discounts = Discount.objects.filter(is_published=True)
    wehelp = WeHelp.objects.all()
    benefits = Benefits.objects.all()
    context = {
        'furnitures': furnitures,
        'categories': categories,
        'wehelps': wehelp,
        'benefits': benefits,
        'news': news,
        'discounts': discounts,
        'title': 'Home',
    }
    return render(request, 'furniture/home.html', context)

def shop(request):
    furnitures = Furniture.objects.filter(is_published=True)
    categories = Category.objects.all()
    context = {
        'furnitures': furnitures,
        'categories': categories,
        'title': 'Shop'
    }
    return render(request, 'furniture/shop.html', context)

class FurnitureDetailView(DetailView):
    model = Furniture
    template_name = 'furniture/furniture_detail.html'
    context_object_name = 'furniture'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Furniture, slug=slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Furniture Detail'
        return context

class CategoryView(DetailView):
    model = Category
    template_name = 'furniture/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['furnitures'] = Furniture.objects.filter(category_id=self.kwargs['pk'])
        context['categories'] = Category.objects.all()
        return context

class CreateFurniture(CreateView):
    model = Furniture
    form_class = FurnitureModelForm
    template_name = 'furniture/create_item.html'
    success_url = reverse_lazy('home')

class DeleteFurniture(DeleteView):
    model = Furniture
    template_name = 'furniture/delete_confirm.html'
    success_url = reverse_lazy('home')

class DiscountViews(ListView):
    model = Discount
    template_name = 'furniture/discount.html'
    context_object_name = 'discounts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Discounts'
        return context
    
    
class DiscountsDetailView(DetailView):
    model = Discount
    template_name = 'furniture/discount_detail.html'
    context_object_name = 'discount'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Discount, slug=slug)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Discount Detail'
        return context

class NewsView(ListView):
    model = News
    template_name = 'furniture/news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'News'
        return context

class NewsDetailView(DetailView):
    model = News
    template_name = 'furniture/news_detail.html'
    context_object_name = 'news'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(News, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'News Detail'
        return context

def cart(request):
    cart_info = get_cart_data(request)
    context = {
        "products": cart_info["products"],
        "order": cart_info["order"],
        "cart_total_price": cart_info["cart_total_price"],
        "cart_total_quantity": cart_info["cart_total_quantity"],
        "title": "Cart"
    }
    return render(request, 'furniture/cart.html', context)

def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, product_id, action)
        return redirect('cart')
    else:
        messages.error(request, "You are not authenticated")
        return redirect('login')

def checkout(request):
    cart_info = get_cart_data(request)
    context = {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'order': cart_info['order'],
        'products': cart_info['products'],
        'customer_form': CustomerForm,
        'shipping_form': ShippingAddressForm,
        'title': "checkout"
    }
    return render(request, 'furniture/checkout.html', context)

def clear_cart(request):
    # Implement cart clearing logic
    pass

def payment(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == "POST":
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.name = customer_form.cleaned_data['name']
            customer.email = customer_form.cleaned_data['email']
        shipping_form = ShippingAddressForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()['order']
            address.save()
        total_price = cart_info['cart_total_price']
        total_quantity = cart_info['cart_total_quantity']
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': "Products of Furni"
                        },
                        'unit_amount': int(total_price)
                    },
                    'quantity': total_quantity
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('success'))
        )
        return redirect(session.url, 303)


def payment_success(request):
    return render(request,"furniture/success.html")
