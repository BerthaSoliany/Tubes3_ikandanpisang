import flet as ft

class Routes:
    HOME = "/"
    SEARCH = "/search"

def create_navbar(page: ft.Page):
    def on_home_click(e):
        page.go(Routes.HOME)

    def on_search_click(e):
        page.go(Routes.SEARCH)

    navbar = ft.Container(
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
                    alignment=ft.alignment.center,
                ),
            ], spacing=0,
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

    return ft.Stack(
        width=page.window.width,
        expand=True,
        controls=[ft.Image(
                    src="/logo.png",
                    width=80,
                    height=80,
                    fit=ft.ImageFit.CONTAIN,
                    left=30,
                    top=10,
                ),
                navbar,],
        alignment=ft.alignment.top_center,
    )

""""
HOW TO USE

page.add(create_navbar(page))
"""