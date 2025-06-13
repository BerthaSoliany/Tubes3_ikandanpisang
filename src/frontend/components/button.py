import flet as ft

def create_button(text: str, on_click, bcolor: str, height: int = 50, width: int =100, size: int=20) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text=text, 
        on_click=on_click, 
        color={
            ft.ControlState.DEFAULT: "black",
            ft.ControlState.HOVERED: 'white',
            ft.ControlState.FOCUSED: 'white',
        },
        height=height,
        bgcolor={
            ft.ControlState.DEFAULT: bcolor,
            ft.ControlState.HOVERED: 'black',
            ft.ControlState.FOCUSED: 'black',
        }, 
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(10),
            side=ft.BorderSide(2, 'black'),
            text_style=ft.TextStyle(
                size=size,
                font_family="PGO",
                color="black",
            )
        ),
        width=width,
    )

"""
HOW TO USE

give the function to the button by making a procedure/function
def button_clicked(e):
    page.add(ft.Text("Button clicked!"))

page.add(create_button("Click me", button_clicked, bcolor='green'))
"""