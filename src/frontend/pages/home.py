import flet as ft
from frontend.components.navbar import create_navbar

def create_home_page(page: ft.Page):
    content = ft.Container(
        content=ft.Column([
            ft.Container(
                content=create_navbar(page),
                alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Image(
                            src="/assets/icon.png",
                            width=100,
                            height=100,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        ft.Text(
                            "Dive Into Pattern Matching\nwith Digital CV",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            font_family="Freeman",
                            color="black",
                        ),
                    ], alignment=ft.MainAxisAlignment.START),
                    
                    ft.Row([
                        ft.Container(
                            content=ft.Text(
                                "A CV analysis tool using advanced pattern matching algorithms (KMP & Boyer-Moore) "
                                "and Levenshtein Distance for intelligent text comparison.",
                                size=16,
                                color="black",
                                font_family="PGO",
                            ),
                            padding=20,
                            border_radius=10,
                            bgcolor="#E2CD95",
                            width=400,
                            border=ft.border.all(2, "black"),

                        ),
                        
                        ft.Column([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(
                                        "Features", 
                                        size=24, 
                                        weight=ft.FontWeight.BOLD, 
                                        font_family="PGO",
                                        color="black",
                                    ),
                                    ft.Text(
                                        "• Pattern Matching with KMP & Boyer-Moore\n"
                                        "• Text Similarity with Levenshtein Distance\n"
                                        "• Automated CV Information Extraction\n"
                                        "• MySQL Database Integration",
                                        size=16,
                                        font_family="PGO",
                                        color="black",
                                    ),
                                ]),
                                padding=20,
                                border_radius=10,
                                bgcolor="#E2CD95",
                                width=400,
                                border=ft.border.all(2, "black"),
                            ),
                            
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(
                                        "Author", 
                                        size=24, 
                                        weight=ft.FontWeight.BOLD, 
                                        font_family="PGO",
                                        color="black",
                                    ),
                                    ft.Text(
                                        "Created by Team Ikan dan Pisang\n"
                                        "• Albert Ghazaly\n"
                                        "• Bertha Soliany\n"
                                        "• Matthew Mahendra",
                                        size=16,
                                        font_family="PGO",
                                        color="black",
                                    ),
                                ]),
                                padding=20,
                                border_radius=10,
                                bgcolor="#E2CD95",
                                width=400,
                                border=ft.border.all(2, "black"),
                            ),
                        ], alignment=ft.MainAxisAlignment.END),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ]),
                padding=30,
                expand=True,
                alignment=ft.alignment.center,
            ),
        ]),
        bgcolor="#EAE6C9",
        expand=True,
    )
    
    return content