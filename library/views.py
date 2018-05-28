from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login as django_login, logout as django_logout, authenticate

from .forms import LoginForm
from library.forms import *
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from library.models import *
from django.db.models import Q

def login(request):
    print("Let's login!")
    if request.method == 'POST':
        # Data bounded form인스턴스 생성
        login_form = LoginForm(request.POST)
        # 유효성 검증에 성공할 경우
        if login_form.is_valid():
            # form으로부터 username, password값을 가져옴
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # 가져온 username과 password에 해당하는 User가 있는지 판단한다
            # 존재할경우 user변수에는 User인스턴스가 할당되며,
            # 존재하지 않으면 None이 할당된다
            # PASS the authenticate session...
            """user = authenticate(
                username=username,
                password=password
            )
            if user :
                django_login(request, user)
                return redirect('main')
                #form=Form()
                #return render(request, 'library/main.html', {'form':form})
            # 인증에 성공했을 경우

            # 겉보기에만 Login으로 보이도록....
            else :
                try :
                    client_backend = Client.objects.get(cid=username)
                    return redirect('main')
                    #form=Form()
                    #return render(request, 'library/main.html', {'form':form})
                except :
                    pass"""
            if username == password :
                try :
                    context = Client.objects.get(cid=username)
                    request.session['user_cid'] = context.cid
                    #return render(request, 'library/main.html', {'form':form})
                    return redirect('main')
                except Client.DoesNotExist :
                    pass
            #if user:
                # Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다
            #    django_login(request, user)
                # Post목록 화면으로 이동
            #    return redirect('login')
            # 인증에 실패하면 login_form에 non_field_error를 추가한다
            login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'library/login.html', context)

def logout(request):
    try:
        del request.session['user_cid']
    except KeyError:
        pass

    return render(request, 'library/logout.html')

def main(request):
    if request.session.get('user_cid') :
        print("GOOD!")
        print(request.session['user_cid'])
    form=Form()
    borrowing_count = len(Book.objects.all().filter(cid=request.session['user_cid']))
    # SEMINAR ROOM AUTO RETURNING... IS NEEDED?
    reserving_count = len(SeminarUse.objects.all().filter(cid=request.session['user_cid']))
    return render(request, 'library/main.html', {'form':form, 'borrowing_count':borrowing_count, 'reserving_count':reserving_count})

def search(request):
    form=request.POST['search']
    #please put 404 not found later one.
    ref=request.POST['ref']
    form=form.strip()
    if form=='':
    	return main(request)

    new_form=''
    for i in form:
    	if i !=' ':
    		new_form+='['+i.lower()+i.upper()+']'
    	else:
    		new_form+=' '
    form = new_form.split()
    string='('
    string+= form[0]
    for i in form[1:]:
    	string+='|' +i
    string+=')'
    if ref=="all":
    	context=Book.objects.filter(Q(name__regex=string)| Q(author__regex=string) )
    elif ref=="name":
    	context=Book.objects.filter(Q(name__regex=string))
    elif ref=="author" :
    	context=Book.objects.filter(Q(author__regex=string))

    return render(request, 'library/search.html', {'context':context.order_by('name')})

def borrow(request, borrow):
    borrowing_cid = request.session['user_cid']
    client = Client.objects.get(cid=borrowing_cid)
    borrow_limit = 3 if client.c_type == 'student' else 5
    if len(Book.objects.all().filter(cid=borrowing_cid)) > borrow_limit :
        # Borrow Permitted
        pass
    book=Book.objects.get(code=borrow)
    book.cid = Client.objects.get(cid=borrowing_cid)
    book.save()

    return render(request, 'library/borrow.html', {'book':book})

def seminar(request) :
    usage = SeminarUse.objects.all()
    seminar = SeminarRoom.objects.all()
    return render(request, 'library/seminar.html', {'seminar':seminar, 'usage':usage})

def staff(request) :
    cstaff = Staff.objects.filter(lname = 'Cultural')
    mstaff = Staff.objects.filter(lname = 'Munji')
    bstaff = Staff.objects.filter(lname = 'Business')
    return render(request,'library/staff.html', {'cstaff':cstaff,'mstaff':mstaff,'bstaff':bstaff})

def reservation(request, slug) :
    from datetime import datetime
    seminar = get_object_or_404(SeminarRoom, pk=slug)
    seminar_use = SeminarUse.objects.create(cid=Client.objects.get(cid=request.session['user_cid']), rname=seminar, date=datetime.today().strftime("%Y-%m-%d"))
    return render(request, 'library/reservation.html', {'seminar':seminar})

def return_book(request) :
    borrowing_cid = request.session['user_cid']
    borrowed_book = Book.objects.filter(cid = borrowing_cid)
    return render(request, 'library/return_book.html', {'books':borrowed_book})

def return_book_complete(request, return_book) :
    book = get_object_or_404(Book, pk=return_book)
    book.cid = None
    book.save()
    return render(request, 'library/return_book_complete.html', {'book':book})
