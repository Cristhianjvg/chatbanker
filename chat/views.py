from django.http import HttpResponse, JsonResponse
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
    if request.method == 'POST':
        # Obtener archivos PDF del formulario
        pdf_files = request.FILES.getlist('pdf_files')

        # Aquí puedes procesar los archivos según tus necesidades
        for pdf_file in pdf_files:
            # Procesar cada archivo, por ejemplo, guardarlo en el sistema de archivos
            st.file_uploader(
                "Upload document",
                type=["pdf"],
                key="file_uploader",
                on_change=read_and_save_file(),
                label_visibility="collapsed",
                accept_multiple_files=True,
            )
            # o realizar alguna otra operación.

        # Devolver alguna respuesta JSON si es necesario
        return JsonResponse({'message': 'Archivos PDF recibidos correctamente.'})

    return render(request, "pdf.html")

def read_and_save_file():
    st.session_state["agent"].forget()  # to reset the knowledge base
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
            st.session_state["agent"].ingest(file_path)
        os.remove(file_path)

