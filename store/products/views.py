from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'title': 'my title',
        'is_discount' : True,
    }
    return render(request, 'products/index.html', context)

def products(request):
    context = {
        'title': 'Store - Catalog'
    }
    return render(request, 'products/products.html', context)

