from django.shortcuts import render
from .models import Product

# Create your views here.
def product(request):
    product = Product.objects.all()
    
    context={
        'product': product
    }
    
    return render(request, 'myapp/index.html', context)

def detail(request, slug):
    product = Product.objects.get(slug=slug)
    
    context={
        'product': product
    }
    
    return render(request, 'myapp/detail.html', context)

