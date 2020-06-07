# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import auth,messages
from .forms import *
from .models import signup
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import *
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
# import pymysql
import math
import numpy as np
import pandas as pd
import requests
import xmltodict
import json
from flask import request, jsonify
from django.contrib.auth.forms import AuthenticationForm

# conn = pymysql.connect(
#     host = '127.0.0.1',
#     port = 3306,
#     user = 'root',
#     password = 'Rasam@22',
#     database = 'bookReview',
#     autocommit = True
# )

def registration(request):
    if request.method == 'POST':
        print('dddd')
        form = register(request.POST)
        if form.is_valid():
            print('xxxxxxxxxxxxxx')
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            firstname=form.cleaned_data['firstname']
            lastname=form.cleaned_data['lastname']
            password=form.cleaned_data['password']
            # response=signup(username=username,email=email,firstname=firstname,lastname=lastname,password=password)
            #isActive=2 means false
            # response.save()
            
            user=form.save(commit=False)
            user.set_password(password)
            user.is_active=False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your ReadersLand account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            #to_email = form.cleaned_data.get('email')
            Email = EmailMessage(
                        mail_subject, message,settings.EMAIL_HOST_USER, to=[email]
            )
            Email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            print(form.errors)
    else:
        form = register()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # cur=conn.cursor()
        # sql='Update signup set isActive=%s where username=%s'
        # query=(1,user.username)
        # cur.execute(sql,query)
        # conn.commit()
        # cur.close()
        signup.objects.filter(username=user.username).update(isActive=1)
        # response=signup(username=user.username,email=user.email,firstname=user.firstname,lastname=user.lastname,password=user.password)
        # response.save()
        print(user)
        auth.login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('pass')
        form=AuthenticationForm(request.POST)
        user=authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['name']=user.username
            return render(request,'index.html',{'name':user.username.upper()})
        else:
            messages.error(request,'username or password is invalid')
    else:
        form = AuthenticationForm()
    return render(request, 'signup.html', {'form': form})

def logout(request):
    auth.logout(request)
    form = AuthenticationForm()
    return render(request, 'signup.html', {'form': form})

def getsimilar(request):
    name=request.session.get('name')
    return render(request,'similarbooks.html',{'name':name.upper()})

def getSimilarBooks(title,titles,publYrS,ratingS,pagesS,reviewsS,publYrO,ratingO,pagesO,reviewsO):
        url=' https://www.goodreads.com/book/title.xml'
        parameters={"key":' laszLDheUrLhOPhB43g',"title":title}
        result = requests.get(url,params=parameters)
        my_dict = xmltodict.parse(result.content)
        x=my_dict['GoodreadsResponse']['book']
        if 'id' in x:
            idb=x['id']
        url='https://www.goodreads.com/book/show.xml'
        parameters={"key":' laszLDheUrLhOPhB43g',"id":idb}
        result = requests.get(url,params=parameters)
        my_dict = xmltodict.parse(result.content)
        x=my_dict['GoodreadsResponse']['book']
        tempt=my_dict['GoodreadsResponse']['book']['title']
        tempi=my_dict['GoodreadsResponse']['book']['id']
        if 'publication_year' in x:
            publicationYear=my_dict['GoodreadsResponse']['book']['publication_year']
        if 'average_rating' in x:
            ratingsAvg=my_dict['GoodreadsResponse']['book']['average_rating']
        if 'num_pages' in x:
            pages=my_dict['GoodreadsResponse']['book']['num_pages']
        if 'reviews_count' in x['work']:
            review=my_dict['GoodreadsResponse']['book']['work']['reviews_count']['#text']
        if 'similar_books' in x:
            ans=my_dict['GoodreadsResponse']['book']['similar_books']['book']
            cnt=0;
            for j in ans:
                flag=0
                if cnt<5:
                    idb1=j['id']
                    title=j['title']
                    df=pd.read_csv('reject.csv')
                    for i,row in df.iterrows():
                        if row["names"]==title:
                            flag=1
                            break
                    for i in range(len(titles)):
                        if titles[i]==title:
                            flag=1
                            break
                    if flag==0:
                        titles.append(j['title'])
                        if j['publication_year'] != None:
                            publYrS.append(int(j['publication_year']))
                        else:
                            publYrS.append(0)               
                        if j['average_rating'] != None:
                            ratingS.append(float(j['average_rating']))
                        else:
                            ratingS.append(0)
                        if j['num_pages'] != None:
                            pagesS.append(int(j['num_pages']))
                        else:
                            pagesS.append(0)
                        cnt=cnt+1
                        url='https://www.goodreads.com/book/show.xml'
                        parameters={"key":' laszLDheUrLhOPhB43g',"id":idb1}
                        result = requests.get(url,params=parameters)
                        my_dict = xmltodict.parse(result.content)
                        x=my_dict['GoodreadsResponse']['book']['work']
                        reviewsS.append(int(x['reviews_count']['#text']))

        else:
            print('no similar books exist')
        
        if publicationYear != None:
            publYrO.append(int(publicationYear))
        else:
            publYrO.append(0)
        if ratingsAvg != None:
            ratingO.append(float(ratingsAvg))
        else:
            ratingO.append(0)
        if pages != None:
            pagesO.append(int(pages))
        else:
            pagesO.append(0)
        if review != None:
            reviewsO.append(int(review))
        else:
            reviewsO.append(0)

