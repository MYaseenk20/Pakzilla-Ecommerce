from django.urls import path
from . import  views
from .views import Login,home,Cart,Checkout,OrderView,Signup
from .middlewares.auth import auth_middleware
# from .views import home
# storecategory
urlpatterns = [
    path('',home.as_view(),name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('Login/', Login.as_view(), name='Login'),
    path('aacart', auth_middleware(Cart.as_view()), name='aacart'),
    path('Checkout/', Checkout.as_view(), name='Checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('logout/', views.logout, name='logout'),

    # path('', home.as_view(), name='home'),
    # path('category/<str:category>/', storecategory.as_view(), name='category'),

]

