import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors

# Função para gerar a carteirinha
def gerar_pdf_carteirinha(aluno):

    # Criar um buffer na memória para o PDF
    buffer = io.BytesIO()

    # Definir o tamanho da carteirinha (ID-1 standard: 85.6mm x 54mm)
    largura, altura = 85.6 * mm, 54 * mm
    c = canvas.Canvas(buffer, pagesize=(largura, altura))

    # --- FRENTE DA CARTEIRINHA ---
    # Fundo e Cabeçalho colorido
    c.setFillColor(colors.HexColor("#1A5276"))
    c.rect(0, altura - 15*mm, largura, 15*mm, stroke=0, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(largura/2, altura - 10*mm, aluno['instituicao'].upper())

    # Moldura para Foto (Lado Esquerdo)
    c.setStrokeColor(colors.lightgrey)
    c.setFillColor(colors.whitesmoke)
    c.rect(5*mm, altura - 45*mm, 25*mm, 28*mm, stroke=1, fill=1)
    c.setFillColor(colors.grey)
    c.setFont("Helvetica", 6)
    c.drawCentredString(17.5*mm, altura - 32*mm, "FOTO 3X4")

    # Informações (Lado Direito)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 7)
    c.drawString(35*mm, altura - 23*mm, f"NOME: {aluno['nome_completo'].upper()}")
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.black)
    c.drawString(35*mm, altura - 27*mm, f"MATRICULA: {aluno['matricula']}")
    c.drawString(35*mm, altura - 31*mm, f"SERIE/TURMA: {aluno['serie']} - {aluno['turma']}")
    
    # Convertendo o modelo da data para DD-MM-YYYY
    data_nasc = aluno['data_nascimento']
    if hasattr(data_nasc, 'strftime'):
        data_br = data_nasc.strftime('%d/%m/%Y')
    else:
        from datetime import datetime
        try:
            data_br = datetime.strptime(str(data_nasc), '%Y-%m-%d').strftime('%d/%m/%Y')
        except:
            data_br = str(data_nasc)
    
    c.drawString(35*mm, altura - 35*mm, f"NASCIMENTO: {data_br}")

    # Rodapé da Frente
    c.setFillColor(colors.HexColor("#1A5276"))
    c.rect(0, 0, largura, 4*mm, stroke=0, fill=1)

    c.showPage() # --- Finaliza a frente e começa o verso ---
    
    # --- VERSO DA CARTEIRINHA ---
    # Moldura geral do verso
    c.setStrokeColor(colors.HexColor("#1A5276"))
    c.rect(2*mm, 2*mm, largura-4*mm, altura-4*mm, stroke=1, fill=0)

    # Texto de Validação / Termos
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(largura/2, altura - 10*mm, "INFORMACOES IMPORTANTES")

    c.setFont("Helvetica", 6)
    texto_verso = [
        "1. Esta carteira e pessoal e intrasferivel.",
        "2. Em caso de perda, informar a secretaria imediatamente.",
        "3. O uso indevido esta sujeito as normas do regimentos escolar.",
        "4. Valida em todo o territorio nascional conforme legislacao vigente."
    ]
    y_text = altura - 15*mm
    for linha in texto_verso:
        c.drawString(5*mm, y_text, linha)
        y_text -= 4*mm
    
    # Simulação de QR CODE (Espaço para validação digital)
    c.setStrokeColor(colors.black)
    c.rect(largura - 20*mm, 5*mm, 15*mm, 15*mm, stroke=1)
    c.setFont("Helvetica", 5)
    c.drawCentredString(largura - 12.5*mm, 3*mm, "VALIDACAO DIGITAL")

    # Linha para assinatura
    c.setStrokeColor(colors.black)
    c.line(10*mm, 10*mm, 50*mm, 10*mm)
    c.drawCentredString(largura - 55*mm, 7*mm, "ASSINATURA DA DIRECAO")

    c.save()

    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf",
                             headers={"Content-Disposition": f"attachment; filename=carteirinha_{aluno['matricula']}.pdf"})