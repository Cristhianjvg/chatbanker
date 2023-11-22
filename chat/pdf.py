from pdfminer.high_level import extract_text

def convert_pdf_to_txt(ruta_del_archivo, ruta_del_txt):
    # Extrae el texto del PDF
    texto = extract_text(ruta_del_archivo)
    
    # Abre el archivo txt en modo escritura y guarda el texto
    with open(ruta_del_txt, 'w', encoding='utf-8') as archivo_txt:
        archivo_txt.write(texto)


# Uso de la función
ruta_del_archivo = 'crucero.pdf'  # Reemplaza esto con la ruta a tu archivo PDF
ruta_del_txt = 'chatbot.txt'  # Reemplaza esto con la ruta a tu archivo txt
convert_pdf_to_txt(ruta_del_archivo, ruta_del_txt)
