from django.shortcuts import render



def index(request):
    return render(request, 'index.html')



from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('index')  # Redirects to the 'index' page