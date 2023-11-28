from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .chatbot import response
from .pdf import pdf

from .pdf import convert_pdf_to_txt
from django.shortcuts import render, redirect
@csrf_exempt
def index(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        pdf_file = request.FILES.get('pdf-input', None)
        pdf(pdf_file, 'static/chatbot.txt') 
        bot_response = response(user_message)  # Llama a tu función con el mensaje del usuario

        return HttpResponse(bot_response)
    else:
        return render(request, "home.html")


def pdf(request):
    return render(request, "pdf.html")
