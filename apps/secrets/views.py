from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count
from .models import User, Secret
# Create your views here.
def index(request):
    try:
        request.session['user_id']
        return redirect('/success')
    except:
        return render(request, 'secrets/index.html')
def register(request):
    if request.method == "POST":
        register_query = User.objects.register(request.POST)
        if register_query[0]:
            request.session['user_id'] = register_query[1]
            messages.info(request, "Thank you for registering!")
            return redirect('/success')
        else:
            for error in User.objects.register(request.POST)[1]:
                messages.info(request, error)
            return redirect('/')
    else:
        return redirect('/')
def success(request):
    if 'user_id' not in request.session:
        messages.info(request, "Please log in.")
        return redirect('/')
    context = {
        'secrets': Secret.objects.annotate(num_likes=Count('likes')),
        'current_user': User.objects.filter(id = request.session['user_id'])
    }
    return render(request, 'secrets/success.html', context)
def login(request):
    if request.method == 'POST':
        if User.objects.login(request.POST):
            request.session['user_id'] = User.objects.filter(email = request.POST['log_email'])[0].id
            messages.info(request, "You've successfully logged in.")
            return redirect('/success')
    return redirect('/')
def logout(request):
    if request.method == 'GET':
        return redirect('/success')
    request.session.clear()
    messages.info(request, "You've successfully logged out. Have a nice day!")
    return redirect('/')
def post_secret(request):
    Secret.objects.post(request.POST['secret_post'], request.session['user_id'])
    return redirect('/success')
def nonsense(request):
    messages.info(request, "Page not found")
    return redirect('/')
def like(request, secret_id):
    Secret.objects.get(id = secret_id).likes.add(User.objects.get(id = request.session['user_id']))
    return redirect('/success')
def del_like(request, secret_id):
    Secret.objects.get(id = secret_id).delete()
    return redirect('/success')
def most_liked(request):
    context = {
        "most_liked": Secret.objects.annotate(num_likes = Count('likes')).order_by('-num_likes')[:10]
    }
    return render(request, 'secrets/most_liked.html', context)
