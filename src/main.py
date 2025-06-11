import flet as ft
from frontend.pages.home import create_home_page

def main(page: ft.Page):
    page.title = "CV Pattern Matching"
    page.padding = 0
    page.bgcolor = '#EAE6C9'

    page.fonts = {
        "PGO": "/fonts/Pathway_Gothic_One/PathwayGothicOne-Regular.ttf",
        "Freeman": "/fonts/Freeman/Freeman-Regular.ttf",
    }

    # page.theme = ft.Theme(
    #     font_family="PGO",
    #     text_theme=ft.TextTheme(
    #         body_large=ft.TextStyle(color="black"),
    #         body_medium=ft.TextStyle(color="black"),
    #         body_small=ft.TextStyle(color="black"),
    #     )
    # )

    # page.theme = ft.Theme(
    #     font_family="Freeman",  # Set default font
    #     text_theme=ft.TextTheme(
    #         body_large=ft.TextStyle(color="black"),
    #         body_medium=ft.TextStyle(color="black"),
    #         body_small=ft.TextStyle(color="black"),
    #     )
    # )

    def route_change(route):
        page.views.clear()
        if page.route == "/" or page.route == "/src/main":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[create_home_page(page)]
                )
            )
        elif page.route == "/src/frontend/pages/searchPage":
            pass
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)