from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Category, Service

def search(request):
    query = request.GET.get('query', '')
    services = Service.objects.filter(status=Service.ACTIVE).filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

    return render(request, 'search.html', {
        'query': query,
        'services': services
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    services = category.services.filter(status=Service.ACTIVE)

    return render(request, 'category_detail.html', {
        'category': category,
        'services': services,
    })


def service_detail(request, category_slug, slug):
    service = get_object_or_404(Service, slug=slug, status=Service.ACTIVE)

    return render(request, 'service_detail.html', {
        'service': service
    })


