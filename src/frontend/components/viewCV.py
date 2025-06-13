import flet as ft
import os
from frontend.components.button import create_button

def view_cv_dialog(page: ft.Page, name: str, pdf_path: str):
    def open_pdf(e):
        os.startfile(pdf_path)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            f"{name}'s CV",
            size=30,
            weight=ft.FontWeight.BOLD,
            font_family="Freeman",
            color="black",
            text_align=ft.TextAlign.CENTER,
        ),
        content=ft.Container(
            content=ft.Column([
                ft.Text(
                    "Click below to open the CV in your default PDF viewer:",
                    size=18,
                    font_family="PGO",
                    color="black",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(
                    content=ft.Text(
                        pdf_path,
                        size=16,
                        font_family="PGO",
                        color="black",
                        italic=True,
                    ),
                    bgcolor="#E2CD95",
                    padding=10,
                    border_radius=10,
                    border=ft.border.all(2, "black"),
                ),
                create_button(
                    text="Open PDF",
                    on_click=open_pdf,
                    bcolor="#9EE295",
                ),
            ], 
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            bgcolor="#EAE6C9",
            width=500,
            border_radius=10,
        ),
        actions=[
            create_button(
                text="Close",
                on_click=lambda e: page.close(dialog),
                bcolor="#E2A195",
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor="#EAE6C9",
    )
    
    return dialog