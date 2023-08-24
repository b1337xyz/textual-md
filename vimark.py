#!/usr/bin/env python3
from pathlib import Path
from textual.app import App, ComposeResult
from textual.reactive import var
from textual.widgets import MarkdownViewer, LoadingIndicator
from textual.binding import Binding
from textual import work
# from textual.worker import Worker, get_current_worker
import sys


class MainApp(App):
    CSS = """\
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

    @property
    def markdown_viewer(self) -> MarkdownViewer:
        return self.query_one(MarkdownViewer)

    def compose(self) -> ComposeResult:
        yield LoadingIndicator()
        yield MarkdownViewer(show_table_of_contents=False)

    async def on_mount(self) -> None:
        self.load_file()

    @work(exclusive=True, thread=True)
    async def load_file(self) -> None:
        # the only way I've found to load a big markdown file without
        # hanging the entire app (not showing the LoadingIndicator)
        # is to use thread=True... TODO: fix this?
        self.markdown_viewer.focus()
        try:
            self.call_from_thread(self.markdown_viewer.go, self.path)
        except FileNotFoundError:
            self.exit(message=f"Unable to load {self.path!r}")

        self.query_one(LoadingIndicator).remove()

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
