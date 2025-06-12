import flet as ft
from frontend.components.button import create_button
from frontend.components.summary import summary_dialog
from frontend.components.viewCV import view_cv_dialog
import os

def create_result_card(page: ft.Page, name: str, keywords: tuple[str, int]):
    total_matches = sum(kw[1] for kw in keywords)

    keyword_items = [
        ft.Text(
            f"{i+1}. {keywords[i][0]}: {keywords[i][1]} occurence{'s' if keywords[i][1] > 1 else ''}",
            size=18,
            font_family="PGO",
            color="black",
        ) for i in range(len(keywords))
    ]
    
    def show_dialog(e):
        page.open(summary_dialog(page, name))
        page.update()

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    cv = os.path.join(project_root, "data", "11995013.pdf")
    def show_cv_dialog(e):
        pdf_path = cv
        page.open(view_cv_dialog(page, name, pdf_path))
        page.update()

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(
                    name,
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    font_family="Freeman",
                    color="black",
                ),
                ft.Text(
                    f"{total_matches} matches",
                    size=20,
                    font_family="PGO",
                    color="black",
                    italic=True,
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Text(
                "Matched keywords:",
                size=20,
                font_family="PGO",
                color="black",
            ),
            
            ft.Container(
                content=ft.ListView(
                    controls=keyword_items,
                    spacing=5,
                    padding=0,
                ),
                height=100,
                bgcolor="#EAE6C9",
                border_radius=10,
            ),
            
            ft.Row([
                create_button(
                    text="summary",
                    on_click=show_dialog,
                    bcolor="#E2CD95",
                    height=35,
                ),
                create_button(
                    text="view CV",
                    on_click=lambda e: show_cv_dialog(e),
                    bcolor="#E2CD95",
                    height=35,
                )
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        ], spacing=3),
        padding=20,
        border_radius=30,
        bgcolor="#EAE6C9",
        border=ft.border.all(2, "black"),
        width=360,
        # height=250,
        expand=True,
    )