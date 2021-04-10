from django.db.models import Q


def find_max_days(dates,owner,today):
    for i in range(len(dates)):
        max_days = owner.room_date_set\
                    .filter(Q(room=dates[i].get("room__id")) & Q(book_date__gt=today))\
                    .order_by("book_date").values("book_date")
        if max_days:
            max_days = max_days[0].get("book_date")
            max_day = str(max_days-today).split(" ")[0]
            dates[i]["max_day"] = max_day
        else:
            max_day = -1
            dates[i]["max_day"] = max_day

    return dates


def none_find_max_days(dates,owner,today):
    for i in range(len(dates)):
        max_days = owner.room_date_set\
                    .filter(Q(room__room_num=dates[i].get("room_num")) & Q(book_date__gt=today))\
                    .order_by("book_date").values("book_date")
        if max_days:
            max_days = max_days[0].get("book_date")
            max_day = str(max_days-today).split(" ")[0]
            dates[i]["max_day"] = max_day
        else:
            max_day = -1
            dates[i]["max_day"] = max_day

    return dates
