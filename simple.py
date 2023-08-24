#!/usr/bin/env python3
from pathlib import Path
from textual.app import App, ComposeResult
from textual.reactive import var
from textual.widgets import MarkdownViewer
from textual.binding import Binding
import sys


class MainApp(App):
    CSS = """
    Screen {
        overflow: hidden;
    }
    """

    BINDINGS = [
        Binding("t", "toggle_table_of_contents", ""),
        Binding("k", "up", "", show=False),
        Binding("j", "down", "", show=False),
        Binding("q", "quit", "", show=False),
        Binding("g", "home", "", show=False),
        Binding("G", "end", "", show=False),
    ]

    path = var(Path(sys.argv[1]).resolve())

    def compose(self) -> ComposeResult:
        yield MarkdownViewer(show_table_of_contents=False)

    @property
    def markdown_viewer(self) -> MarkdownViewer:
        return self.query_one(MarkdownViewer)

    async def on_mount(self) -> None:
        self.markdown_viewer.focus()
        try:
            await self.markdown_viewer.go(self.path)
        except FileNotFoundError:
            self.exit(message=f"Unable to load {self.path!r}")

    def action_toggle_table_of_contents(self) -> None:
        self.markdown_viewer.show_table_of_contents = \
                not self.markdown_viewer.show_table_of_contents

    def action_up(self) -> None:
        self.markdown_viewer.scroll_up(animate=False)

    def action_down(self) -> None:
        self.markdown_viewer.scroll_down(animate=False)

    def action_home(self) -> None:
        self.markdown_viewer.scroll_home(animate=False)

    def action_end(self) -> None:
        self.markdown_viewer.scroll_end(animate=False)


if __name__ == "__main__":
    app = MainApp()
    app.run()
