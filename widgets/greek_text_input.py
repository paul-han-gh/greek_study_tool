from textual import events

from textual.widgets import Input


class GreekTextInput(Input):
    """An input field that transposes keypresses into Greek characters"""


    character_mapping = {
        'a': 'α',
        'b': 'β',
        'g': 'γ',
        'd': 'δ',
        'e': 'ε',
        'z': 'ζ',
        'i': 'ι',
        't': 'τ'
    }


    def on_key(self, event: events.Key) -> None:
        self._restart_blink()
        event.stop()
        character = event.character
        character_before_insert_position = self.value[:(
            self.cursor_position
            if self.selection.is_empty
            else self.selection.start
        )][-1:]
        replace_character_before_insert_position = False

        if character in self.character_mapping:
            character = self.character_mapping[character]
        elif character == 'h':
            match character_before_insert_position:
                case 'τ':
                    character = 'θ'
                    replace_character_before_insert_position = True

        selection = self.selection
        if selection.is_empty:
            if replace_character_before_insert_position:
                self.replace(character, self.cursor_position - 1, self.cursor_position)
            else:
                self.insert_text_at_cursor(character)
        else:
            start = (
                selection.start - 1
                if replace_character_before_insert_position
                else selection.start
            )
            self.replace(character, start, selection.end)
        event.prevent_default()
