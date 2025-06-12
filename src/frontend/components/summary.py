import flet as ft
from frontend.components.button import create_button

skills = [
    "React", "Express", "HTML", "CSS", "JavaScript", "Python", "Django",
    "Flask", "Node.js", "MongoDB", "PostgreSQL", "MySQL", "Git", "Docker",
]

def summary_dialog(page: ft.Page, name: str):
        rows = []
        for i in range(0, len(skills), 6):
            row = ft.Row([
                    ft.Container(
                        content=ft.Text(
                            skill,
                            size=16,
                            font_family="PGO",
                            color="black",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        bgcolor="#E2D995",
                        padding=ft.padding.symmetric(10, 20),
                        border_radius=20,
                        border=ft.border.all(2, "black"),
                    ) for skill in skills[i:i+6]
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=5,
            )
            rows.append(row)
        # panggil fungsi meks disini. trus isi sesuai data2nya. fetch dr database
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "CV Summary",
                size=30,
                weight=ft.FontWeight.BOLD,
                font_family="Freeman",
                color="black",
                text_align=ft.TextAlign.CENTER,
            ),
            title_text_style=ft.TextStyle(
                font_family="Freeman",
                size=30,
                weight=ft.FontWeight.BOLD,
                color="black",
            ),
            content_text_style=ft.TextStyle(
                font_family="PGO",
                size=18,
                color="black",
            ),
            content=ft.Container(
                content=ft.Column([
                    # Personal Info Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                name,
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                font_family="Freeman",
                                color="black",
                            ),
                            ft.Text(
                                "Birthdate: 05-19-2025",
                                size=18,
                                font_family="PGO",
                                color="black",
                            ),
                            ft.Text(
                                "Address: Masjid Salman ITB",
                                size=18,
                                font_family="PGO",
                                color="black",
                            ),
                            ft.Text(
                                "Phone: 0812 3456 7890",
                                size=18,
                                font_family="PGO",
                                color="black",
                            ),
                        ]),
                        bgcolor="#E2CD95",
                        padding=10,
                        border_radius=10,
                        border=ft.border.all(2, "black"),
                        width=600,
                        expand=True,
                    ),
                    
                    # Skills Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "Skills",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                font_family="Freeman",
                                color="black",
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=rows,
                                    spacing=10,
                                    horizontal_alignment=ft.CrossAxisAlignment.START,
                                ),
                                bgcolor="#E2CD95",
                                border_radius=8,
                                padding=10,
                                border=ft.border.all(2, "black"),
                                width=600,
                            ),
                        ]),
                    ),
                    
                    # Job History Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "Job History",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                font_family="Freeman",
                                color="black",
                            ),
                            ft.Container(
                                bgcolor="#E2CD95",
                                border_radius=10,
                                padding=10,
                                content=ft.ListView(
                                    height=100,
                                    spacing=5,
                                ),
                                border=ft.border.all(2, "black")
                            ),
                        ]),
                    ),
                    
                    # Education Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "Education",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                font_family="Freeman",
                                color="black",
                            ),
                            ft.Container(
                                bgcolor="#E2CD95",
                                border_radius=10,
                                padding=10,
                                content=ft.ListView(
                                    height=100,
                                    spacing=5,
                                ),
                                border=ft.border.all(2, "black")
                            ),
                        ],),
                    ),
                ], scroll=ft.ScrollMode.AUTO, spacing=20),
                padding=20,
                bgcolor="#EAE6C9",
                width=600,
                height=800,
                expand=True,
                border_radius=10,
                # border=ft.border.all(2, "black"),
            ),
            actions=[create_button(
                text="Close",
                on_click=lambda e: page.close(dialog),
                bcolor="#E2A195",
            )],
            actions_alignment=ft.MainAxisAlignment.END,
            alignment=ft.alignment.top_center,
            bgcolor="#EAE6C9",
            
        )
        return dialog
        
        # page.open(dialog)
        # page.update()