from typing import Counter
from rest_framework.settings import reload_api_settings
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import JsonResponse
from utils.send import send_content
from .models import Room_Type, Room ,Room_Date ,Customer, Booking_record ,Money
from .serializers import RoomTypeSerializer, RoomSerializer, RoomNoneSerializer, BookNoneSerializer, LiveNoneSerializer, CancelNoneSerializer, BookRecordSerializer, MoneyTableSerializer
from .forms import AddRoomForm, DeleteRoomForm, AddRoomTypeForm, UpdateRoomTypeForm, DeleteRoomTypeForm, NoneAddForm, NoneBookForm, BookAddForm, LivePutForm
from user.models import Staff
import datetime
from django.db.models import Q, F, Count, Sum
from utils.max_day import find_max_days, none_find_max_days
from utils.jd_date import jd_today
from functools import reduce

class index(APIView):
    
    def get(self, request, *args, **kwargs):
        data = dict()
        error = dict()

        # request.auth=="-1"
        # print(datetime.timedelta(days=1))
        # print(datetime.date.today()+datetime.timedelta(days=37))
        if(request.auth=="-1"):
            data["code"] = 404
            data["error"] = {"id":"没有登录"}
        else:
            # owner = Staff.objects.filter(id=13).values("owner")[0]["owner"]
            # owner = User.objects.get(id=owner)
            if(request.user["auth"]=="0"):
                owner = Staff.objects.filter(id=request.auth).values("owner")[0]["owner"]
                owner = User.objects.get(id=owner)
            else:
                owner = User.objects.get(id=request.auth)

            data["code"] = 200

            today = jd_today(request.query_params.get('top_date'))

            
            if(request.query_params.get('room_status')=="none"):
                filter_nums = dict()
                filter_nums_list = list()
                room_nums_list = list()

                dates_nums = owner.room_date_set\
                            .filter(
                                (Q(is_book=True) & Q(book_date=today))
                                | (Q(is_live=True) & Q(cancel_date__gt=today))
                                )\
                            .values("room__room_num","room__room_type__room_type","room__room_type__price")
                #是否预订 且 今日入住
                #不可能存在两份今日入住的同房间号的订单
                # is_live已入住 且 退房时间大于今天的
                #不可能存在两份
                cancel_nums = owner.room_date_set\
                            .filter((Q(is_live=True) & Q(cancel_date=today)))\
                            .values("room__room_num","room__room_type__room_type","room__room_type__price")
                #is_live已入住 且 退房时间等于今天的
                #不可能存在两份
                for i in owner.room_set.values("room_num","room_type__room_type","room_type__price"):
                    filter_nums["room_num"] = i["room_num"]
                    filter_nums["room_type"] = i["room_type__room_type"]
                    filter_nums["price"] = i["room_type__price"]
                    filter_nums['status'] = "空房"
                    room_nums_list.append(filter_nums)
                    filter_nums = dict()

                for i in dates_nums:
                    filter_nums["room_num"] = i["room__room_num"]
                    filter_nums["room_type"] = i["room__room_type__room_type"]
                    filter_nums["price"] = i["room__room_type__price"]
                    filter_nums['status'] = "空房"
                    if(filter_nums in room_nums_list):
                        room_nums_list.remove(filter_nums)
                    filter_nums = dict()
                
                for i in cancel_nums:
                    filter_nums["room_num"] = i["room__room_num"]
                    filter_nums["room_type"] = i["room__room_type__room_type"]
                    filter_nums["price"] = i["room__room_type__price"]
                    filter_nums['status'] = "空房"
                    if(filter_nums in room_nums_list):
                        a = room_nums_list.index(filter_nums)
                        room_nums_list[a]['status'] = "今日退房"
                    filter_nums = dict()

                # 入住时间小于今天 且 退房时间小于等于今天
                # 入住时间大于今天 且 退房时间大于今天)
                none_count = len(room_nums_list)

                dates = none_find_max_days(room_nums_list,owner,today)
                
                s = RoomNoneSerializer(instance=dates, many=True)
                
                data["none_room"] = s.data
                data["none_count"] = none_count
                data["room_count"] = Room.objects.filter(owner=owner).count()
            elif(request.query_params.get('room_status')=="book"):
                #是否预订 且 今日入住
                #不可能存在两份今日入住的同房间号的订单
                dates = owner.room_date_set\
                            .filter(Q(is_book=True) & Q(book_date=today))\
                            .values("room__id","id","room__room_num","room__room_type__room_type","name","tel","book_day","crash")
                
                book_count = len(dates)
                dates = find_max_days(dates,owner,today)
                s = BookNoneSerializer(instance=dates, many=True)
                
                data["book_room"] = s.data
                data["book_count"] = book_count
                data["room_count"] = Room.objects.filter(owner=owner).count()

            elif(request.query_params.get('room_status')=="live"):
                dates = owner.room_date_set\
                            .filter(Q(is_live=True) & Q(cancel_date__gt=today))\
                            .values("room__id","id","room__room_num","room__room_type__room_type","book_date","cancel_date","name","tel","deposit")
                # is_live已入住 且 退房时间大于今天的
                #不可能存在两份
                live_count = len(dates)
                dates = find_max_days(dates,owner,today)
                s = LiveNoneSerializer(instance=dates, many=True)
                
                data["live_room"] = s.data
                data["live_count"] = live_count
                data["room_count"] = Room.objects.filter(owner=owner).count()

            elif(request.query_params.get('room_status')=="cancel"):
                dates = owner.room_date_set\
                        .filter(Q(is_live=True) & Q(cancel_date=today))\
                        .values("room__id","id","room__room_num","room__room_type__room_type","name","tel","deposit")
                #is_live已入住 且 退房时间等于今天的
                #不可能存在两份
                cancel_count = len(dates)
                dates = find_max_days(dates,owner,today)
                s = CancelNoneSerializer(instance=dates, many=True)
                
                data["cancel_room"] = s.data
                data["cancel_count"] = cancel_count
                data["room_count"] = Room.objects.filter(owner=owner).count()

        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})

    def post(self, request, *args, **kwargs):
        data = dict()
        error = dict()
        post = dict()
        today = jd_today(request.query_params.get('top_date'))

        if(request.auth=="-1"):
            data["code"] = 404
            data["error"] = {"id":"没有登录"}
        else:
            if(request.user["auth"]=="0"):
                owner_id = Staff.objects.filter(id=request.auth).values("owner")[0]["owner"]
                owner = User.objects.get(id=owner_id)
            else:
                owner = User.objects.get(id=request.auth)
                owner_id = request.auth

            if(request.query_params.get('room_status')=="none"):
                today = datetime.date.today()
                post = request.POST.copy()
                post["owner_id"] = owner_id
                obj = NoneAddForm(post)

                if(obj.is_valid()):
                    
                    room_none = Room.objects.filter(Q(owner=owner) & Q(room_num=obj.cleaned_data.get('room_num')))[0]
                    Room_Date.objects\
                            .create(
                                owner = owner,
                                room = room_none,
                                book_date = today,
                                cancel_date = today + datetime.timedelta(days=obj.cleaned_data.get('live_day')),
                                is_live = True,
                                is_book = False,
                                name = obj.cleaned_data.get('customer1'),
                                tel = obj.cleaned_data.get('tel'),
                                crash = obj.cleaned_data.get('crash'),
                                deposit = obj.cleaned_data.get('deposit'),
                                )

                    for i in range(1,7):
                        cus = 'customer' + str(i)
                        cus_id = 'customer_id' + str(i)
                        if(obj.cleaned_data.get(cus)):
                            if(i==1):
                                customer = Customer.objects.create(
                                                owner = owner,
                                                name = obj.cleaned_data.get(cus),
                                                id_card = obj.cleaned_data.get(cus_id),
                                                tel = obj.cleaned_data.get("tel"),
                                            )
                            else:
                                customer = Customer.objects.create(
                                                owner = owner,
                                                name = obj.cleaned_data.get(cus),
                                                id_card = obj.cleaned_data.get(cus_id),
                                            )
                            Booking_record.objects.create(
                                owner = owner,
                                room = room_none,
                                customer = customer,
                                book_date = today,
                                cancel_date = today + datetime.timedelta(days=obj.cleaned_data.get('live_day')),
                                room_registrant = request.user["username"]
                            )

                    Money.objects.create(
                        owner = owner,
                        room = room_none,
                        book_date = today,
                        cancel_date = today + datetime.timedelta(days=obj.cleaned_data.get('live_day')),
                        crash = obj.cleaned_data.get('crash'),
                    )
                    data["code"] = 200
                else:
                    error_lsit = ['customer1','customer2', 'customer_id1', 'customer_id2', 'tel', 'crash', 'deposit', 'live_day', 'customer3', 'customer4', 'customer5', 'customer6', 'customer_id3', 'customer_id4', 'customer_id5', 'customer_id6', 'owner_id']
                    
                    for i in error_lsit:
                        try:
                            error[i] = obj.errors[i][0]
                        except:
                            pass
                    data["code"] = 404
                    data["error"] = error
            elif(request.query_params.get('room_status')=="book"):
                post = request.POST.copy()
                post["owner_id"] = owner_id
                obj = NoneBookForm(post)

                if(obj.is_valid()):
                    room_none = Room.objects.filter(Q(owner=owner) & Q(room_num=obj.cleaned_data.get('room_num')))[0]
                    Room_Date.objects\
                            .create(
                                owner = owner,
                                room = room_none,
                                book_date = today,
                                cancel_date = today + datetime.timedelta(days=obj.cleaned_data.get('book_day')),
                                is_live = False,
                                is_book = True,
                                name = obj.cleaned_data.get('customer_book'),
                                tel = obj.cleaned_data.get('tel'),
                                crash = obj.cleaned_data.get('crash'),
                                book_day = obj.cleaned_data.get('book_day'),
                                )
                    data["code"] = 200
                
                else:
                    error_lsit = ['customer_book', 'tel', 'crash', 'book_day', 'owner_id']
                    
                    for i in error_lsit:
                        try:
                            error[i] = obj.errors[i][0]
                        except:
                            pass
                    data["code"] = 404
                    data["error"] = error
        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})

    def put(self, request, *args, **kwargs):
        data = dict()
        error = dict()
        post = dict()
        today = jd_today(request.query_params.get('top_date'))

        if(request.auth=="-1"):
            data["code"] = 404
            data["error"] = {"id":"没有登录"}
        else:
            if(request.user["auth"]=="0"):
                owner_id = Staff.objects.filter(id=request.auth).values("owner")[0]["owner"]
                owner = User.objects.get(id=owner_id)
            else:
                owner = User.objects.get(id=request.auth)
                owner_id = request.auth
            
            if(request.query_params.get('room_status')=="book"):
                today = datetime.date.today()
                post = request.POST.copy()
                post["owner_id"] = owner_id
                obj = BookAddForm(post)
                if(obj.is_valid()):
                    room_date = Room_Date.objects\
                                .filter(id=obj.cleaned_data.get('id'))
                    room_date.update(
                                    book_date = today,
                                    cancel_date = today + datetime.timedelta(days=obj.cleaned_data.get('book_live_day')),
                                    is_live = True,
                                    is_book = False,
                                    name = obj.cleaned_data.get('book_customer1'),
                                    tel = obj.cleaned_data.get('book_tel'),
                                    crash = obj.cleaned_data.get('book_price'),
                                    deposit = obj.cleaned_data.get('book_deposit'),
                                )
                    room_date[0].save()

                    for i in range(1,7):
                        cus = 'book_customer' + str(i)
                        cus_id = 'book_customer_id' + str(i)
                        if(obj.cleaned_data.get(cus)):
                            if(i==1):
                                customer = Customer.objects.create(
                                                owner = owner,
                                                name = obj.cleaned_data.get(cus),
                                                id_card = obj.cleaned_data.get(cus_id),
                                                tel = obj.cleaned_data.get("book_tel"),
                                            )
                            else:
                                customer = Customer.objects.create(
                                                owner = owner,
                                                name = obj.cleaned_data.get(cus),
                                                id_card = obj.cleaned_data.get(cus_id),
                                            )
                            Booking_record.objects.create(
                                owner = owner,
                                room = room_date[0].room,
                                customer = customer,
                                book_date = today,
                                cancel_date = today + datetime.timedelta(days=obj.cleaned_data.get('book_live_day')),
                                room_registrant = request.user["username"]
                            )

                    Money.objects.create(
                        owner = owner,
                        room = room_date[0].room,
                        book_date = today,
                        cancel_date = today + datetime.timedelta(days=obj.cleaned_data.get('book_live_day')),
                        crash = obj.cleaned_data.get('book_price'),
                    )
                    data["code"] = 200

                else:
                    error_lsit = ['book_customer1','book_customer2', 'book_customer_id1', 'book_customer_id2', 'book_tel', 'book_price', 'book_deposit', 'book_live_day', 'book_customer3', 'book_customer4', 'book_customer5', 'book_customer6', 'book_customer_id3', 'book_customer_id4', 'book_customer_id5', 'book_customer_id6', 'owner_id']
                        
                    for i in error_lsit:
                        try:
                            error[i] = obj.errors[i][0]
                        except:
                            pass
                    data["code"] = 404
                    data["error"] = error
            elif(request.query_params.get('room_status')=="live"):
                today = datetime.date.today()
                post = request.POST.copy()
                post["owner_id"] = owner_id
                print(post)
                obj = LivePutForm(post)

                if(obj.is_valid()):
                    room_date = Room_Date.objects\
                                .filter(id=obj.cleaned_data.get('id'))
                    pre_registrant = Booking_record.objects.filter(
                                                Q(room=room_date[0].room_id)
                                                &Q(book_date=room_date[0].book_date)
                                                &Q(cancel_date=room_date[0].cancel_date)
                                            )[0].room_registrant
                    
                    Booking_record.objects\
                                    .filter(
                                            Q(room=room_date[0].room_id)
                                            &Q(book_date=room_date[0].book_date)
                                            &Q(cancel_date=room_date[0].cancel_date)
                                    ).update(
                        cancel_date = room_date[0].cancel_date + datetime.timedelta(days=obj.cleaned_data.get('live_live_day')),
                        room_registrant = pre_registrant + " " + request.user["username"]
                    )

                    pre_crash = Money.objects.filter(
                        Q(room=room_date[0].room_id)
                        &Q(book_date=room_date[0].book_date)
                        &Q(cancel_date=room_date[0].cancel_date)
                    )[0].crash

                    Money.objects.filter(
                            Q(room=room_date[0].room_id)
                            &Q(book_date=room_date[0].book_date)
                            &Q(cancel_date=room_date[0].cancel_date)
                            ).update(
                            cancel_date = room_date[0].cancel_date + datetime.timedelta(days=obj.cleaned_data.get('live_live_day')),
                            crash = pre_crash + obj.cleaned_data.get('live_price'),
                        )
                    

                    room_date.update(
                            cancel_date = room_date[0].cancel_date + datetime.timedelta(days=obj.cleaned_data.get('live_live_day')),
                            crash = pre_crash + obj.cleaned_data.get('live_price'),
                        )
                    data["code"] = 200

                else:
                    error_lsit = ['live_price', 'live_live_day', 'owner_id']
                        
                    for i in error_lsit:
                        try:
                            error[i] = obj.errors[i][0]
                        except:
                            pass
                    data["code"] = 404
                    data["error"] = error
        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})

    def delete(self, request, *args, **kwargs):
        data = dict()
        error = dict()
        post = dict()
        today = jd_today(request.query_params.get('top_date'))

        if(request.auth=="-1"):
            data["code"] = 404
            data["error"] = {"id":"没有登录"}
        else:
            if(request.user["auth"]=="0"):
                owner_id = Staff.objects.filter(id=request.auth).values("owner")[0]["owner"]
                owner = User.objects.get(id=owner_id)
            else:
                owner = User.objects.get(id=request.auth)
                owner_id = request.auth

            room_date = Room_Date.objects\
                                .filter(id=request.POST.get('id'))
            try:
                room_date[0].delete()
                data["code"] = 200
            except:
                data["error"] = {"id":"没有此房间"}
                data["code"] = 404

        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})

