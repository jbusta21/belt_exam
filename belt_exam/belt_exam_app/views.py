from django.shortcuts import render, redirect
from django import views
from .models import User, Thoughts, Likes
from django.contrib import messages



def main(request):
    
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("pw_confirmation")
        if len(first_name) < 2 or len(last_name) < 2:
            messages.error(request, "First name or Last name cannot be less than 2 characters")
            return redirect('index')
        try:
            user_exist = User.objects.get(email=email)
        except User.DoesNotExist:
            user_exist = None        
        if user_exist:
            messages.error(request, "User already exist")
            return redirect('index')
        if password != confirm_password:
            messages.error(request, "Passwords must match")
            return redirect('index')

        new_user = User(first_name=first_name, last_name=last_name, email=email, 
                        password=password)
        new_user.save()
        user = User.objects.get(email=email)
        request.session['user_id'] = user.id
        all_jobs = Thoughts.objects.all()
        return redirect('dashboard')
        

def login(request):
    if request.method=='POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)        
        except User.DoesNotExist:
            user = None
        if user is None:
            messages.error(request, "User does not exist")
            return redirect('index')
        print(user, "+++")
        if user.password != password:
            messages.error(request, "Incorrect credentials")
            return redirect('index')
        request.session['user_id'] = user.id
        # all_jobs = Thoughts.objects.all()
        return redirect('dashboard')

def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('index')


def dashboard(request):
    logged_user = request.session.get('user_id')
    if not logged_user:
        messages.error(request, "You need to login in")
        return redirect('index')

    user = User.objects.get(id=logged_user)
    # if request.method == "POST":
    #     thought = request.POST.get("thought")
    #     new_thought = Thoughts(title=thought, user=user)
    #     new_thought.save()
    all_jobs = Thoughts.objects.all()
    my_jobs = Likes.objects.filter(user_id=logged_user)
    return render(request, 'dashboard.html', {"jobs": all_jobs, "myjobs": my_jobs, "user": user})

def addJob(request):
    logged_user = request.session.get('user_id')
    if not logged_user:
        messages.error(request, "You need to login in")
        return redirect('index')

    user = User.objects.get(id=logged_user)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        location = request.POST.get("location")
        new_job = Thoughts(title=title, description=description, location=location, user=user)
        new_job.save()
        all_jobs = Thoughts.objects.all()
        return redirect('dashboard')
    else:
        return render(request, 'addJob.html', {"user": user})


# def thoughts(request):
#     logged_user = request.session.get('user_id')
#     if not logged_user:
#         messages.error(request, "You need to login in")
#         return redirect('index')

#     user = User.objects.get(id=logged_user)
#     if request.method == "POST":
#         thought = request.POST.get("thought")
#         new_thought = Thoughts(title=thought, user=user)
#         new_thought.save()
#     all_thoughts = Thoughts.objects.all()
#     return render(request, 'thoughts.html', {"thoughts": all_thoughts, "user": user})


def get_job(request, id):
    logged_user = request.session.get('user_id')
    if not logged_user:
        messages.error(request, "You need to login in")
        return redirect('index')
    try:
        job = Thoughts.objects.get(id=id)
    except Thoughts.DoesNotExist:
        job = Likes.objects.get(id=id)
    return render(request, 'view.html', {"job": job})


def edit(request, id):
    logged_user = request.session.get('user_id')
    if not logged_user:
        messages.error(request, "You need to login in")
        return redirect('index')
    job = Thoughts.objects.get(id=id)    
        
    return render(request, 'edit.html', {"job": job})

def update(request):
    title = request.POST.get("title")
    description = request.POST.get("description")        
    location = request.POST.get("location")
    updateId = request.POST.get("updateId")
    existed_job = Thoughts.objects.get(pk=updateId)
    existed_job.title = title
    existed_job.description = description
    existed_job.location = location
    existed_job.save()
    return redirect('dashboard')

def remove(request, id):
    job = Thoughts.objects.get(pk=id)
    job.delete()
    return redirect('dashboard')


def addMyJob(request, id):
    logged_user = request.session.get('user_id')
    if not logged_user:
        messages.error(request, "You need to login in")
        return redirect('index')
    job = Thoughts.objects.get(id=id)
    user = User.objects.get(id=logged_user)
    like = Likes(user_id=user, title=job.title, description=job.description, location=job.location)
    like.save()
    job.delete()
    return redirect('dashboard')


def removeMyJob(request, id):
    job = Likes.objects.get(pk=id)
    job.delete()
    return redirect('dashboard')
    
# def groups(request):
#     return render(request, 'groups.html')

# def new(request):
#     return render(request, 'groups.html')