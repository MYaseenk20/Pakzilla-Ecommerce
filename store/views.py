from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import Product,Category,Customer,Order
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
from store.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
# Create your views here.
class home(View):
    def get(self, request):
        products = None
        categorys = Category.objects.all()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.objects.filter(category=categoryID)
        else:
            products = Product.objects.all()
        # print(request.session.get('email'))
        context = {'products': products, 'categorys': categorys}
        return render(request, 'store/home.html', context)
    def post(self,request):
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product]=quantity+1
            else:
                cart[product]=1

        else:
            cart={}
            cart[product]=1

        request.session['cart']=cart
        print(request.session['cart'])
        return redirect('home')
# class home(ListView):
#     model = Product
#     template_name = 'store/home.html'
#     context_object_name = 'products'
#     def get_context_data(self, *args, **kwargs):
#         context=super(home,self).get_context_data(**kwargs)
#         context['categorys']=Category.objects.all()
#         return context
# class storecategory(ListView):
#     model = Product
#     template_name = 'store/home.html'
#     context_object_name = 'products'
#     def get_queryset(self):
#         self.category=self.kwargs['category']
#         return Product.objects.filter(category=self.category)
#     def get_context_data(self, *args, **kwargs):
#         context=super(storecategory,self).get_context_data(**kwargs)
#         context['categorys']=Category.objects.all()
#         context['category']=self.category
#         return context


class Signup(View):
    def get(self,request):
        return render(request, 'store/signup.html')
    def post(self,request):

        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            value = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            }
            error_message=None
            customer_exist = Customer.objects.filter(email=email)
            if len(first_name) < 4:
                error_message = 'First Name must be 4 Character'
            elif len(last_name) < 4:
                error_message = 'Last Name must be 4 Character'
            elif len(email) < 4:
                error_message = 'First Name must be 4 Character'
            elif len(password) < 4:
                error_message = 'First Name must be 4 Character'
            elif customer_exist:
                error_message = 'email address already registered..'
            if not error_message:
                customer = Customer(first_name=first_name, last_name=last_name, email=email, password=password)
                customer.password = make_password(customer.password)
                customer.save()
            else:
                data = {
                    'values': value,
                    'error_message': error_message,
                }
                return render(request, 'store/signup.html', data)

        return render(request, 'store/signup.html')




class Login(View):
    return_url=None
    def get(self, request):
        Login.return_url=request.GET.get('return_url')
        return render(request,'store/login.html')
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.objects.filter(email=email)[0]
        if customer:
            flag=check_password(password,customer.password)
            if flag:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url=None
                    return redirect('home')
            else:
                error_message = 'Email or Password Invalid'
        else:
            error_message = 'Email or Password Invalid'
        return render(request, 'store/login.html',{'error':error_message})

class Cart(View):
    def get(self,request):
        ids=list(request.session.get('cart').keys())
        print(list(request.session.get('cart').keys()))
        products=Product.objects.filter(id__in=ids)
        context={'products':products}
        return render(request,'store/cart.html',context)

class Checkout(View):
    def post(self,request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer=request.session.get('customer')
        cart=request.session.get('cart')
        products=Product.objects.filter(id__in=list(cart.keys()))
        print(customer)
        print(products)
        for product in products:
            order=Order(
                customer=Customer(id=customer),
                product=product,
                phone=phone,
                price=product.price,
                address=address,
                quantity=cart.get(str(product.id))
            )
            order.placeorder();
        request.session['cart']={}

        return redirect('cart')

class OrderView(View):

    def get(self,request):
        customer=request.session.get('customer')
        orders=Order.objects.filter(customer=customer)
        context={'orders':orders}
        return render(request,'store/order.html',context)


def logout(request):
    request.session.clear()
    return redirect('Login')


