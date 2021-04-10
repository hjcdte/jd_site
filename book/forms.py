from django.db.models.query_utils import refs_expression
from django.forms import Form
from django.forms import fields
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Customer, Room, Room_Date, Room_Type
from django.contrib.auth.hashers import check_password


class AddRoomForm(Form):
    owner_id = fields.IntegerField(
        required=True,
    )

    room_num = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "必填",
            "invalid" : "无效",
        }
    )

    room_type_id =fields.IntegerField(
        required=True,
    )

    def clean(self):

        if  Room_Type.objects\
                .filter(owner=self.cleaned_data.get("owner_id"))\
                .filter(id=self.cleaned_data.get("room_type_id")).exists() == False:
            
            msg = "无此房间类型"
            self.add_error("room_type_id", msg)

        if  Room.objects\
                .filter(owner=self.cleaned_data.get("owner_id"))\
                .filter(room_num=self.cleaned_data.get("room_num")).exists() == True:
            
            msg = "已存在"
            self.add_error("room_num", msg)

        return self.cleaned_data


class DeleteRoomForm(Form):
    owner_id = fields.IntegerField(
        required=True,
    )

    id = fields.IntegerField(
        required=True,
    )

    def clean(self):

        if  Room.objects\
                .filter(owner=self.cleaned_data.get("owner_id"))\
                .filter(id=self.cleaned_data.get("id")).exists() == False:
            
            msg = "无此房间"
            self.add_error("id", msg)

        return self.cleaned_data


class AddRoomTypeForm(Form):
    owner_id = fields.IntegerField(
        required=True,
    )

    price = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "必填",
            "invalid" : "无效",
        }
    )

    room_type = fields.CharField(
        required=True,
        error_messages={
            "required" : "必填",
        }
    )

    def clean(self):
        if  Room_Type.objects\
                .filter(owner=self.cleaned_data.get("owner_id"))\
                .filter(room_type=self.cleaned_data.get("room_type")).exists() == True:
            
            msg = "已有此类型"
            self.add_error("room_type", msg)

        return self.cleaned_data


class UpdateRoomTypeForm(Form):
    owner_id = fields.IntegerField(
        required=True,
    )

    id = fields.IntegerField(
        required=True,
    )

    newprice = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "必填",
            "invalid" : "无效",
        }
    )

    def clean(self):
        if  Room_Type.objects\
                .filter(owner=self.cleaned_data.get("owner_id"))\
                .filter(id=self.cleaned_data.get("id")).exists() == False:
            
            msg = "无此类型"
            self.add_error("id", msg)

        return self.cleaned_data


class DeleteRoomTypeForm(Form):
    owner_id = fields.IntegerField(
        required=True,
    )

    id = fields.IntegerField(
        required=True,
    )

    def clean(self):

        if  Room_Type.objects\
                .filter(owner=self.cleaned_data.get("owner_id"))\
                .filter(id=self.cleaned_data.get("id")).exists() == False:
            
            msg = "无此房间类型"
            self.add_error("id", msg)

        return self.cleaned_data


class NoneAddForm(Form):

    room_num = fields.IntegerField(
        required=True,
    )
    
    owner_id = fields.IntegerField(
        required=True,
    )

    customer1 = fields.CharField(
        required=True,
        error_messages={
            "required" : "必填",
        }
    )

    customer_id1 = fields.CharField(
        required=True,
        max_length=19,
        min_length=18,
        error_messages={
            "required" : "身份证不能为空",
            "invalid" : "请输入一个有效的身份证号码",
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })

    customer2 = fields.CharField(
        required=False,
    )

    customer_id2 = fields.CharField(
        required=False,
        max_length=19,
        min_length=18,
        error_messages={
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })

    customer3 = fields.CharField(
        required=False,
    )

    customer_id3 = fields.CharField(
        required=False,
        max_length=19,
        min_length=18,
        error_messages={
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })

    customer4 = fields.CharField(
        required=False,
    )

    customer_id4 = fields.CharField(
        required=False,
        max_length=19,
        min_length=18,
        error_messages={
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })

    customer5 = fields.CharField(
        required=False,
    )

    customer_id5 = fields.CharField(
        required=False,
        max_length=19,
        min_length=18,
        error_messages={
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })

    customer6 = fields.CharField(
        required=False,
    )

    customer_id6 = fields.CharField(
        required=False,
        max_length=19,
        min_length=18,
        error_messages={
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })

    tel = fields.CharField(
        required=True, 
        max_length=11,
        min_length=11,    
        error_messages={
            "required" : "电话号码不能为空",
            "invalid" : "请输入一个有效的电话号码",
            "max_length" : "请输入一个有效的电话号码",
            "min_length" : "请输入一个有效的电话号码",
        })     

    crash = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "非空",
            "invalid" : "无效",
        })

    deposit = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "非空",
            "invalid" : "无效",
        })

    live_day = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "非空",
            "invalid" : "无效",
        })

    def clean(self):

        if Room.objects\
                .filter(owner=self.cleaned_data.get("owner_id"))\
                .filter(room_num=self.cleaned_data.get("room_num")).exists() == False:
            msg = "不存在"
            self.add_error("owner_id", msg)
        try:
            int(self.cleaned_data.get("tel"))
        except:
            msg = "请输入一个有效的电话号码"
            self.add_error("tel", msg)

        for i in range(2,7):
            user = "customer" + str(i)
            card = "customer_id" + str(i)
            if(self.cleaned_data.get(user)):
                if(self.cleaned_data.get(card)):
                    pass
                else:    
                    msg = "身份证不能为空"
                    self.add_error(card, msg)

        for i in range(1,7):
            card = "customer_id" + str(i)
            if(self.cleaned_data.get(card)):
                try:
                    int(self.cleaned_data.get(card))
                except:
                    msg = "请输入一个有效的身份证号码"
                    self.add_error(card, msg)

        return self.cleaned_data


