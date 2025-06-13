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
                content=ft.Stack([
                    ft.Container(
                        left=150,
                        top=10,
                        content=ft.Column([
                            ft.Text(
                                "Dive Into Pattern Matching\nwith Digital CV",
                                size=70,
                                weight=ft.FontWeight.BOLD,
                                font_family="Freeman",
                                color="black",
                            ),
                            ft.Container(height=20),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(
                                        "About Project",
                                        size=30,
                                        weight=ft.FontWeight.BOLD,
                                        font_family="PGO",
                                        color="black",
                                    ),
                                    ft.Text(
                                        "A CV analysis tool using advanced pattern matching algorithms (KMP & Boyer-Moore) "
                                        "and Levenshtein Distance for intelligent text comparison.",
                                        size=25,
                                        color="black",
                                        font_family="PGO",
                                    ),
                                ]),
                                padding=20,
                                border_radius=30,
                                bgcolor="#E2CD95",
                                width=400,
                                height=270,
                                border=ft.border.all(2, "black"),
                            ),
                        ]),
                    ),
                    
                    ft.Container(
                        right=150,
                        top=150,
                        content=ft.Column([
                            ft.Text(
                                "Features",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                font_family="PGO",
                                color="black",
                            ),
                            ft.Text(
                                "• Advanced pattern matching algorithms (KMP & Boyer-Moore)\n"
                                "• Levenshtein Distance for intelligent text comparison\n"
                                "• User-friendly interface for CV analysis\n"
                                "• Real-time results and insights",
                                size=20,
                                color="black",
                                font_family="PGO",
                            ),
                        ]),
                        padding=20,
                        border_radius=30,
                        bgcolor="#E2CD95",
                        width=450,
                        height=220,
                        border=ft.border.all(2, "black"),
                    ),
                    
                    ft.Container(
                        right=150,
                        top=390,
                        content=ft.Column([
                            ft.Text(
                                "Author",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                font_family="PGO",
                                color="black",
                            ),
                            ft.Text(
                                # "Created by Team Ikan dan Pisang\n"
                                "Bertha Soliany Frandi"
                                " \\ Rafen Max Alessandro"
                                " \\ Grace Evelyn Simon",
                                size=20,
                                font_family="PGO",
                                color="black",
                            ),
                        ]),
                        padding=20,
                        border_radius=30,
                        bgcolor="#E2CD95",
                        width=500,
                        border=ft.border.all(2, "black"),
                    ),

                    ft.Image(
                        src="/dust1.png",
                        width=250,
                        height=150,
                        fit=ft.ImageFit.CONTAIN,
                        right=5,
                        bottom=-40,
                    ),
                ]),
                padding=0,
                expand=True,
            ),
        ]),
        bgcolor="#EAE6C9",
        expand=True,
        border_radius=30,
    )
    
    return content