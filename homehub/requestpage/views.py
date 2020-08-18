from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .models import *
from .forms import CreateUserForm, RequestForm

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import RequestSerializer
from .models import Request
from rest_framework.decorators import action
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'requestpage/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'requestpage/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

class RequestpageList(APIView):
    def get(self, request, format=None):
        renderer_classes = [TemplateHTMLRenderer]
        queryset = Request.objects.all()
        return render(request, template_name = 'requestpage/requestlist.html',context={'requests': queryset})

    def post(self, request, format=None):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('/')
        context = {}
        context['form'] = RequestForm()
        context['errors'] = serializer.errors
        context['Invalid_mobile_number_format'] = "Invalid Mobile Number! Please Try With '+917013*****' this format"
        return render(request,'requestpage/newrequest_page.html',context=context)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='login')
def Newrequestpage(request):
    context={}
    context['form'] = RequestForm()
    return render(request, template_name='requestpage/newrequest_page.html', context=context)


class RequestpageDetail(APIView):
    def get_object(self, pk):
        try:
            return Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RequestSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        req_obj = self.get_object(pk)
        serializer = RequestSerializer(req_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        request = self.get_object(pk)
        request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