def getBooks(request):
    publication=[]
    rating=[]
    reviewsS=[]
    reviewsO=[]
    reviews=[]
    distance=[]
    publYrS=[]
    ratingS=[]
    publYrO=[]
    page=[]
    pagesO=[]
    pagesS=[]
    ratingO=[]
    titles=[]
    name=request.session.get('name')
    title1=request.POST.get('name1')
    title2=request.POST.get('name2')
    title3=request.POST.get('name3')
    getSimilarBooks(title1,titles,publYrS,ratingS,pagesS,reviewsS,publYrO,ratingO,pagesO,reviewsO);
    getSimilarBooks(title2,titles,publYrS,ratingS,pagesS,reviewsS,publYrO,ratingO,pagesO,reviewsO);
    getSimilarBooks(title3,titles,publYrS,ratingS,pagesS,reviewsS,publYrO,ratingO,pagesO,reviewsO);

    x=len(publYrS)
    x1=publYrO[0]
    x2=publYrO[1]
    x3=publYrO[2]
    for i in range(x):
        dist=math.sqrt((publYrS[i]-x1)**2+(publYrS[i]-x2)**2+(publYrS[i]-x3)**2)
        publication.append(dist)
    y=len(ratingS)
    y1=ratingO[0]
    y2=ratingO[1]
    y3=ratingO[2]
    for i in range(y):
        dist=math.sqrt((ratingS[i]-y1)**2+(ratingS[i]-y2)**2+(ratingS[i]-y3)**2)
        rating.append(dist)   
    z=len(pagesS)
    z1=pagesO[0]
    z2=pagesO[1]
    z3=pagesO[2]
    for i in range(z):
        dist=math.sqrt((pagesS[i]-z1)**2+(pagesS[i]-z2)**2+(pagesS[i]-z3)**2)
        page.append(dist)
    w=len(reviewsS)
    w1=reviewsO[0]
    w2=reviewsO[1]
    w3=reviewsO[2]
    for i in range(w):
        dist=math.sqrt((reviewsS[i]-w1)**2+(reviewsS[i]-w2)**2+(reviewsS[i]-w3)**2)
        reviews.append(dist)

    yr=15
    rate=4
    pg=8
    rv=6
    x=len(rating)
    for i in range(x):
        dist=rating[i]*rate+publication[i]*yr+page[i]*pg+reviews[i]*rv
        distance.append(dist)

    for i in range(1,x):
        data=distance[i]
        book=titles[i]
        j=i-1
        while data<distance[j] and j>=0:
            distance[j+1]=distance[j]
            titles[j+1]=titles[j]
            j=j-1
        distance[j+1]=data
        titles[j+1]=book

    # print(titles)
    return render(request,'similarbooksWithOutput.html',{'name':name.upper(),'title1':title1,'title2':title2,'title3':title3,'list':titles})

def home(request):
    name=request.session.get('name')
    return render(request,'index.html',{'name':name.upper()})

def getInfo(request):
    name=request.session.get('name')
    return render(request,'bookInfo.html',{'name':name.upper()})

def getNames(request):
    name=request.session.get('name')
    return render(request,'bookNames.html',{'name':name.upper()})

def getTitles(request):
    name=request.session.get('name')
    keyword=request.POST.get('name1')
    info=[]
    url=' https://www.goodreads.com/search/index.xml'
    parameters={"key":' laszLDheUrLhOPhB43g',"q":keyword}
    result = requests.get(url,params=parameters)
    my_dict = xmltodict.parse(result.content)
    x=my_dict['GoodreadsResponse']['search']['results']['work']
    for i in x:
        ans=i['best_book']
        info.append(ans['title'])
    print(info)
    return render(request,'bookNamesWithOutput.html',{'name':name.upper(),'keyword':keyword,'list':info})


def getDetails(request):
    name=request.session.get('name')
    title=request.POST.get('name1')
    info=[]
    url=' https://www.goodreads.com/book/title.xml'
    parameters={"key":' laszLDheUrLhOPhB43g',"title":title}
    result = requests.get(url,params=parameters)
    my_dict = xmltodict.parse(result.content)
    x=my_dict['GoodreadsResponse']['book']
    if 'id' in x:
        idb=x['id']
    url='https://www.goodreads.com/book/show.xml'
    parameters={"key":' laszLDheUrLhOPhB43g',"id":idb}
    result = requests.get(url,params=parameters)
    my_dict = xmltodict.parse(result.content)
    x=my_dict['GoodreadsResponse']['book']
    info.append("Title : {}".format(x['title']))
    info.append("Book id :{}".format(idb))
    info.append("Image Url :{}".format(x['image_url']))
    info.append("Averge Rating : {}".format(x['average_rating']))
    info.append("Author : {}".format(x['authors']['author']['name']))
    print(info)
    return render(request,'bookInfoWithOutput.html',{'name':name.upper(),'title1':title,'BookName':title,'details':info})