class room(APIView):

    def get(self, request, *args, **kwargs):
        data = dict()
        error = dict()
        post = dict()

        if(request.user["auth"]=="0"):
            if(request.user["auth"]=="0"):
                data["code"] = 404
                data["error"] = {"id":"没有权限"}
        else:
            rooms = Room.objects.filter(owner=request.auth).values("room_type__room_type","room_num","room_type__price","id")
            s = RoomSerializer(instance=rooms, many=True)
            data["room"] = s.data
            data["code"] = 200
        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})

    def post(self, request, *args, **kwargs):
        data = dict()
        error = dict()
        post = dict()

        if(request.user["auth"]=="0"):
            data["code"] = 404
            data["error"] = {"id":"没有权限"}
        else:
            post["room_num"] = request.POST.get("room_num")
            post["room_type_id"] = request.POST.get("room_type_id")
            post["owner_id"] = request.auth
            
            obj = AddRoomForm(post)
            if(obj.is_valid()):

                user = User.objects.only('pk').get(pk=request.auth)
                typer = Room_Type.objects.only('pk').get(pk=obj.cleaned_data["room_type_id"])
                
                rooms = Room.objects.create(
                    owner=user,
                    room_num=obj.cleaned_data["room_num"],
                    room_type=typer,
                )

                data["code"] = 200
            else:
                error_lsit = ['room_num', 'room_type_id',]
                
                for i in error_lsit:
                    try:
                        error[i] = obj.errors[i][0]
                    except:
                        pass
                data["code"] = 404
                data["error"] = error
            content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})
    
    def delete(self, request, *args, **kwargs):
        data = dict()
        error=dict()
        post = dict()

        if(request.user["auth"]=="0"):
            data["code"] = 404
            data["error"] = {"id":"没有权限"}
        else:
            post['id'] = request.POST['id']
            post['owner_id'] = request.auth
            
            obj = DeleteRoomForm(post)
            if(obj.is_valid()):

                rooms = Room.objects\
                            .filter(owner=obj.cleaned_data['owner_id'])\
                            .filter(id=obj.cleaned_data['id'])
                
                rooms[0].delete()

                data["code"] = 200
            else:
                error_lsit = ['id',]
                
                for i in error_lsit:
                    try:
                        error[i] = obj.errors[i][0]
                    except:
                        pass
                data["code"] = 404
                data["error"] = error
        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})

