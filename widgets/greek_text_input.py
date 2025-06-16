from textual import events

from textual.widgets import Input


class GreekTextInput(Input):
    """An input field that transposes keypresses into Greek characters"""


    character_mapping = {
        'a': 'α',
        'b': 'β',
        'd': 'δ',
        'e': 'ε',
        'g': 'γ',
        'i': 'ι',
        'j': 'η',
        'k': 'κ',
        'p': 'π',
        'r': 'ρ',
        't': 'τ',
        'z': 'ζ'
    }


    def on_key(self, event: events.Key) -> None:
        self._restart_blink()

        if event.is_printable:
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
                    case 'κ':
                        character = 'χ'
                        replace_character_before_insert_position = True
                    case 'π':
                        character = 'φ'
                        replace_character_before_insert_position = True
                    case 'ρ':
                        character = 'ῥ'
                        replace_character_before_insert_position = True
                    case 'ῥ':
                        character = 'ῤ'
                        replace_character_before_insert_position = True
                    case 'τ':
                        character = 'θ'
                        replace_character_before_insert_position = True
                    case _:
                        character = '-'

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
