from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, get_object_or_404, HttpResponse, render_to_response
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
                    if username[0] == 'a' :
                        context = Staff.objects.get(sid=username[1:])
                        request.session['user_id'] = context.sid
                        request.session['authorization'] = 1
                    else :
                        context = Client.objects.get(cid=username)
                        request.session['user_id'] = context.cid
                        request.session['authorization'] = 0
                    #return render(request, 'library/main.html', {'form':form})
                    return redirect('main')
                except Client.DoesNotExist or Staff.DoesNotExist :
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
        del request.session['user_id']
    except KeyError:
        pass

    return render(request, 'library/logout.html')

def main(request):
    if request.session.get('user_id') :
        print("GOOD!")
        print(request.session['user_id'])
        print(request.session['authorization'])
    else :
        # Rendering error page
        pass

    # Staff Case
    if int(request.session['authorization']) :
        form=Form()
        staff = Staff.objects.get(sid=request.session['user_id'])
        return render(request, 'library/main_staff.html', {'form':form, 'job_name':staff.s_type})
    # Client Case
    else :
        form=Form()
        ranking = popular_book.objects.all()[:10]
        borrowing_count = len(BookChecked.objects.all().filter(state='borrowing').filter(ccode=request.session['user_id']))
        # SEMINAR ROOM AUTO RETURNING... IS NEEDED?
        reserving_count = len(SeminarUse.objects.all().filter(cid=request.session['user_id'], state='accept'))
        sum = 0
        import datetime
        date = datetime.datetime.now()
        book = BookChecked.objects.all().filter(ccode=request.session['user_id'], state='borrowing')
        for iter in book :
            delta = date-datetime.datetime.strptime(str(iter.date), "%Y-%m-%d")
            if int(delta.days) >= 0:
                sum += int(delta.days)*100

        return render(request, 'library/main.html', {'fee':sum, 'form':form, 'ranking':ranking, 'borrowing_count':borrowing_count, 'reserving_count':reserving_count})

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

    borrowing = BookChecked.objects.filter(state='borrowing')

    return render(request, 'library/search.html', {'context':context.order_by('name'), 'borrowing':borrowing})

def borrow(request, borrow):
    borrowing_cid = request.session['user_id']
    client = Client.objects.get(cid=borrowing_cid)
    borrow_limit = 3 if client.c_type == 'student' else 5
    if len(BookChecked.objects.all().filter(ccode=borrowing_cid).filter(state='borrowing')) > borrow_limit - 1 :
        # Borrow Permitted
        #return HttpResponse("You cannot borrow more than {} books".format(borrow_limit))
        return render_to_response('library/alarm.html', {'message':'You cannot borrow more than {} books'.format(borrow_limit)})
    #book=Book.objects.get(code=borrow)
    import datetime
    #book.due = datetime.today().strftime("%H:%M")
    print("What is borrow?")
    borrowed_book = Book.objects.get(pk=borrow)
    #borrow_date = datetime.today().strftime("%Y-%m-%d")
    borrow_date = datetime.datetime.now() + datetime.timedelta(days=2)
    if len(BookChecked.objects.filter(bcode=borrow, ccode=borrowing_cid, state='borrowing')) > 0 :
        #return HttpResponse("Cannot borrow already borrowed book")
        return render_to_response('library/alarm.html', {'message':'Cannot borrow already borrowed book'})
    if len(BookChecked.objects.filter(bcode=borrow, ccode=borrowing_cid, date=borrow_date.strftime("%Y-%m-%d"))) > 0 :
        #return HttpResponse("Cannot borrow same book at same day")
        return render_to_response('library/alarm.html', {'message':'Cannot borrow same book at same bay'}) 
    BookChecked.objects.create(bcode=borrowed_book, ccode=Client.objects.get(pk=borrowing_cid), state='borrowing', date=borrow_date.strftime("%Y-%m-%d"))
    #book.cid = Client.objects.get(cid=borrowing_cid)
    #book.save()

    return render(request, 'library/borrow.html', {'book_name':borrowed_book.name, 'borrow_date':borrow_date})

def seminar_show(request) :
    seminars = SeminarUse.objects.filter(cid=Client.objects.get(cid=request.session['user_id']))
    return render(request, 'library/seminar_show.html', {'seminars':seminars})

def seminar(request) :
    if request.method == 'POST' :
        request_form = SeminarForm(request.POST)
        if request_form.is_valid() :
            borrow_date = request_form.cleaned_data['borrow_date']
        room_name = request.POST['room']
        seminar = get_object_or_404(SeminarRoom, pk=room_name)
        import datetime
        if datetime.date.today() > borrow_date :
            return HttpResponse("Please setting borrow date should be after today")
        if len(SeminarUse.objects.filter(cid=Client.objects.get(cid=request.session['user_id']), rname=seminar)) :
            return HttpResponse("Cannot borrow same seminar room more than once")
        SeminarUse.objects.create(cid=Client.objects.get(cid=request.session['user_id']), rname=seminar, date=borrow_date, state='ready')
        return render(request, 'library/reservation.html', {'seminar':seminar})
    else :
        form = SeminarForm()
        usage = SeminarUse.objects.filter(state='accept')
        seminar = SeminarRoom.objects.all()
        return render(request, 'library/seminar.html', {'form':form, 'seminar':seminar, 'usage':usage})