class room_type(APIView):

    def get(self, request, *args, **kwargs):
        data = dict()
        error = dict()
        post = dict()

        if(request.user["auth"]=="0"):
            data["code"] = 404
            data["error"] = {"id":"没有权限"}
        else:
            types = Room_Type.objects.filter(owner=request.auth).values("room_type","price","id")
            s = RoomTypeSerializer(instance=types, many=True)
            

            data["room_type"] = s.data
            data["code"] = 200
        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})

    def post(self, request, *args, **kwargs):
        data = dict()
        error=dict()
        post = dict()

        if(request.user["auth"]=="0"):
            data["code"] = 404
            data["error"] = {"id":"没有权限"}
        else:
            post["price"] = request.POST.get("price")
            post["room_type"] = request.POST.get("room_type")
            post["owner_id"] = request.auth
            obj = AddRoomTypeForm(post)
            if(obj.is_valid()):

                user = User.objects.only('pk').get(pk=request.auth)
                Room_Type.objects\
                        .create(
                            owner=user,
                            room_type=obj.cleaned_data["room_type"],
                            price=obj.cleaned_data["price"],
                        )
                data["code"] = 200
            else:
                error_lsit = ['price', 'room_type',]
                
                for i in error_lsit:
                    try:
                        error[i] = obj.errors[i][0]
                    except:
                        pass
                data["code"] = 404
                data["error"] = error
        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})

    def put(self, request, *args, **kwargs):
        data = dict()
        error=dict()
        post = dict()

        if(request.user["auth"]=="0"):
            data["code"] = 404
            data["error"] = {"id":"没有权限"}
        else:
            post["newprice"] = request.POST.get("newprice")
            post["id"] = request.POST.get("id")
            post["owner_id"] = request.auth

            obj = UpdateRoomTypeForm(post)
            if(obj.is_valid()):

                room_type = Room_Type.objects\
                                    .filter(owner=request.auth)\
                                    .filter(id=obj.cleaned_data.get("id"))
                room_type.update(price=obj.cleaned_data.get("newprice"))
                room_type[0].save()

                data["code"] = 200
            else:
                error_lsit = ['newprice', 'id',]
                
                for i in error_lsit:
                    try:
                        error[i] = obj.errors[i][0]
                    except:
                        pass
                data["code"] = 404
                data["error"] = error
        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})

    def delete(self, request, *args, **kwargs):
        data = dict()
        error=dict()
        post = dict()

        if(request.user["auth"]=="0"):
            data["code"] = 404
            data["error"] = {"id":"没有权限"}
        else:
            post["id"] = request.POST.get("id")
            post["owner_id"] = request.auth

            obj = DeleteRoomTypeForm(post)
            if(obj.is_valid()):

                room_type = Room_Type.objects\
                                    .filter(owner=obj.cleaned_data.get("owner_id"))\
                                    .filter(id=obj.cleaned_data.get("id"))    
                
                room_type[0].delete()

                data["code"] = 200
            else:
                error_lsit = ['id',]
                
                for i in error_lsit:
                    try:
                        error[i] = obj.errors[i][0]
                    except:
                        pass
                data["code"] = 404
                data["error"] = error

        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})

