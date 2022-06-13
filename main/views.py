import json

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import TODO
from django.http import HttpResponseRedirect, JsonResponse
from datetime import datetime, date
from django.views.generic.detail import DetailView
from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import AllowAny,  IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer
from main.serializers import TODOSerializer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect


@csrf_exempt
def home2(request):
    todo_items_list = TODO.objects.all().order_by("-added_date")
    # return render(request, 'main/index.html', {"todo_items": todo_items_list})
    # return render(request, 'main/tester.html')
    # return render(request, 'main/index.html', {"todo_items": todo_items_list})
    if request.method == 'GET':
        todo_items_list = TODO.objects.all().order_by("-added_date")
        serializer = TODOSerializer(todo_items_list, many=True)
        # return Response(serializer.data)
        # return render(request, 'main/index.html', {"todo_items": todo_items_list})
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        serializer = TODOSerializer(data=data)
        if serializer.is_valid():
            # serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, safe=False, status=400)


def home(request):
    todo_items_list = TODO.objects.all().order_by("-added_date")
    return render(request, 'main/index.html', {"todo_items": todo_items_list})

def api_completed_todo_detail(request, todo_id):
    todo_items_list = TODO.objects.all().filter(is_done=True)
    todo_items_list = TODO.objects.get(id=todo_id)
    serializer = TODOSerializer(todo_items_list)
    return JsonResponse(serializer.data, safe=False)


def api_completed_todo(request):
    todo_items_list = TODO.objects.all().filter(is_done=True)
    serializer = TODOSerializer(todo_items_list, many=True)
    return JsonResponse(serializer.data, safe=False)



@csrf_exempt
def add_todo(request):
    print(request.POST)
    current_time = datetime.today()
    content = request.POST["content"]
    due_on2 = (timezone.now() + timezone.timedelta(days=365))
    due_on3 = date.today().strftime('%Y-%m-%d')
    owner2 = request.user
    created_object = TODO.objects.create(title=content, added_date=current_time, due_on=due_on2, owner=owner2)
    # lengthOfToDo = TODO.objects.all().count()
    return HttpResponseRedirect('/')

@csrf_exempt
def delete_todo(request):
    TODO.objects.all().delete()
    return HttpResponseRedirect('/')

@csrf_exempt
def delete_todoOne(request):
    a =  TODO.objects.all()
    for i in a:
        if i.is_done:
            i.delete()

    return HttpResponseRedirect('/')

def completed_todo(request):
    a = TODO.objects.all()
    return render(request, 'main/completed_todo_list.html', {'done':a})

@csrf_exempt
def check(request, todo_id):
     a = TODO.objects.get(id = todo_id)
     a.is_done = not a.is_done
     if a.is_done:
        a.color = "red"
        a.text_for_done_button = "Done"
     elif a.is_done==False:
         a.color = "blue"
         a.text_for_done_button = "Not done"


     TODO.save(self = a)
     return HttpResponseRedirect('/')

class TODODetail(DetailView):
    model = TODO
    context_object_name = 'task'
    template_name = 'main/task_detail.html'



@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        todo_items_list = TODO.objects.all()
        serializer = TODOSerializer(todo_items_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        serializer = TODOSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TODOListAPIView(APIView):

    def get(self, request):
        todos = TODO.objects.all()
        serializer = TODO(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TODO(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)
    def post(self, request):
        user = request.data.get('user', {})

        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Обратите внимание, что мы не вызываем метод save() сериализатора, как
        # делали это для регистрации. Дело в том, что в данном случае нам
        # нечего сохранять. Вместо этого, метод validate() делает все нужное.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# def home(request):
#     return render(request, 'main/index.html')

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # Здесь нечего валидировать или сохранять. Мы просто хотим, чтобы
        # сериализатор обрабатывал преобразования объекта User во что-то, что
        # можно привести к json и вернуть клиенту.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Паттерн сериализации, валидирования и сохранения - то, о чем говорили
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
