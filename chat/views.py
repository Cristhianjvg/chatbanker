from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .chatbot import response

@csrf_exempt
def index(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        bot_response = response(user_message)  # Llama a tu función con el mensaje del usuario
        return HttpResponse(bot_response)
    else:
        return render(request, "home.html")


def pdf(request):
    return render(request, "pdf.html")