class booking_record(APIView):

    def get(self, request, *args, **kwargs):
        data = dict()

        if(request.user["auth"]=="0"):
            data["code"] = 404
            data["error"] = {"id":"没有权限"}
        else:
            
            record = Booking_record.objects\
                                    .filter(owner=request.auth)\
                                    .values("customer__name","room__room_num","book_date","cancel_date","room_registrant")
            s = BookRecordSerializer(instance=record, many=True)
            

            data["record"] = s.data
            data["code"] = 200
        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})

class money(APIView):

    def get(self, request, *args, **kwargs):
        data = dict()
        post1 = dict()
        post2 = dict()
        post3 = dict()


        if(request.user["auth"]=="0"):
            data["code"] = 404
            data["error"] = {"id":"没有权限"}
        else:
            now_year = str(datetime.date.today()).split('-')

            now_month = int(now_year[1])
            now_year = int(now_year[0])
            
            for i in range(1,13):
                if(i==12):
                    post1["去年%d月" % i] = Money.objects\
                                                .filter(owner=request.auth)\
                                                .filter((Q(book_date__gte=datetime.date(now_year-1,i,1))&Q(book_date__lt=datetime.date(now_year,1,1)))
                                                        )\
                                                .aggregate(all_money = Sum("crash"))
                    post2["今年%d月" % i] = Money.objects\
                                                .filter(owner=request.auth)\
                                                .filter((Q(book_date__gte=datetime.date(now_year,i,1))&Q(book_date__lt=datetime.date(now_year+1,1,1)))
                                                        )\
                                                .aggregate(all_money = Sum("crash"))
                else:
                    post1["去年%d月" % i] = Money.objects\
                                                .filter(owner=request.auth)\
                                                .filter((Q(book_date__gte=datetime.date(now_year-1,i,1))&Q(book_date__lt=datetime.date(now_year-1,i+1,1)))
                                                        )\
                                                .aggregate(all_money = Sum("crash"))
                    post2["今年%d月" % i] = Money.objects\
                                                .filter(owner=request.auth)\
                                                .filter((Q(book_date__gte=datetime.date(now_year,i,1))&Q(book_date__lt=datetime.date(now_year,i+1,1)))
                                                        )\
                                                .aggregate(all_money = Sum("crash"))
            
            data["去年营收"] = Money.objects.filter(owner=request.auth).filter(Q(book_date__gte=datetime.date(now_year-1,1,1))&Q(book_date__lt=datetime.date(now_year,1,1))).aggregate(all_money = Sum("crash"))
            data["今年营收"] = Money.objects.filter(owner=request.auth).filter(Q(book_date__gte=datetime.date(now_year,1,1))&Q(book_date__lt=datetime.date(now_year+1,1,1))).aggregate(all_money = Sum("crash"))
            # s = BookRecordSerializer(instance=record, many=True)
            data["yesterday"] = Money.objects.filter(owner=request.auth).filter(book_date=datetime.date.today() - datetime.timedelta(days=1)).aggregate(all_money = Sum("crash"))
            data["last_yesterday"] = Money.objects.filter(owner=request.auth).filter(book_date=datetime.date.today() - datetime.timedelta(days=366)).aggregate(all_money = Sum("crash"))
            data["today"] = Money.objects.filter(owner=request.auth).filter(book_date=datetime.date.today()).aggregate(all_money = Sum("crash"))
            
            room_types = Room_Type.objects.filter(owner=request.auth).values("room_type")
            # data["record"] = s.data
            for i in room_types:
                post3[i['room_type']] = Money.objects\
                                            .filter(owner=request.auth)\
                                            .filter(room__room_type__room_type=i['room_type'])\
                                            .filter(Q(book_date__gte=datetime.date(now_year,3,1))&Q(book_date__lt=datetime.date(now_year,4,1) + datetime.timedelta(days=30)))\
                                            .aggregate(all_money = Sum("crash"))
            data["code"] = 200
            data["data1"] = post1
            data["data2"] = post2
            data["data3"] = post3

        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})
    
    def post(self, request, *args, **kwargs):
        data = dict()

        if(request.user["auth"]=="0"):
            data["code"] = 404
            data["error"] = {"id":"没有权限"}
        else:
            money_tables = Money.objects\
                                .filter(owner=request.auth)\
                                .values("room__room_num",'crash',"book_date","cancel_date")
            s = MoneyTableSerializer(instance=money_tables, many=True)
            

            data["money"] = s.data
            data["code"] = 200
        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})