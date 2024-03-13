from django.shortcuts import render
from storefront.models import Service
def frontpage(request):
    services =Service.objects.filter(status=Service.ACTIVE)[0:6]

    return render(request, 'frontpage.html', {
        'services': services
    })

def about(request):
    return render(request, 'about.html')


