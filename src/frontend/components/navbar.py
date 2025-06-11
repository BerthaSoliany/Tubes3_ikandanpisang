import flet as ft

def create_navbar(page: ft.Page):
    # page.fonts = {
    #     "PGO": "fonts/Pathway_Gothic_One/PathwayGothicOne-Regular.ttf",
    # }

    # page.theme = ft.Theme(font_family="PGO")

    def flush_session(e):
        # contoh
        page.session.set("Tanaman", None)
        page.session.set("Sorting", None)
        page.session.set("action", None)
        page.session.set("jenis_tanaman", None)
        page.session.set("index_tanaman", None)
        page.session.set("data_pertumbuhan_tanaman", None)

    def on_home_click(e):
        flush_session(e)
        page.go("/src/main")

    def on_search_click(e):
        flush_session(e)
        page.go("/src/frontend/pages/searchPage")   

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.TextButton(
                                "Home", 
                                on_click=on_home_click, 
                                style=ft.ButtonStyle(
                                    color='white', 
                                    text_style=ft.TextStyle(
                                        font_family="PGO", 
                                        size=40, 
                                        decoration={
                                            ft.ControlState.HOVERED: ft.TextDecoration.UNDERLINE, 
                                            ft.ControlState.FOCUSED: ft.TextDecoration.UNDERLINE
                                        }
                                    )
                                )
                            ),
                            ft.TextButton(
                                "Search", 
                                on_click=on_search_click, 
                                style=ft.ButtonStyle(
                                    color='white', 
                                    text_style=ft.TextStyle(
                                        font_family="PGO", 
                                        size=40, 
                                        decoration={
                                            ft.ControlState.HOVERED: ft.TextDecoration.UNDERLINE, 
                                            ft.ControlState.FOCUSED: ft.TextDecoration.UNDERLINE
                                        }
                                    )
                                )
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    expand=True,
                ),
            ],
        ),
        bgcolor='black',
        padding=10,
        margin=0,
        width=600,
        height=92,
        border_radius=ft.border_radius.only(
            bottom_left=30,
            bottom_right=30,
        ),
    )

""""
HOW TO USE

page.add(create_navbar(page))
"""