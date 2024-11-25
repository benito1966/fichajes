from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from base_de_datos import obtener_fichajes_filtrados


def generar_pdf(empleado_id=None, mes=None):
    fichajes = obtener_fichajes_filtrados(empleado_id, mes)
    ruta_pdf = "informe_fichajes.pdf"

    # Crear documento PDF
    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
    elementos = []

    # Título del informe
    titulo = "Informe de Fichajes"
    if empleado_id or mes:
        titulo += " - Filtros Aplicados"
    elementos.append(Table([[titulo]], colWidths=[500]))

    # Espacio debajo del título
    elementos.append(Table([[""]], colWidths=[500]))

    # Crear tabla de fichajes
    datos = [["ID", "Empleado", "Fecha y Hora", "Tipo"]]
    for fichaje in fichajes:
        id_fichaje, nombre, fecha_hora, tipo = fichaje
        datos.append([id_fichaje, nombre, fecha_hora, tipo])

    # Estilo de la tabla
    tabla = Table(datos, colWidths=[50, 150, 200, 100])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elementos.append(tabla)

    # Generar el PDF
    doc.build(elementos)
    return ruta_pdf

