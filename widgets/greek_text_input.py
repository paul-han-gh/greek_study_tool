from textual import events

from textual.widgets import Input


class GreekTextInput(Input):
    """An input field that transposes keypresses into Greek characters"""


    character_mapping = {
        'a': 'α'
    }


    def on_key(self, event: events.Key) -> None:
        self._restart_blink()

        if (
            event.is_printable
            and event.character in self.character_mapping
        ):
            event.stop()
            selection = self.selection
            character = self.character_mapping[event.character]
            if selection.is_empty:
                self.insert_text_at_cursor(character)
            else:
                self.replace(character, *selection)
            event.prevent_default()
