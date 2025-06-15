import flet as ft
import flet_audio as fta
from frontend.pages.home import create_home_page
from frontend.pages.searchPage import create_search_page
from backend.database.connection import db_manager
from backend.controllers.searchController import SearchController
from frontend.components.navbar import Routes

def main(page: ft.Page):
    if not db_manager.initialize_connection():
        print("Failed to initialize database connection")
        return
    else:
        print("Starting PDF extract...")
        dict_of_cv_texts = SearchController.extract_cv_texts()
        if dict_of_cv_texts is None:
            print("Failed to extract CV texts")
            return
        print("PDF extract completed successfully")
    page.title = "CV Pattern Matching"
    page.padding = 0
    page.bgcolor = '#EAE6C9'
    page.window.height = 800
    page.window.width = 1300

    page.fonts = {
        "PGO": "/fonts/Pathway_Gothic_One/PathwayGothicOne-Regular.ttf",
        "Freeman": "/fonts/Freeman/Freeman-Regular.ttf",
    }

    background_audio = fta.Audio(
        src="lofi-295209.mp3",
        autoplay=True,
    )
    page.overlay.append(background_audio)

    is_playing = True

    def toggle_audio(e):
        nonlocal is_playing
        if is_playing:
            background_audio.pause()
            audio_button.icon = ft.Icons.PLAY_ARROW
            audio_button.tooltip = "Play music"
        else:
            background_audio.play()
            audio_button.icon = ft.Icons.PAUSE
            audio_button.tooltip = "Pause music"
        is_playing = not is_playing
        audio_button.update()

    audio_button = ft.FloatingActionButton(
        icon=ft.Icons.PAUSE,
        bgcolor="black",
        # icon_color="black",
        tooltip="Pause music",
        on_click=toggle_audio,
        width=40,
        height=40,
        # left=1115,
        # top=550
        right=50,
        bottom=50,
    )

    def route_change(route):
        page.views.clear()
        if page.route == Routes.HOME:
            page.views.append(
                ft.View(
                    route=Routes.HOME,
                    controls=[create_home_page(page, audio_button)]
                )
            )
        elif page.route == Routes.SEARCH:
            page.views.append(
                ft.View(
                    route=Routes.SEARCH,
                    controls=[create_search_page(page, dict_of_cv_texts)]
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(Routes.HOME)

if __name__ == "__main__":
    ft.app(target=main)