class NoneBookForm(Form):
    customer_book = fields.CharField(
        required=True,
        error_messages={
            "required" : "必填",
        }
    )

    tel = fields.CharField(
        required=True, 
        max_length=11,
        min_length=11,    
        error_messages={
            "required" : "电话号码不能为空",
            "invalid" : "请输入一个有效的电话号码",
            "max_length" : "请输入一个有效的电话号码",
            "min_length" : "请输入一个有效的电话号码",
        }
    )     

    crash = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "非空",
            "invalid" : "无效",
        }
    )

    book_day = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "非空",
            "invalid" : "无效",
        }
    )

    room_num = fields.IntegerField(
        required=True,
    )

    owner_id = fields.IntegerField(
        required=True,
    )

    def clean(self):
        if Room.objects\
                    .filter(owner=self.cleaned_data.get("owner_id"))\
                    .filter(room_num=self.cleaned_data.get("room_num")).exists() == False:
            msg = "不存在"
            self.add_error("owner_id", msg)
        try:
            int(self.cleaned_data.get("tel"))
        except:
            msg = "请输入一个有效的电话号码"
            self.add_error("tel", msg)

        return self.cleaned_data


class BookAddForm(Form):

    id = fields.IntegerField(
        required=True,
    )
    
    owner_id = fields.IntegerField(
        required=True,
    )

    book_customer1 = fields.CharField(
        required=True,
        error_messages={
            "required" : "必填",
        }
    )

    book_customer_id1 = fields.CharField(
        required=True,
        max_length=19,
        min_length=18,
        error_messages={
            "required" : "身份证不能为空",
            "invalid" : "请输入一个有效的身份证号码",
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })

    book_customer2 = fields.CharField(
        required=False,
    )

    book_customer_id2 = fields.CharField(
        required=False,
        max_length=19,
        min_length=18,
        error_messages={
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })

    book_customer3 = fields.CharField(
        required=False,
    )

    book_customer_id3 = fields.CharField(
        required=False,
        max_length=19,
        min_length=18,
        error_messages={
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })

    book_customer4 = fields.CharField(
        required=False,
    )

    book_customer_id4 = fields.CharField(
        required=False,
        max_length=19,
        min_length=18,
        error_messages={
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })

    book_customer5 = fields.CharField(
        required=False,
    )

    book_customer_id5 = fields.CharField(
        required=False,
        max_length=19,
        min_length=18,
        error_messages={
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })

    book_customer6 = fields.CharField(
        required=False,
    )

    book_customer_id6 = fields.CharField(
        required=False,
        max_length=19,
        min_length=18,
        error_messages={
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })

    book_tel = fields.CharField(
        required=True, 
        max_length=11,
        min_length=11,    
        error_messages={
            "required" : "电话号码不能为空",
            "invalid" : "请输入一个有效的电话号码",
            "max_length" : "请输入一个有效的电话号码",
            "min_length" : "请输入一个有效的电话号码",
        })     

    book_price = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "非空",
            "invalid" : "无效",
        })

    book_deposit = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "非空",
            "invalid" : "无效",
        })

    book_live_day = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "非空",
            "invalid" : "无效",
        })

    def clean(self):

        if Room_Date.objects\
                .filter(owner=self.cleaned_data.get("owner_id"))\
                .filter(id=self.cleaned_data.get("id")).exists() == False:
            msg = "不存在"
            self.add_error("owner_id", msg)
        try:
            int(self.cleaned_data.get("book_tel"))
        except:
            msg = "请输入一个有效的电话号码"
            self.add_error("book_tel", msg)

        for i in range(2,7):
            user = "book_customer" + str(i)
            card = "book_customer_id" + str(i)
            if(self.cleaned_data.get(user)):
                if(self.cleaned_data.get(card)):
                    pass
                else:    
                    msg = "身份证不能为空"
                    self.add_error(card, msg)

        for i in range(1,7):
            card = "book_customer_id" + str(i)
            if(self.cleaned_data.get(card)):
                try:
                    int(self.cleaned_data.get(card))
                except:
                    msg = "请输入一个有效的身份证号码"
                    self.add_error(card, msg)

        return self.cleaned_data

class LivePutForm(Form):
    id = fields.IntegerField(
        required=True,
    )
    
    owner_id = fields.IntegerField(
        required=True,
    )

    live_live_day = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "非空",
            "invalid" : "无效",
        }
    )

    live_price = fields.IntegerField(
        required=True,
        error_messages={
            "required" : "非空",
            "invalid" : "无效",
        }
    )

    def clean(self):

        if Room_Date.objects\
                .filter(owner=self.cleaned_data.get("owner_id"))\
                .filter(id=self.cleaned_data.get("id")).exists() == False:
            msg = "不存在"
            self.add_error("owner_id", msg)
        
        return self.cleaned_data
