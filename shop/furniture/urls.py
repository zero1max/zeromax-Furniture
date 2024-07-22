from django.urls import path
from .views import RegisterView, CustomLoginView, home, FurnitureDetailView,\
      CategoryView, CreateFurniture, DeleteFurniture, shop, DiscountViews,\
      DiscountsDetailView, NewsView, NewsDetailView, user_logout,\
      cart, checkout, clear_cart, to_cart, payment_success, payment,\
      FurnitureView, FurnitureViewCRUD, search

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('furniture/<slug:slug>/', FurnitureDetailView.as_view(), name='detail_url'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category_url'),
    path('create/furniture/', CreateFurniture.as_view(), name='create_furniture_url'),
    path('delete/furniture/<slug:slug>/', DeleteFurniture.as_view(), name='delete_furniture_url'),
    path('shop/', shop, name='shop'),
    path('search/', search, name='search'),
    path('discount/', DiscountViews.as_view(), name='discount'),
    path('discount/<slug:slug>/', DiscountsDetailView.as_view(), name='discount_detail_url'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail_url'),
    path('logout/', user_logout, name='logout'),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
    path("clear/", clear_cart, name="clear"),
    path("to_cart/<int:product_id>/<str:action>/", to_cart, name="to_cart"),
    path("payment/", payment, name="payment"),
    path("success/", payment_success, name="success"),
    path("furnitures/", FurnitureView.as_view(), name="furnitures"),
    path('furnitures/<int:pk>/', FurnitureViewCRUD.as_view(), name="furnituresCRUD"),
]
