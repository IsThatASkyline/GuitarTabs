from aiogram_dialog.widgets.text import Jinja


SONG_CHORDS_WITHOUT_TABS_TEMPLATE = Jinja(
            "Аккорды для песни \n"
            "{% for verse in verses %}"
            "\n\n{{ verse.title }}:\n"
            "{% for verse_string in verse.strings%}"
            "{% for chord in verse_string.chords %}"
            "{% if verse_string.chords_count == 1 %}"
            "{{ chord.title }}"
            "{% elif verse_string.chords_count == 2 %}"
            "{{ '%-50s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 3 %}"
            "{{ '%-26s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 4 %}"
            "{{ '%-17s'|format(chord.title) }}"
            "{% endif %}"
            "{% endfor %}"
            "\n\n{{ verse_string.lyrics }}\n"
            "{% endfor %}"
            "{% endfor %}"
        )

SONG_CHORDS_WITH_TABS_TEMPLATE = Jinja(
            "Аккорды для песни \n\n"
            "{% for chord in chords_tabs %}"            
            "{{ chord.title }}:"
            "{{ chord.tab }}\n"
            "{% endfor %}"
            "{% for verse in verses %}"
            "\n\n{{ verse.title }}:\n"
            "{% for verse_string in verse.strings%}"
            "{% for chord in verse_string.chords %}"
            "{% if verse_string.chords_count == 1 %}"
            "{{ chord.title }}"
            "{% elif verse_string.chords_count == 2 %}"
            "{{ '%-50s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 3 %}"
            "{{ '%-26s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 4 %}"
            "{{ '%-17s'|format(chord.title) }}"
            "{% endif %}"
            "{% endfor %}"
            "\n\n{{ verse_string.lyrics }}\n"
            "{% endfor %}"
            "{% endfor %}"
        )