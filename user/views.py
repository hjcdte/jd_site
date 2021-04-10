from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm, LoginStaffForm , RegisterStaffForm, UpdateStaffForm, DeleteStaffForm
from utils.send import send_content
from utils.token_jwt import create_jwttoken
from .models import Staff
from .serializers import StaffSerializer


class login(APIView):

    # authentication_classes = [JwtAuthentication, ]
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        try:
            request.POST['first_name']
        except:
            obj = LoginStaffForm(request.POST)
            is_manager = False
        else:
            obj = LoginForm(request.POST)
            is_manager = True
        data = dict()
        error = dict()

        if(obj.is_valid()):

            if(is_manager):
                user = User.objects.\
                        filter(username=obj.cleaned_data["username"]).\
                        values("id", "username", "first_name")
            else:
                user = Staff.objects.\
                        filter(username=obj.cleaned_data["username"]).\
                        values("id", "username", "first_name")

            token = create_jwttoken({'id': user[0]['id'], 
                                        'username': user[0]['username'],
                                        'first_name': user[0]['first_name'],
                                        })
                                        
            data["code"] = 200
            data["token"] = token
            
        else:
            error_lsit = ['username', 'password']
            
            for i in error_lsit:
                try:
                    error[i] = obj.errors[i][0]
                except:
                    pass
            data["code"] = 404
            data["error"] = error

        content = send_content(data)
        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})


def register(request):

    obj = RegisterForm(request.POST)

    data = dict()
    error = dict()

    if(obj.is_valid()):
    
        User.objects.create_user(
            username=obj.cleaned_data["username"],
            password=obj.cleaned_data["password1"],
            email=obj.cleaned_data["email"],
            first_name="1",
            )

        data["code"] = 200
    else:
        error_lsit = ['username', 'password1', 'password2', 'email']
        
        for i in error_lsit:
            try:
                error[i] = obj.errors[i][0]
            except:
                pass
        data["code"] = 404
        data["error"] = error

    content = send_content(data)
    return JsonResponse(content,json_dumps_params={'ensure_ascii':False})


class staff(APIView):

    def post(self, request, *args, **kwargs):
        
        data = dict()
        error = dict()
        post = dict()

        if(request.user["auth"]=="0"):
            error_lsit = ['username', 'password1', 'password2', 'tel', 'id_card']
            
            for i in error_lsit:
                try:
                    error[i] = "没有权限！"
                except:
                    pass
            data["code"] = 404
            data["error"] = error
        else:
            post['username'] = request.POST['username']
            post['password1'] = request.POST['password1']
            post['password2'] = request.POST['password2']
            post['tel'] = request.POST['tel']
            post['id_card'] = request.POST['id_card']

            post.update({"ownerid":request.auth})
            obj = RegisterStaffForm(post)
            if(obj.is_valid()):

                user = User.objects.only('pk').get(pk=request.auth)
                Staff.objects.create(
                owner=user,
                username=obj.cleaned_data["username"],
                password=obj.cleaned_data["password1"],
                tel=obj.cleaned_data["tel"],
                id_card=obj.cleaned_data["id_card"],
                first_name="0",
                )

                data["code"] = 200
            else:
                error_lsit = ['username', 'password1', 'password2', 'tel', 'id_card']
                
                for i in error_lsit:
                    try:
                        error[i] = obj.errors[i][0]
                    except:
                        pass
                data["code"] = 404
                data["error"] = error

        content = send_content(data)
        
        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})
    
    def get(self, request, *args, **kwargs):
        data = dict()
        if(request.user["auth"]=="0"):
            data["code"] = 404
        else:
            user = Staff.objects.\
                    filter(owner=request.auth).\
                    values("id","username","id_card","tel")

            s = StaffSerializer(instance=user, many=True)
            
            data["staff"] = s.data
            data["code"] = 200
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
            post['newpassword'] = request.POST['newpassword']
            post['id'] = request.POST['id']
            post.update({"ownerid":request.auth})
            obj = UpdateStaffForm(post)

            if(obj.is_valid()):
                
                user = Staff.objects\
                        .filter(owner=obj.cleaned_data.get("ownerid"))\
                        .filter(id=obj.cleaned_data.get("id"))
                    # .update(password=obj.cleaned_data.get("newpassword"))\
                    # .save()
                user.update(password=obj.cleaned_data.get("newpassword"))
                user[0].save()
                data["code"] = 200
            else:
                error_lsit = ['newpassword','id']
                
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
            post.update({"ownerid":request.auth})
            obj = DeleteStaffForm(post)

            if(obj.is_valid()):

                user = Staff.objects\
                        .filter(owner=request.auth)\
                        .filter(id=obj.cleaned_data.get("id"))
                user[0].delete()
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


class jwt(APIView):
    
    def get(self, request, *args, **kwargs):
        data = dict()
        if(request.auth=="-1"):
            data["username"] = "未登录"
        else:
            data.update(request.user)
        data["id"] = request.auth
        content = send_content(data)

        return JsonResponse(content,json_dumps_params={'ensure_ascii':False})