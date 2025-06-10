import flet as ft

def create_button(text: str, on_click, bcolor: str):
    return ft.ElevatedButton(
        text=text, 
        on_click=on_click, 
        color='black', 
        bgcolor={
            ft.ControlState.DEFAULT: bcolor,
            ft.ControlState.HOVERED: 'lightgray',
            ft.ControlState.FOCUSED: 'lightgray',
        }, 
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(10),
            side=ft.BorderSide(2, 'black')
        ),
    )

"""
HOW TO USE

give the function to the button by making a procedure/function
def button_clicked(e):
    page.add(ft.Text("Button clicked!"))

page.add(create_button("Click me", button_clicked, bcolor='green'))
"""