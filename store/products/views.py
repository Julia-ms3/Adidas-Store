from django.shortcuts import render
from products.models import Category, Product


def index(request):
    context = {
        'title': 'my title',
        'is_discount' : True,
    }
    return render(request, 'products/index.html', context)

def products(request):
    context = {
        'title': 'Store - Catalog',
        'products': Product.objects.all(),
        'categories': Category.objects.all()
    }
    return render(request, 'products/products.html', context)

