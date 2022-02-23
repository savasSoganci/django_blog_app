import json
from django.forms import formset_factory
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import (Post)
from blog.forms import (RegistrationForm,AccountAuthenticationForm,AddPostForm)
from django.contrib.auth import login,authenticate
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    return HttpResponse("Blog Home")


def about(request):
    return HttpResponse("Blog About")


def blog_title_getirme(request):
    posts = Post.published.all()
    return render(request, "index.html", {"posts": posts})


def blog_object(request,id):
    post=get_object_or_404(Post,id=id)
    #post=Post.published.filter(id=id).first().first()  Burada bir dizi değil obje döndürüyon forla kullanamazsın. Forla kullancaksan firstsüz halini yaz.
    return render(request,"indexbody.html",{"post1":post})


def registration_view(request):
    context={}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)#Dolu yollayınca var mı diye bakıyo varsa doluyu boşsa boş nesneyi, boş yollayınca boş bir tane bize geri mi döndürüyo?
        if form.is_valid():
            form.save()
            email=form.cleaned_data.get('email')#yoksa none döner.(defaultta bile none döndürür. Sorun o)
            username=form.cleaned_data['username']#yoksa keyerror döner. (SEN YİNE DE İKİSİNİN FARKINA BAK)
            raw_password=form.cleaned_data.get('password1')
            account=authenticate(email=email,username=username, password=raw_password)
            login(request,account)
            return redirect('blog:index')
        else:
            context['registration_form']=form
    else:
        form=RegistrationForm()
        context['registration_form']=form
    return render(request, 'register.html',context)


def logout_view(request):
    logout(request)
    return redirect('blog:index')    


def login_view(request):#add postta kayıtlı değilse loginde girişi sağladığında ana syafa yerine başta istek attığı sayfaya gitsin.
    context={}
    user=request.user
    if user.is_authenticated:
        return redirect("blog:index")    
    if request.method == 'POST':
        form=AccountAuthenticationForm(request.POST)#bu sonradan ölüyor mu duruyor mu
        if form.is_valid():
            print("is_valid")
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('blog:index')##ana sayfa burası
            else:
                messages.error(request, 'Invalid login.')
                return redirect("blog:login") 
    else:
        form=AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'login.html', context) #html'de context[] diye yazmama sebebini sor. Fonkların içine girdim ama bir yerde kafam karıştı.                  


def my_repository(request):
    if request.user.is_authenticated:
        user_posts=Post.objects.filter(author=request.user)
        return render(request,"repository.html",{"user_posts":user_posts})
    else:
        return redirect("blog:login")


def add_post(request):
    #import ipdb;ipdb.set_trace()
    user=request.user
    if not user.is_authenticated:#Djangonun gömülü authenticated kontrolü yapan decoratorü var. Onu kullan
        return redirect("blog:login")
    context={}
    if request.method == 'POST':
        form = AddPostForm(request.POST,request.FILES)#Dolu yollayınca var mı diye bakıyo varsa doluyu boşsa boş nesneyi, boş yollayınca boş bir tane bize geri mi döndürüyo?
        if form.is_valid():
            obj=form.save(commit=False)
            obj.author=request.user
            obj.save()
            return redirect('blog:index')
        context['add_post_form']=form

    else:
        form=AddPostForm()
        context['add_post_form']=form
    return render(request, 'addPost.html',context)    


def update_post(request,id):
    user=request.user
    if not user.is_authenticated:#Djangonun gömülü authenticated kontrolü yapan decoratorü var. Onu kullan
        return redirect("blog:login")
    context={}
    blog_post=get_object_or_404(Post,id=id)
    if(request.POST==True):
        form=AddPostForm()


def post_slug_update(request):
    if request.method == 'POST':
        post_title = request.POST.get('title_value')
        title_slug=Post.making_slug(post_title)#generate_slug diyebilirsin. ing'li isimlendirme yapma.
        return HttpResponse(title_slug)#Json response yap burayı
    return HttpResponse(status=405)    

