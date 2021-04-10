from django.forms import Form
from django.forms import fields
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Staff
from django.contrib.auth.hashers import check_password


class LoginForm(Form):
    username = fields.CharField(
        required=True,
        error_messages={
            "required" : "用户名不能为空",
        })
    password = fields.CharField(
        required=True,
        error_messages={
            "required" : "密码不能为空",
        })
    
    def clean(self):
        if User.objects.filter(username=self.cleaned_data.get("username")).exists() == False:
            msg = '用户名未注册'
            self.add_error('username', msg)
            return self.cleaned_data

        if authenticate(
            username=self.cleaned_data.get("username"),
            password=self.cleaned_data.get("password"),
        ) == None:
            msg = '密码错误'
            self.add_error('password', msg)
        
        return self.cleaned_data


class RegisterForm(Form):
    username = fields.CharField(
        required=True,
        error_messages={
            "required" : "用户名不能为空",
        })
    password1 = fields.CharField(
        required=True,
        min_length=8,
        error_messages={
            "required" : "密码不能为空",
            "min_length" : "密码不能少于8位",
        })
    password2 = fields.CharField(
        required=True, 
        min_length=8,
        error_messages={
            "required" : "密码不能为空",
            "min_length" : "密码不能少于8位",
        })
    email = fields.EmailField(
        required=True,
        error_messages={
            "required" : "邮箱不能为空",
            "invalid" : "请输入一个有效的邮箱地址",
        })

    def clean(self):
        if User.objects.filter(username=self.cleaned_data.get("username")):
            msg = '用户名已被注册'
            self.add_error('username', msg)

        if self.cleaned_data.get("password2") != self.cleaned_data.get("password1"):
            msg = '两次密码不一致！'
            self.add_error('password2', msg)
            # raise ValidationError('两次密码不一致！')
        
        if User.objects.filter(email=self.cleaned_data.get("email")):
            msg = '邮箱已被注册'
            self.add_error('email', msg)
        
        return self.cleaned_data


class LoginStaffForm(Form):
    username = fields.CharField(
        required=True,
        error_messages={
            "required" : "员工不能为空",
        })
    password = fields.CharField(
        required=True,
        error_messages={
            "required" : "密码不能为空",
        })
    
    def clean(self):
        if Staff.objects.filter(username=self.cleaned_data.get("username")).exists() == False:
            msg = '员工未注册'
            self.add_error('username', msg)
            return self.cleaned_data
        
        print(self.cleaned_data.get("password"))
        print(Staff.objects.filter(username=self.cleaned_data.get("username")).values("password")[0]["password"])
        print(check_password(
            self.cleaned_data.get("password"), 
            Staff.objects.filter(username=self.cleaned_data.get("username")).values("password")[0]["password"]
        ))
        if check_password(
            self.cleaned_data.get("password"), 
            Staff.objects.filter(username=self.cleaned_data.get("username")).values("password")[0]["password"]
        ) == False :
            msg = '密码错误'
            self.add_error('password', msg)
        
        return self.cleaned_data


class RegisterStaffForm(Form):
    username = fields.CharField(
        required=True,
        error_messages={
            "required" : "用户名不能为空",
        })
    password1 = fields.CharField(
        required=True,
        min_length=8,
        error_messages={
            "required" : "密码不能为空",
            "min_length" : "密码不能少于8位",
        })
    password2 = fields.CharField(
        required=True, 
        min_length=8,
        error_messages={
            "required" : "密码不能为空",
            "min_length" : "密码不能少于8位",
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
    id_card = fields.CharField(
        required=True,
        max_length=19,
        min_length=18,
        error_messages={
            "required" : "身份证不能为空",
            "invalid" : "请输入一个有效的身份证号码",
            "max_length" : "请输入一个有效的身份证号码",
            "min_length" : "请输入一个有效的身份证号码",
        })
    ownerid = fields.IntegerField(
        required=True,
    )


    def clean(self):

        if self.cleaned_data.get("password2") != self.cleaned_data.get("password1"):
            msg = '两次密码不一致！'
            self.add_error('password2', msg)
        
        try:
            int(self.cleaned_data.get("tel"))
        except:
            msg = "请输入一个有效的电话号码"
            self.add_error("tel", msg)
        
        try:
            int(self.cleaned_data.get("id_card"))
        except:
            msg = "请输入一个有效的身份证号码"
            self.add_error("id_card", msg)
            return self.cleaned_data

        if Staff.objects\
                .filter(owner=self.cleaned_data.get("ownerid"))\
                .filter(id_card=self.cleaned_data.get("id_card")).exists():
                
            msg = "身份证号码已存在"
            self.add_error("id_card", msg)

        return self.cleaned_data

class UpdateStaffForm(Form):
    newpassword = fields.CharField(
        required=True,
        min_length=8,
        error_messages={
            "required" : "新密码不能为空",
            "min_length" : "新密码不能少于8位",
        })
    id = fields.CharField(
        required=True,
    )

    ownerid = fields.IntegerField(
        required=True,
    )

    def clean(self):

        try:
            staff_id = int(self.cleaned_data.get("id"))
        except:
            return self.cleaned_data
        
        if Staff.objects\
                .filter(owner=self.cleaned_data.get("ownerid"))\
                .filter(id=staff_id).exists() == False:
            
            msg = "无此用户"
            self.add_error("id", msg)
        
            
        return self.cleaned_data


class DeleteStaffForm(Form):
    id = fields.CharField(
        required=True,
    )
    ownerid = fields.IntegerField(
        required=True,
    )

    def clean(self):

        try:
            staff_id = int(self.cleaned_data.get("id"))
        except:
            return self.cleaned_data

        if Staff.objects\
                .filter(owner=self.cleaned_data.get("ownerid"))\
                .filter(id=staff_id).exists() == False:
            
            msg = "无此用户"
            self.add_error("id", msg)

        return self.cleaned_data