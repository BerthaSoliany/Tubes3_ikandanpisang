import flet as ft
from frontend.components.button import create_button

def summary_dialog(page: ft.Page, name: str):
    personal_info = {
    "name": name,
    "birthdate": "05-19-2025",
    "address": "Masjid Salman ITB",
    "phone": "0812 3456 7890",
    "summary": "Experienced software engineer with a strong background in web development and a passion for building scalable applications. Proficient in both frontend and backend technologies, with a focus on delivering high-quality code and user experiences.",
    }
    skills = [
        "React", "Express", "HTML", "CSS", "JavaScript", "Python", "Django",
        "Flask", "Node.js", "MongoDB", "PostgreSQL", "MySQL", "Git", "Docker",
    ]
    job_history = [
        "Software Engineer at Company A (2020-2022)",
        "Frontend Developer at Company B (2018-2020)",
        "Backend Developer at Company C (2016-2018)",
    ]
    education = [
        "Bachelor of Computer Science, University X (2012-2016)",
        "Master of Software Engineering, University Y (2016-2018)",
        "PhD in Computer Science, University Z (2018-2022)",
    ]
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
                        content=ft.Column(
                            controls=[
                            ft.Text(
                                personal_info["name"],
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                font_family="Freeman",
                                color="black",
                            ),
                            ft.Text(
                                "Summary:",
                                size=20,
                                # weight=ft.FontWeight.BOLD,
                                font_family="PGO",
                                color="black",
                            ),
                            ft.Text(
                                f"Birthdate: {personal_info['birthdate']}",
                                size=18,
                                font_family="PGO",
                                color="black",
                            ),
                            ft.Text(
                                f"Address: {personal_info['address']}",
                                size=18,
                                font_family="PGO",
                                color="black",
                            ),
                            ft.Text(
                                f"Phone: {personal_info['phone']}",
                                size=18,
                                font_family="PGO",
                                color="black",
                            ),]
                        ),
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
                                    controls=[
                                        ft.Text(
                                            job,
                                            size=16,
                                            font_family="PGO",
                                            color="black",
                                        ) for job in job_history
                                    ],
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
                                    controls=[
                                        ft.Text(
                                            edu,
                                            size=16,
                                            font_family="PGO",
                                            color="black",
                                        ) for edu in education
                                    ],
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