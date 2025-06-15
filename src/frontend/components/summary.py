import flet as ft
from frontend.components.button import create_button

def summary_dialog(page: ft.Page, summary: str, applicant_info: dict):
    skills = summary["skills"]
    if not skills:
        skills = ["No skills found"]
    else:
        skills = skills[:3] # menampilkan hanya maksimal 3 skill

    job_history = summary["experience"]
    if not job_history:
        job_history = ["No job history found"]
        job_container = ft.Container(
            content=ft.Text(
                "No job history found",
                size=16,
                font_family="PGO",
                color="black",
            ),
            bgcolor="#E2CD95",
            padding=ft.padding.symmetric(10, 20),
            border_radius=20,
            border=ft.border.all(2, "black"),
        )
    else:
        job_list = ft.ListView(
            spacing=10,
            height=100,
            expand=True,
        )
        for job in job_history:
            job_column = ft.Column([
                ft.Text(
                    job[0],
                    size=16,
                    font_family="PGO",
                    color="black",
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    job[1],
                    size=14,
                    font_family="PGO",
                    color="black",
                )
            ], alignment=ft.MainAxisAlignment.START)
            job_list.controls.append(job_column)
        job_container = job_list

    education = summary["education"]
    if not education:
        education_container = ft.Container(
            content=ft.Text(
                "No education found",
                size=16,
                font_family="PGO",
                color="black",
            ),
            bgcolor="#E2CD95",
            padding=ft.padding.symmetric(10, 20),
            border_radius=20,
            border=ft.border.all(2, "black"),
        )
    else:
        education_list = ft.ListView(
            height=100,
            expand=True,
            spacing=10,
        )
        for edu in education:
            education_column = ft.Column([
                ft.Text(
                    edu[0],
                    size=16,
                    font_family="PGO",
                    color="black",
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    edu[1],
                    size=14,
                    font_family="PGO",
                    color="black",
                )
            ], alignment=ft.MainAxisAlignment.START)
            education_list.controls.append(education_column)
        education_container = education_list

    rows = []
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
            ) for skill in skills
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
                            applicant_info["name"],
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            font_family="Freeman",
                            color="black",
                        ),
                        ft.Text(
                            f"Role: {applicant_info['role']}",
                            size=18,
                            font_family="PGO",
                            color="black",
                        ),
                        ft.Text(
                            f"Summary: {summary['summary']}",
                            size=18,
                            font_family="PGO",
                            color="black",
                        ),
                        ft.Text(
                            f"Birthdate: {applicant_info['dob']}",
                            size=18,
                            font_family="PGO",
                            color="black",
                        ),
                        ft.Text(
                            f"Address: {applicant_info['address']}",
                            size=18,
                            font_family="PGO",
                            color="black",
                        ),
                        ft.Text(
                            f"Phone: {applicant_info['phone']}",
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
                            content=job_container,
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
                            content=education_container,
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