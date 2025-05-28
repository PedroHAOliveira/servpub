import flet as ft
import json
import os
import re
from datetime import datetime
from fpdf import FPDF
import xlwt
import xlrd

DADOS_PATH = "dados.json"
EXCEL_PATH = "atendimentos.xls"
PROTOCOLO_PATH = "protocolo.txt"


# CPF

def validar_cpf(cpf):
    cpf = re.sub(r"[^0-9]", "", cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True


def gerar_protocolo():
    # Lê o último número salvo ou começa do 1
    if os.path.exists(PROTOCOLO_PATH):
        with open(PROTOCOLO_PATH, "r") as f:
            ultimo = int(f.read().strip() or "0")
    else:
        ultimo = 0

    novo_protocolo = ultimo + 1

    # Salva o novo número
    with open(PROTOCOLO_PATH, "w") as f:
        f.write(str(novo_protocolo))

    return novo_protocolo


# JSON

def carregar_dados():
    if os.path.exists(DADOS_PATH):
        try:
            with open(DADOS_PATH, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                return json.loads(conteudo) if conteudo else {}
        except Exception as e:
            print(f"Erro ao carregar JSON: {e}")
            return {}
    return {}


def salvar_dados(dados):
    with open(DADOS_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


# PDF
class PDF(FPDF):
    def __init__(self, protocolo_num):
        super().__init__()
        self.protocolo_num = protocolo_num

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'SOLICITAÇÃO DE SERVIÇO DE VACOL - Protocolo nº {self.protocolo_num}', ln=1, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-25)
        self.set_font('Arial', '', 9)
        self.multi_cell(0, 5, "Travessa João José de Andrade, s/n - Prainha - Arraial do Cabo - "
                              "RJ\nEmail: servpublico@arraial.rj.gov.br", align='C')


def gerar_pdf(info):
    protocolo = gerar_protocolo()
    pdf = PDF(protocolo)
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    hoje = datetime.now().strftime("%d/%m/%y")
    pdf.cell(0, 10, f"Serviço Solicitado em {hoje}", ln=1)
    pdf.ln(5)

    pdf.cell(0, 10, f"CPF: {info.get('CPF', '')}", ln=1)
    pdf.cell(0, 10, f"Nome: {info.get('Nome', '')}", ln=1)
    pdf.cell(0, 10, f"Tel/Cel: {info.get('Telefone', '')}", ln=1)
    pdf.cell(0, 10, f"Bairro: {info.get('Bairro', '')}", ln=1)
    pdf.cell(0, 10, f"Endereço: {info.get('Endereço', '')}       Nº: {info.get('Número', '')}", ln=1)
    pdf.cell(0, 10, f"QD: {info.get('Quadra', '')}      LT: {info.get('Lote', '')}", ln=1)
    pdf.multi_cell(0, 10, f"Referência: {info.get('Referência', '')}", ln=1)
    pdf.cell(0, 10, f"OBS/ Nº FOSSAS: {info.get('Número de Fossas', '')}", ln=1)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, """""", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 10, f"Chegada: ____:____   Saída: ____:____   (Concluída: ____/____/2025)", ln=1)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, "Dados da Empresa", ln=1)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 10, "Placa:_____________   Motorista:_____________________   Ajudante:_________________", ln=1)

    pdf.ln(8)
    pdf.multi_cell(0, 10, "Observação:" + "_" * 65, ln=1)
    pdf.cell(0, 10, "_" * 75, ln=1)
    pdf.cell(0, 10, "_" * 75, ln=1)

    pdf.ln(10)
    pdf.cell(0, 10, "Atesto a conclusão do serviço:", ln=1, align="C")
    pdf.ln(12)
    pdf.cell(0, 10, "___________________________________", ln=1, align="C")
    pdf.cell(0, 10, "Solicitante", ln=1, align="C")

    nome_arquivo = f"OrdemServico_{info['CPF'].replace('.', '').replace('-', '')}_P{protocolo}.pdf"
    pdf.output(nome_arquivo)
    return nome_arquivo


# INTERFACE

if __name__ == "__main__":
    from interface import main
    ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
