import flet as ft
from frontend.components.navbar import create_navbar
from frontend.components.button import create_button
from frontend.components.resultCard import create_result_card
from backend.controllers.searchController import SearchController

def create_search_page(page: ft.Page):
    rows = []
    keywords_field = ft.TextField(
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
                    )
    
    algorithm_dropdown = ft.Dropdown(
                            width=200,
                            border_color="black",
                            border_radius=10,
                            border_width=2,
                            fill_color="#E2CD95",
                            hint_text="Select an algorithm",
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
                        )
    top_matches_field = ft.TextField(
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
                        )
    results_list = ft.ListView(
                        controls=rows,
                        spacing=20,
                        height=320,
                        expand=True,
                    )

    # match_text = ft.Text(
    #     "",
    #     size=18,
    #     font_family="PGO",
    #     color="black",
    # )
    exact_text = ft.Text(
        "",
        size=18,
        font_family="PGO",
        color="black",
    )
    fuzzy_text = ft.Text(
        "",
        size=18,
        font_family="PGO",
        color="black",
    )

    alert_dialog = ft.AlertDialog(
        title=ft.Text("Invalid Input"),
        title_text_style=ft.TextStyle(
            font_family="PGO",
            size=24,
            color="black",
        ),
        content="",
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

            # ft.TextButton(
            #     "OK",
            #     on_click=lambda e: page.close(alert_dialog),
            #     style=ft.ButtonStyle(
            #         color="black",
            #         bgcolor="#E2A195",
            #         text_style=ft.TextStyle(
            #             font_family="PGO",
            #             size=20,
            #         ),
            #         shape=ft.RoundedRectangleBorder(radius=10)
            #     ),
            # )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def validate_input(e):
        if not keywords_field.value or keywords_field.value.strip() == "":
            alert_dialog.content = ft.Text("Please enter at least one keyword.")
            page.open(alert_dialog)
            page.update()
            return False
        if algorithm_dropdown.value is None:
            alert_dialog.content = ft.Text("Please select an algorithm. ")
            page.open(alert_dialog)
            page.update()
            return False
        if not top_matches_field.value:
            alert_dialog.content = ft.Text("Please enter a value for Top Matches.")
            page.open(alert_dialog)
            page.update()
            return False
        if top_matches_field.value and not top_matches_field.value.isdigit():
            alert_dialog.content = ft.Text("Top Matches must be a number.")
            page.open(alert_dialog)
            page.update()
            return False
        if top_matches_field.value and int(top_matches_field.value) <= 0:
            alert_dialog.content = ft.Text("Please enter a number greater than 0 for Top Matches.")
            page.open(alert_dialog)
            page.update()
            return False
        return True
    
    loading_container = ft.Container(
        content=ft.Column([
            ft.ProgressRing(
                color="black",
                width=50,
                height=50,
                stroke_width=5,
            ),
            ft.Text(
                "Searching...",
                size=20,
                font_family="PGO",
                color="black",
                text_align=ft.TextAlign.CENTER,
            )
        ],
        alignment=ft.alignment.center,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        ),
        visible=False,
        alignment=ft.alignment.center,
    )

    def search_cvs(e):
        if not validate_input(e):
            return
        
        loading_container.visible = True
        results_list.controls.clear()
        results_list.visible = False
        exact_text.value = ""
        fuzzy_text.value = ""
        page.update()

        keywords = [k.strip() for k in keywords_field.value.split(",")]
        algorithm = algorithm_dropdown.value
        top_n = int(top_matches_field.value) if top_matches_field.value else None
        
        algo_map = {"KMP": 0, "Boyer-Moore": 1, "Aho-Corasick": 2}
        algo_index = algo_map.get(algorithm, 0)
        
        results = SearchController.search_cvs(keywords, algo_index, top_n)
        if results:
            results_list.controls.clear()
            stats = results["statistics"]

            exact_count = sum(1 for r in results["results"] if r["exact_matches"])
            fuzzy_count = sum(1 for r in results["results"] if r["fuzzy_matches"])

            exact_text.value = f"Exact matching: {exact_count} CVs ({stats['exact_time']:.4f}s)"
            fuzzy_text.value = f"Fuzzy matching: {fuzzy_count} CVs ({stats['fuzzy_time']:.4f}s)"
            # match_text.value = (
            #     f"Ditemukan sejumlah {len(results['results'])} CV dengan total waktu: {stats['total_time']:.2f}s"
            #     f"({exact_count} exact macth ({stats['exact_time']:.4f}s) dan {fuzzy_count} fuzzy matches ({stats['exact_time']:.4f}s))"
            # )

            if exact_count == 0 and fuzzy_count == 0:
                results_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Image(
                                src="/dust2.png",
                                width=200,
                                height=200,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            ft.Text(
                                "No matches found",
                                size=24,
                                font_family="PGO",
                                color="red",
                                text_align=ft.TextAlign.CENTER,
                                weight= ft.FontWeight.BOLD,
                            ),
                        ], alignment=ft.alignment.center, spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        # ft.Text(
                        #     "No matches found",
                        #     size=24,
                        #     font_family="PGO",
                        #     color="black",
                        #     text_align=ft.TextAlign.CENTER,
                        # ),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(top=20),
                        )
                    )
            else:
                current_row = []
                for result in results["results"]:
                    # print(result)
                    # applicant_info = result.get("applicant_info", {})
                    # print(applicant_info)
                    # applicant_name = applicant_info.get("name", result["name"])
                    card = create_result_card(
                        page=page,
                        name=result["name"],
                        exact_matches=result["exact_matches"],
                        fuzzy_matches=result["fuzzy_matches"],
                        # keywords=[(kw, count) for kw, count, _ in result["matches"]],
                        cv_path=result["cv_path"],
                        applicant_info=result.get("applicant_info"),
                        extracted_cv=result["cv_txt"]
                    )
                    current_row.append(card)
                    # results_list.controls.append(card)
                    
                    if len(current_row) == 3 or result == results["results"][-1]:
                        row = ft.Row(
                            controls=current_row,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                        )
                        results_list.controls.append(row)
                        current_row = []
                            
        loading_container.visible = False
        results_list.visible = True
        page.update()
    
    data = []
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
            # audio_button,
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
                            keywords_field,
                            ft.Row([
                                ft.Column([
                                    ft.Text(
                                        "Algoritma",
                                        size=20,
                                        font_family="PGO",
                                        color="black",
                                    ),
                                    algorithm_dropdown,
                                ]),
                                ft.Column([
                                    ft.Text(
                                        "Top Matches",
                                        size=20,
                                        font_family="PGO",
                                        color="black",
                                    ),
                                    top_matches_field,
                                ]),
                                ft.Container(
                                    content=create_button(
                                        text="Search",
                                        on_click=search_cvs,
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
                                # match_text,
                                exact_text,
                                fuzzy_text,
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            loading_container,
                            results_list,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5, alignment=ft.alignment.center
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