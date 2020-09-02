from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product,cart):
    keys=cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False;

@register.filter(name='cart_quantity')
def cart_quantity(product,cart):
    keys=cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0;

@register.filter(name='Total_all_product')
def Total_all_product(product,cart):
    return product.price*cart_quantity(product,cart)



@register.filter(name='Total_cart_product')
def Total_cart_product(products,cart):
    sum = 0 ;
    for p in products:
        sum  += Total_all_product(p,cart)
    return sum


@register.filter(name='total_price')
def total_price(num1,num2):
    return num1*num2;