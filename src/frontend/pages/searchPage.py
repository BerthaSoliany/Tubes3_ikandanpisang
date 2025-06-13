import flet as ft
from frontend.components.navbar import create_navbar
from frontend.components.button import create_button
from frontend.components.resultCard import create_result_card

def create_search_page(page: ft.Page):
    is_exact_match = True
    match_text = (
        f"Exact Match: {1} CVs scanned in {100}ms" 
        if is_exact_match 
        else f"Fuzzy Match: {1} CVs scanned in {101}ms"
    )
    data = [create_result_card(page, "Farhan", [("React", 1), ("Express", 2), ("HTML", 1), ("CSS", 1), ("JavaScript", 23)]),
            create_result_card(page, "Farhan", [("React", 1), ("Express", 2), ("HTML", 1)]),
            create_result_card(page, "Farhan", [("React", 1), ("Express", 2), ("HTML", 1)]),
            create_result_card(page, "Farhan", [("React", 1), ("Express", 2), ("HTML", 1)]),
    ]
    rows = []
    for i in range(0, len(data), 3):
        row = ft.Row(
            controls=data[i:i+3],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
        rows.append(row)
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
                                # width=800,
                                height=50,
                                border_radius=10,
                                bgcolor="#E2CD95",
                                border_color="black",
                                border_width=2,
                                text_style=ft.TextStyle(
                                    color="black",
                                    size=20,
                                    font_family="PGO",
                                ),
                                cursor_color="black",
                                hint_text="ex: React, Express, HTML",
                                hint_style=ft.TextStyle(
                                    color="grey",
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
                                        border_color="black",
                                        border_radius=10,
                                        border_width=2,
                                        fill_color="#E2CD95",
                                        # color="#E2CD95",
                                        text_style=ft.TextStyle(
                                            color="black",
                                            size=20,
                                            font_family="PGO",
                                            # bgcolor="#E2CD95",
                                        ),
                                        bgcolor="black",

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
                                        height=50,
                                        bgcolor="#E2CD95",
                                        border_color="black",
                                        border_radius=10,
                                        border_width=2,
                                        color="black",
                                        cursor_color="black",
                                        text_style=ft.TextStyle(
                                            color="black",
                                            size=20,
                                            font_family="PGO",
                                        ),
                                        hint_text="ex: 3",
                                        hint_style=ft.TextStyle(
                                            color="grey",
                                            size=20,
                                            font_family="PGO",
                                        ),
                                    ),
                                ]),
                                ft.Container(
                                    content=create_button(
                                        text="Search",
                                        on_click=lambda e: None, # manggil fungsi search meks
                                        bcolor="#9EE295",
                                        width=200,
                                    ),
                                    padding=ft.padding.only(top=39, left=570),
                                ),
                            ], alignment=ft.MainAxisAlignment.START, spacing=20),
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
                                    match_text,
                                    size=18,
                                    font_family="PGO",
                                    color="black",
                                ),
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            
                            ft.ListView(
                                controls=rows,
                                spacing=20,
                                height=320,
                                expand=True,
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5
                        ),
                        padding=ft.padding.only(top=10, left=20, right=20, bottom=10),
                        bgcolor="#E2CD95",
                        border_radius=10,
                        border=ft.border.all(2, "black"),
                        alignment=ft.alignment.center,
                        # width=1210,
                        height=380,
                        margin=ft.margin.only(bottom=20, left=20, right=20),
                        expand=True,
                    ),
                ]),
                padding=ft.padding.only(top=0, left=10, right=10, bottom=5),
            ),
        ]),
        bgcolor="#EAE6C9",
        border_radius=30,
        expand=True,
        alignment=ft.alignment.center,
    )
    
    return content