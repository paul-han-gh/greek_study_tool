from textual.app import App, ComposeResult

import widgets


class Home(App):
    def compose(self) -> ComposeResult:
        yield widgets.GreekTextInput()


if __name__ == "__main__":
    app = Home()
    app.run()
