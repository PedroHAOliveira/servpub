import flet as ft
from datetime import datetime
from main import validar_cpf, carregar_dados, salvar_dados, gerar_pdf, EXCEL_PATH, gerar_protocolo
import os
import xlwt


def main(page: ft.Page):
    page.title = "Atendimento"
    page.scroll = ft.ScrollMode.AUTO
    dados = carregar_dados()

    cpf_input = ft.TextField(label="CPF", width=300)
    resultado = ft.Text()
    container_detalhes = ft.Column()

    def atualizar_interface():
        page.update()

    def buscar_cpf(e):
        container_detalhes.controls.clear()
        cpf = cpf_input.value.strip()
        if not validar_cpf(cpf):
            resultado.value = "CPF inválido."
            atualizar_interface()
            return

        cpf = ''.join(filter(str.isdigit, cpf))
        if cpf in dados:
            info = dados[cpf]
            resultado.value = f"{info['Nome']} - {info['Endereço']}"
            mostrar_detalhes(info)
        else:
            resultado.value = "CPF não encontrado. Deseja cadastrar?"
            container_detalhes.controls.append(
                ft.ElevatedButton("Cadastrar novo", on_click=lambda e: exibir_formulario_novo(cpf))
            )
        atualizar_interface()

    def exibir_formulario_novo(cpf):
        campos = {}
        layout = []
        labels = ["Nome", "Telefone", "Bairro", "Endereço", "Número", "Quadra", "Lote", "Referência", "Número de Fossas"]
        for campo in labels:
            tf = ft.TextField(label=campo)
            campos[campo] = tf
            layout.append(tf)

        def salvar_novo(e):
            info = {"CPF": cpf}
            for campo in labels:
                info[campo] = campos[campo].value
            info["Data Início"] = ""
            info["Data Fim"] = ""
            dados[cpf] = info
            salvar_dados(dados)
            page.dialog.open = False
            resultado.value = "Cadastro realizado."
            mostrar_detalhes(info)
            atualizar_interface()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Novo Cadastro"),
            content=ft.Column(layout),
            actions=[
                ft.TextButton("Salvar", on_click=salvar_novo),
                ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo())
            ]
        )
        page.dialog.open = True
        atualizar_interface()

    def mostrar_detalhes(info):
        container_detalhes.controls.clear()
        container_detalhes.controls.extend([
            ft.Text(f"Nome: {info['Nome']}"),
            ft.Text(f"Endereço: {info['Endereço']} Nº: {info.get('Número', '')}"),
            ft.Text(f"Bairro: {info['Bairro']} - Tel: {info['Telefone']}"),
            ft.ElevatedButton("Visualizar PDF", on_click=lambda e: os.startfile(gerar_pdf(info))),
            ft.ElevatedButton("Editar Cadastro", on_click=lambda e: editar_dados(info)),

        ])

    def editar_dados(info):
        campos = {}
        layout = []
        for campo in ["Nome", "Telefone", "Bairro", "Endereço", "Número", "Quadra", "Lote", "Referência", "Número de Fossas"]:
            tf = ft.TextField(label=campo, value=info.get(campo, ""))
            campos[campo] = tf
            layout.append(tf)

        def salvar_edicao(e):
            for campo in campos:
                info[campo] = campos[campo].value
            salvar_dados(dados)
            page.dialog.open = False
            resultado.value = "Cadastro atualizado."
            mostrar_detalhes(info)
            atualizar_interface()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Editar Cadastro"),
            content=ft.Column(layout),
            actions=[
                ft.TextButton("Salvar", on_click=salvar_edicao),
                ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo())
            ]
        )
        page.dialog.open = True
        atualizar_interface()




    def fechar_dialogo():
        page.dialog.open = False
        atualizar_interface()

    def exportar_planilha(e):
        wb = xlwt.Workbook()
        ws = wb.add_sheet("Atendimentos")
        headers = ["Número de Protocolo", "CPF", "Nome", "Telefone", "Bairro", "Endereço", "Número de Fossas", "Data Início", "Data Fim"]
        for idx, h in enumerate(headers):
            ws.write(0, idx, h)
        for i, pessoa in enumerate(dados.values(), start=1):
            ws.write(i, 0, pessoa.get("Número de Protocolo"))
            ws.write(i, 1, pessoa.get("CPF"))
            ws.write(i, 2, pessoa.get("Nome"))
            ws.write(i, 3, pessoa.get("Telefone"))
            ws.write(i, 4, pessoa.get("Bairro"))
            ws.write(i, 5, pessoa.get("Endereço"))
            ws.write(i, 6, pessoa.get("Endereço"))
            ws.write(i, 7, pessoa.get("Número de Fossas"))
            ws.write(i, 8, pessoa.get("Data Início"))
            ws.write(i, 9, pessoa.get("Data Fim"))
        wb.save(EXCEL_PATH)
        page.snack_bar = ft.SnackBar(ft.Text("Planilha exportada."))
        page.snack_bar.open = True
        atualizar_interface()

    page.add(
        ft.Column([
            ft.Row([cpf_input, ft.ElevatedButton("Buscar CPF", on_click=buscar_cpf)]),
            container_detalhes,
            ft.Row([
                ft.ElevatedButton("Salvar na Planilha", on_click=exportar_planilha),
                ft.ElevatedButton("Abrir Planilha", on_click=lambda e: os.startfile(EXCEL_PATH) if os.path.exists(EXCEL_PATH) else None)
            ])
        ])
    )
