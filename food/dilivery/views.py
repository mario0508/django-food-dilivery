from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from time import sleep, time
from django.core.mail import send_mail
from .models import user, Item, orderlog
import random
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML


def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        # print(request.user.email)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            print(user)
            login(request, user)
            request.session['user'] = username
            # return render(request,'Feed.html')
            return redirect('/feed')
        else:
            print('hi')

            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def log_out(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def feed_u(request):
    if request.user.user.type == 'user':
        dic = {'seller': user.objects.filter(type='seller'),'name':request.user.username}
        return render(request, 'feed.html', context=dic)
    elif request.user.user.type == 'seller' and request.POST.get('del') != 'delete' and request.POST.get(
            'edit') != 'edit' and request.POST.get('update') != 'update' and request.POST.get('add')!='add' and request.POST.get('add1')!='add1':

        print('working0')
        print(Item.objects.filter(seller=request.user.user.id))
        dic = {
            'item': Item.objects.filter(seller=request.user.user.id),
        }
        return render(request, 'sfeed.html', context=dic)
    elif request.method == 'POST' and request.POST.get('del') == 'delete' and request.POST.get(
            'edit') != 'edit' and request.POST.get('update') != 'update':
        print('working')

        Item.objects.filter(name=request.POST['iname']).delete()
        dic = {
            'item': Item.objects.filter(seller=request.user.id),
        }
        return render(request, 'sfeed.html', context=dic)
    elif request.POST.get('update') == 'update':
        pname = request.POST.get('item')
        pprice = request.POST.get('price')
        ii=request.session['iid']

        Item.objects.filter(id=ii).update(name=pname, price=pprice)

        dic = {
            'item': Item.objects.filter(seller=request.user.user.id),
        }
        print('qqqq4')
        return render(request, 'sfeed.html', context=dic)
    elif request.POST.get('add')=='add':
        print('redirect')
        return render(request,'add.html')
    elif request.POST.get('add1')=='add1':
        i=request.POST.get('item')
        p=request.POST.get('price')
        s=request.user.user
        print(i,"  ",p," ",s)
        Item.objects.create(name=i,price=p,seller=s)
        dic = {
            'item': Item.objects.filter(seller=request.user.user.id),
        }
        print('qqqq5')
        return render(request, 'sfeed.html', context=dic)

    elif request.method == 'POST' and request.POST['edit'] == 'edit':
        a=request.POST.get('iid')
        request.session['iid']=a
        p=request.POST.get('price')
        n=request.POST.get('iname')
        dic={'p':p,'n':n}

        print("id==>",p)
        print("id==>",p)
        return render(request, 'citem.html',dic)
    else:
        return HttpResponse("HI")


def signup(request):
    if request.method == 'POST':
        u_name = request.POST['uname']
        pasw = request.POST['pasw']
        email = request.POST['email']
        user1 = User.objects.create_user(u_name, email, pasw)
        user2 = user.objects.create(username=user1)
        sleep(5)
        if (user2):
            status = 'Succsess,Go to login page'
        else:
            status = 'Retry'

        return render(request, 'signup.html', {'stat': status})
    else:
        return render(request, 'signup.html')


def ssignup(request):
    if request.method == 'POST':
        u_name = request.POST['uname']
        pasw = request.POST['pasw']
        email = request.POST['email']
        user1 = User.objects.create_user(u_name, email, pasw)
        user2 = user.objects.create(username=user1, type='seller')
        sleep(5)
        if (user2):
            status = 'Succsess,Go to login page'
        else:
            status = 'Retry'

        return render(request, 'ssignup.html', {'stat': status})
    else:
        return render(request, 'ssignup.html')


def menu(request, seller):
    if request.method == 'POST' and request.POST.get('checkout') != 'checkout' and request.POST.get('print') != 'print':
        request.session['qty'] = str(request.session.get('qty', 0)) + ',' + str(request.POST['quantity'])
        request.session['iname'] = str(request.session.get('iname', 0)) + ',' + request.POST['iname']
        request.session['price'] = str(request.session.get('price', 0)) + ',' + str(request.POST['price'])
        print(request.session['qty'], request.session['iname'], request.session['price'])
        # if 'iname'not in request.session:
        # request.session['qty']=0
        #     request.session['iname']=0
        #     request.session['price']=0
        user1 = user.objects.get(username=User.objects.get(username=seller))
        items = Item.objects.filter(seller=user1)
        request.session['seller'] = seller

        dic = {
            'n': range(5),
            'items': items,

        }
        return render(request, 'menu.html', context=dic)

    elif request.POST.get('checkout') == 'checkout':
        print('nbdfkljawqehnlnrl')
        qty = request.session['qty'].split(',')

        name = request.session['iname'].split(',')
        price = request.session['price'].split(',')
        qty.pop(0)
        name.pop(0)
        price.pop(0)
        print(qty, ' ', name, ' ', price)

        totali = []
        for i in range(len(name)):
            t = int(price[i]) * int(qty[i])
            totali.append(t)
        ftotal = sum(totali)
        f = zip(qty, name, totali)
        dic = {
            'f': f,
            'qty': qty,
            'name': name,
            'totali': totali,
            'ftotal': ftotal,
            'ti': range(len(name))
        }
        return render(request, 'bill.html', dic)
    elif request.POST.get('print') == 'print':
        print('nbdfkljawqehnlnrl')
        qty = request.session['qty'].split(',')

        name = request.session['iname'].split(',')
        price = request.session['price'].split(',')
        qty.pop(0)
        name.pop(0)
        price.pop(0)
        print(qty, ' ', name, ' ', price)

        totali = []
        for i in range(len(name)):
            t = int(price[i]) * int(qty[i])
            totali.append(t)
        ftotal = sum(totali)
        f = zip(qty, name, totali)
        dic = {
            'f': f,
            'qty': qty,
            'name': name,
            'totali': totali,
            'ftotal': ftotal,
            'ti': range(len(name))
        }
        html_string = render_to_string('bill.html', dic)
        name = str(name)
        orderlog.objects.create(user=request.session['user'], seller=request.session['seller'], order=name, qty=qty,
                                total=ftotal)

        html = HTML(string=html_string)
        html.write_pdf(target='mypdf.pdf');

        fs = FileSystemStorage('')
        with fs.open('mypdf.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
            return response

        return response

    else:
        user1 = user.objects.get(username=User.objects.get(username=seller))
        items = Item.objects.filter(seller=user1)
        dic = {
            'n': range(5),
            'items': items,
        }
        return render(request, 'menu.html', context=dic)


def mail(request):
    if request.method == 'GET':
        print('1')
        return render(request, 'fpassword.html')
    elif request.method == 'POST' and request.POST['tpe'] == 'otpgen':
        subject = 'Reset Password'
        msg = 'Hey, there use this key as otp '
        a = random.randrange(1111, 9999)
        request.session['otp'] = a
        request.session['otime'] = time()
        request.session['uname'] = request.POST['username']
        n = request.POST['username']
        email = settings.EMAIL_HOST_USER
        msg = msg + ' ' + str(a)
        list1 = list()
        list1.append(User.objects.get(username=n).email)
        print(list1)
        send_mail(subject, msg, email, list1, fail_silently=True)
        print('1')
        return render(request, 'eotp.html')
    elif request.POST['tpe'] == 'otpc':
        d = request.session['otime'] - time()
        o = int(request.POST['otp'])
        s = request.session['otp']
        print(s, o, type(s), type(o), d)
        if o == s and d > int(-122):
            print('done')
            return render(request, "cpass.html")
        elif d < -122:
            return HttpResponse('Time Out')
        elif request.POST['otp'] == request.session['otp']:
            return HttpResponse('Wrong Otp')

    elif request.POST['tpe'] == 'cpass':
        a = request.POST['pass1']
        b = request.POST['pass2']
        if (a == b):
            xx = User.objects.get(username=request.session['uname'])
            xx.set_password(a)
            xx.save()
            return redirect('login')
