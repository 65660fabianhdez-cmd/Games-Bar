from django.shortcuts import render
from django.http import HttpResponse
import csv
import io
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from Usuarios.views import role_required


@role_required(['analista_reportes'])
def reporte(request):
    formatos = ["PDF", "XLSX", "CSV"]

    if request.method == "POST":
        periodo_id = request.POST.get("periodo_id", "").strip()
        formato = request.POST.get("formato", "").upper()
        nombre_archivo = request.POST.get("nombre_archivo", "").strip() or "reporte_inventario"
        detalle_incidencia = request.POST.get("detalle_incidencia", "").strip()
        observaciones = request.POST.get("observaciones", "").strip()

        rows = [
            ["Producto", "Entradas", "Salidas", "Stock"],
            ["Cerveza", 120, 45, 75],
            ["Bebida Energizante", 80, 32, 48],
            ["Snacks", 54, 20, 34],
        ]

        if formato == "CSV":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}.csv"'
            writer = csv.writer(response)
            for row in rows:
                writer.writerow(row)
            return response

        if formato == "XLSX":
            output = io.BytesIO()
            wb = Workbook()
            ws = wb.active
            ws.title = "Reporte"
            for row in rows:
                ws.append(row)
            wb.save(output)
            output.seek(0)
            response = HttpResponse(
                output.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}.xlsx"'
            return response

        if formato == "PDF":
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(40, 750, "Reporte de Inventario")
            pdf.setFont("Helvetica", 11)
            pdf.drawString(40, 730, f"Período ID: {periodo_id or 'N/A'}")
            pdf.drawString(40, 712, f"Incidencias: {detalle_incidencia or 'Ninguna'}")
            pdf.drawString(40, 694, f"Observaciones: {observaciones or 'Ninguna'}")
            y = 660
            for row in rows:
                pdf.drawString(40, y, " | ".join(map(str, row)))
                y -= 18
                if y < 60:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 11)
                    y = 750
            pdf.save()
            buffer.seek(0)
            response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}.pdf"'
            return response

    return render(request, "reporte.html", {"formatos": formatos})