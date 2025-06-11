import flet as ft
from frontend.components.button import create_button

def create_result_card(page: ft.Page, name: str, keywords: tuple[str, int]):
    total_matches = sum(kw[1] for kw in keywords)
    
    return ft.Container(
        content=ft.Column([
            # Header
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
                    [
                        ft.Text(
                            f"{i+1}. {keywords[i][0]}: {keywords[i][1]} occurence{'s' if keywords[i][1] > 1 else ''}",
                            size=18,
                            font_family="PGO",
                            color="black",
                        ) for i in range(len(keywords))
                    ],
                    spacing=5,
                    height=150,
                ),
            ),
            
            ft.Row([
                create_button(
                    text="summary",
                    on_click=lambda e: page.go(f"/src/frontend/pages/summaryPage?name={name}"),
                    bcolor="#E2CD95"
                ),
                create_button(
                    text="view CV",
                    on_click=lambda e: page.go(f"/src/frontend/pages/cvPage?name={name}"),
                    bcolor="#E2CD95"
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ], spacing=10),
        padding=20,
        border_radius=30,
        bgcolor="#E2CD95",
        border=ft.border.all(2, "black"),
        width=400,
        height=300,
    )