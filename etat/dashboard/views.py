
from django.shortcuts import redirect

def home(request):
    #return render(request, 'dashboard/home.html')
    return redirect('member_list')