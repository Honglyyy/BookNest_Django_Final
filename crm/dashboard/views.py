from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

# Create your views here.
@staff_member_required(login_url='login')
def dashboard_home(request):
    return render(request, 'dashboard/index.html')