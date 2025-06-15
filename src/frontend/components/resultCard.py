import flet as ft
from frontend.components.button import create_button
from frontend.components.summary import summary_dialog
from backend.algorithms.regex_parse import get_summary
import os

def create_result_card(page: ft.Page, name: str, exact_matches: list[tuple[str, int]], fuzzy_matches: list[tuple[str, int]], cv_path: str, applicant_info: dict = None, extracted_cv: str = None):
    if not exact_matches and not fuzzy_matches:
        return ft.Container(
            content=ft.Text(
                "No matches found",
                size=20,
                font_family="PGO",
                color="black",
            ),
            padding=20,
            border_radius=30,
            bgcolor="#EAE6C9",
            border=ft.border.all(2, "black"),
            width=360,
            height=250,
            expand=True,
        )
    
    total_matches = sum(m[1] for m in exact_matches + fuzzy_matches)

    matches_list = ft.ListView(
        spacing=5,
    )

    if exact_matches:
        matches_list.controls.append(
            ft.Text(
                "Exact matches:",
                size=20,
                font_family="PGO",
                color="black",
                weight=ft.FontWeight.BOLD
            )
        )
        
        for i, match in enumerate(exact_matches):
            if match[1] > 0:
                matches_list.controls.append(
                    ft.Text(
                        f"{i+1}. {match[0]}: {match[1]} occurence{'s' if match[1] > 1 else ''}",
                        size=18,
                        font_family="PGO",
                        color="black",
                    )
                )

    if fuzzy_matches:
        matches_list.controls.append(
            ft.Text(
                "Fuzzy matches:",
                size=20,
                font_family="PGO",
                color="black",
                weight=ft.FontWeight.BOLD
            )
        )
        
        for i, match in enumerate(fuzzy_matches):
            if match[1] > 0:
                matches_list.controls.append(
                    ft.Text(
                        f"{i+1}. {match[0]}: {match[1]} occurence{'s' if match[1] > 1 else ''}",
                        size=18,
                        font_family="PGO",
                        color="black",
                        italic=True
                    )
                )

    def show_dialog(e):
        summary = get_summary(extracted_cv)
        page.open(summary_dialog(page, summary, applicant_info))
        page.update()

    alert_dialog = ft.AlertDialog(
        content="CV not found. Please check the file path.",
        content_text_style=ft.TextStyle(
            font_family="PGO",
            size=20,
            color="black",
        ),
        alignment=ft.alignment.center,
        bgcolor="#EAE6C9",
        actions=[
            create_button(
                text="OK",
                on_click=lambda e: page.close(alert_dialog),
                bcolor="#E2A195",
                height=30,
                width=50,
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    def open_cv(e):
        if not os.path.exists(cv_path):
            page.open(alert_dialog)
            page.update()
            return
        else:
            os.startfile(cv_path)

    if applicant_info:
        info_items = []
        if applicant_info.get("role"):
            info_items.append(
                ft.Text(
                    f"Role: {applicant_info['role']}",
                    size=16,
                    font_family="PGO",
                    color="black",
                    italic=True
                )
            )

    display_name = name
    if applicant_info and applicant_info.get("name"):
        display_name = applicant_info["name"]
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(
                    display_name,
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
            ft.Container(
                content=matches_list,
                height=130,
                bgcolor="#EAE6C9",
                border_radius=10,
            ),
            ft.Row([
                create_button(
                    text="Summary",
                    on_click=show_dialog,
                    bcolor="#E2CD95",
                    height=35,
                ),
                create_button(
                    text="View CV",
                    on_click=lambda e: open_cv(e),
                    bcolor="#E2CD95",
                    height=35,
                )
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        ], spacing=5),
        padding=20,
        border_radius=30,
        bgcolor="#EAE6C9",
        border=ft.border.all(2, "black"),
        width=360,
        expand=True,
    )