def seminar_confirm(request, client, seminar) :
    SeminarUse.objects.filter(cid=client, rname=seminar, state='reject').delete()
    return render(request, 'library/complete.html', {'title':'REJECT confirmed', 'content':'You confirm seminar room reservation request rejected'})


def staff(request) :
    cstaff = Staff.objects.filter(lname = 'Cultural')
    mstaff = Staff.objects.filter(lname = 'Munji')
    bstaff = Staff.objects.filter(lname = 'Business')
    return render(request,'library/staff.html', {'cstaff':cstaff,'mstaff':mstaff,'bstaff':bstaff})

def reservation(request, slug) :
    if request.method == 'POST' :
        request_form = SeminarForm(request.POST)
        if request_form.is_valid() :
            borrow_date = request_form.cleaned_data['borrow_date']
            print(borrow_date)
    else :
        from datetime import datetime
        borrow_date = datetime.today().strftime("%Y-%m-%d")
    seminar = get_object_or_404(SeminarRoom, pk=slug)
    seminar_use = SeminarUse.objects.create(cid=Client.objects.get(cid=request.session['user_id']), rname=seminar, date=borrow_date, state='ready')
    return render(request, 'library/reservation.html', {'seminar':seminar})

def return_book(request) :
    borrowing_cid = request.session['user_id']
    borrowed_book = BookChecked.objects.filter(ccode = borrowing_cid).filter(state='borrowing')
    return render(request, 'library/return_book.html', {'books':borrowed_book})

def return_book_complete(request, return_book) :
    print(return_book)
    book = get_object_or_404(Book, pk=return_book)
    book_record= BookChecked.objects.filter(bcode=return_book, state='borrowing', ccode=request.session['user_id']).update(state='returned')
    return render(request, 'library/return_book_complete.html', {'book':book})

def request_book(request) :
    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        if request_form.is_valid() :
            book_name = request_form.cleaned_data['book_name']
            author = request_form.cleaned_data['author']
            genre = request_form.cleaned_data['genre']
            new_book_request = BookRequest.objects.create(name=book_name, author=author, genre=genre,
                cid=Client.objects.get(cid=request.session['user_id']), state='ready')

            print(book_name, author, genre)
        return redirect('request')

    else :
        form = RequestForm()
        id = request.session['user_id']
        request_queue = BookRequest.objects.filter(cid=request.session['user_id'])

        return render(request, 'library/request.html', {'form':form, 'books':request_queue})



def book_staff(request) :
    id = request.session['user_id']
    staff = Staff.objects.get(sid=id)
    if staff.s_type != 'librarian' and staff.s_type != 'adm' :
        return HttpResponse("You are NOT allowed to access this section.")

    else :
        books = BookRequest.objects.all().filter(state='ready')
        return render(request, 'library/book_staff.html', {'books':books})


def book_staff_accept(request, book) :
    book_request = BookRequest.objects.get(name=book)
    name = book_request.name
    author = book_request.author
    genre = book_request.genre
    book_request.state = 'accept'
    book_request.save()

    # Save Book
    # 중복 책 경우 제외... 나중에 구현
    lastest_code = key = Book.objects.latest('code').code
    new_code = 'A' + str(int(lastest_code[1:]) + 1)

    Book.objects.create(code=new_code, name=name, author=author, genre=genre, lname=Library.objects.get(name='Cultural'))

    return render(request, 'library/complete.html', {'title':'REQUEST ACCEPTED', 'content':'Book request processed successfully'})

def book_staff_decline(request, book) :
    book_request = BookRequest.objects.filter(name=book)
    book_request.delete()

    return render(request, 'library/complete.html', {'title':'REQUEST REJECTED', 'content':'Book request processed successfully'})



def seminar_staff(request) :
    id = request.session['user_id']
    staff = Staff.objects.get(sid=id)
    if staff.s_type != 'room_adm' and staff.s_type != 'adm' :
        return HttpResponse("You are NOT allowed to access this section.")
    else :
        seminars = SeminarUse.objects.all().filter(state='ready')
        return render(request, 'library/seminar_staff.html', {'seminars':seminars})


def seminar_staff_accept(request, client, seminar) :
    seminar_use = SeminarUse.objects.filter(cid=client, rname=seminar).update(state='accept')
    #seminar_use.state = 'accept'
    #seminar_use.save()
    #print('direct to new page')
    return render(request, 'library/complete.html', {'title':'REQUEST ACCEPTED', 'content':'Process Complete.'})

def seminar_staff_decline(request, client, seminar) :
    seminar_use = SeminarUse.objects.filter(cid=client, rname=seminar).update(state='reject')
    #seminar_use.state = 'reject'
    #seminar_use.save()
    return render(request, 'library/complete.html', {'title':'REQUEST REJECTED', 'content':'Processc Complete.'})
