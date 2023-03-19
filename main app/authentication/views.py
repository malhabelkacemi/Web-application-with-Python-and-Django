
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm


from pymongo import MongoClient

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if  form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            first_name = form.cleaned_data.get("first_name")
            user = authenticate(username=username, first_name=first_name, password=raw_password)


            success = True
            msg = 'User created'

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})




def Modifier_User(org_email,username,Newemail,role):



    myclient = MongoClient('localhost', 27017)
    users = myclient.UsersOperateur.auth_user


    id=0
    listt = list(users.find())
    for i in listt:
        if(i['email'].strip()==org_email.strip() ):
            id=i['_id']

    users.update_one({"_id":id},
                     {'$set': {'username': username.strip() , 'email': Newemail.strip() , 'first_name': role.strip() }})


def Supprimer_User(org_email):
    myclient = MongoClient('localhost', 27017)
    users = myclient.UsersOperateur.auth_user

    id = 0
    listt = list(users.find())
    for i in listt:
        if (i['email'].strip() == org_email.strip()):
            id = i['_id']


    users.delete_one({"_id":id})





def update_info(request):

    if request.method == "POST":
            print(request.POST)

            print("old value")
            org_email = request.POST.get("org_email", None)

            print("new")
            username = request.POST.get("inputName", None)
            email = request.POST.get("inputEmail", None)
            role = request.POST.get("SelectedRole", None)

            Modifier_User(org_email, username, email, role)


    return render(request, "accounts/Table_Users.html")

def remove_User(request):
    if request.method == "POST":
            org_email = request.POST.get("org_email", None)
            Supprimer_User(org_email)

    return render(request, "accounts/Table_Users.html")