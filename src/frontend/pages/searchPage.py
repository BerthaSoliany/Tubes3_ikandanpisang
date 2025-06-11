import flet as ft
from frontend.components.navbar import create_navbar
from frontend.components.button import create_button
from frontend.components.resultCard import create_result_card

def create_search_page(page: ft.Page):
    content = ft.Container(
        content=ft.Column([
            ft.Container(
                content=create_navbar(page),
                alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "Keywords",
                                size=24,
                                font_family="PGO",
                                color="black",
                            ),
                            ft.TextField(
                                width=800,
                                height=50,
                                border_radius=10,
                                bgcolor="#E2CD95",
                                border_color="black",
                                text_style=ft.TextStyle(
                                    color="black",
                                    size=20,
                                    font_family="PGO",
                                ),
                            ),
                            ft.Row([
                                ft.Column([
                                    ft.Text(
                                        "Algoritma",
                                        size=20,
                                        font_family="PGO",
                                        color="black",
                                    ),
                                    ft.Dropdown(
                                        width=200,
                                        bgcolor="#E2CD95",
                                        border_color="black",
                                        options=[
                                            ft.dropdown.Option("KMP"),
                                            ft.dropdown.Option("Boyer-Moore"),
                                            ft.dropdown.Option("Aho-Corasick"),
                                        ],
                                    ),
                                ]),
                                ft.Column([
                                    ft.Text(
                                        "Top Matches",
                                        size=20,
                                        font_family="PGO",
                                        color="black",
                                    ),
                                    ft.TextField(
                                        width=200,
                                        height=40,
                                        bgcolor="#E2CD95",
                                        border_color="black",
                                    ),
                                ]),
                                ft.Container(
                                    content=create_button(
                                        text="Search",
                                        on_click=lambda e: None,
                                        bcolor="#9EE295"
                                    ),
                                    padding=ft.padding.only(top=25),
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ]),
                        padding=20,
                    ),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "Results",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                font_family="Freeman",
                                color="black",
                            ),
                            ft.Row([
                                ft.Text(
                                    "Exact Match: 100 CVs scanned in 100ms",
                                    size=18,
                                    font_family="PGO",
                                    color="black",
                                ),
                                ft.Text(
                                    "Fuzzy Match: 100 CVs scanned in 101ms",
                                    size=18,
                                    font_family="PGO",
                                    color="black",
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            
                            ft.ListView(
                                controls=[
                                    create_result_card(page, "Farhan", [("React", 1), ("Express", 2), ("HTML", 1), ("uuuu", 1), ("aaaa",3)]),
                                    create_result_card(page, "Farhan", [("React", 1), ("Express", 2), ("HTML", 1)]),
                                    create_result_card(page, "Farhan", [("React", 1), ("Express", 2), ("HTML", 1)]),
                                ],
                                spacing=20,
                                height=320,
                                horizontal=True,
                                auto_scroll=True
                            ),
                        ]),
                        padding=20,
                        bgcolor="#E2CD95",
                        border_radius=10,
                        border=ft.border.all(2, "black"),
                    ),
                ]),
                padding=30,
            ),
        ]),
        bgcolor="#EAE6C9",
    )
    
    return content