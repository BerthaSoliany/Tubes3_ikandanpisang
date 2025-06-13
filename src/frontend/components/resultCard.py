import flet as ft
from frontend.components.button import create_button
from frontend.components.summary import summary_dialog
from frontend.components.viewCV import view_cv_dialog
import os

def create_result_card(page: ft.Page, name: str, exact_matches: list[tuple[str, int]], fuzzy_matches: list[tuple[str, int]], cv_path: str, applicant_info: dict = None):
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

    # keyword_items = [
    #     ft.Text(
    #         f"{i+1}. {keywords[i][0]}: {keywords[i][1]} occurence{'s' if keywords[i][1] > 1 else ''}",
    #         size=18,
    #         font_family="PGO",
    #         color="black",
    #     ) for i in range(len(keywords))
    # ]

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

    # exact_items = []
    # if exact_matches:
    #     exact_items.extend([
    #         ft.Text(
    #             "Exact matches:",
    #             size=20,
    #             font_family="PGO",
    #             color="black",
    #             weight=ft.FontWeight.BOLD
    #         ),
    #         *[ft.Text(
    #             f"{i+1}. {match[0]}: {match[1]} occurence{'s' if match[1] > 1 else ''}",
    #             size=18,
    #             font_family="PGO",
    #             color="black",
    #         ) for i, match in enumerate(exact_matches)]
    #     ])
    
    # # Create fuzzy match items
    # fuzzy_items = []
    # if fuzzy_matches:
    #     fuzzy_items.extend([
    #         ft.Text(
    #             "Fuzzy matches:",
    #             size=20,
    #             font_family="PGO",
    #             color="black",
    #             weight=ft.FontWeight.BOLD,
    #             color="#E2A195"  # Different color for fuzzy matches
    #         ),
    #         *[ft.Text(
    #             f"{i+1}. {match[0]}: {match[1]} occurence{'s' if match[1] > 1 else ''}",
    #             size=18,
    #             font_family="PGO",
    #             color="#E2A195",  # Same color for fuzzy matches
    #             italic=True
    #         ) for i, match in enumerate(fuzzy_matches)]
    #     ])

    
    def show_dialog(e):
        page.open(summary_dialog(page, name))
        page.update()

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    cv = os.path.join(project_root, cv_path)
    def show_cv_dialog(e):
        pdf_path = cv
        page.open(view_cv_dialog(page, name, pdf_path))
        page.update()

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
            
            # ft.Text(
            #     "Matched keywords:",
            #     size=20,
            #     font_family="PGO",
            #     color="black",
            # ),
            
            ft.Container(
                content=matches_list,
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