from aiogram_dialog.widgets.text import Jinja

SONG_CHORDS_WITHOUT_TABS_TEMPLATE = Jinja(
    "<b>{{ song.band.title }} - {{ song.title }}</b>\n"
    "{% for verse in verses %}"
    "{% if not verse.strings  %}"
    "\n\n{{ verse.title }}\n"
    "{% else %}"
    "\n\n{{ verse.title }}:\n"
    "{% for verse_string in verse.strings %}"
    "{% if verse_string.lyrics %}"
    "{% if not verse_string.chords %}"
    "{{ verse_string.space_between_chords }}"
    "{% else %}"
    "{% if verse_string.chords|length == 1 %}"
    "{{ verse_string.chords|join(' ', attribute='title') }} {{ verse_string.space_between_chords }}"
    "{% else %}"
    "{% for chord in verse_string.chords %}"
    "{% if loop.last %}"
    "{{ chord.title }} "
    "{% else %}"
    "{{ chord.title }} {{ verse_string.space_between_chords }}"
    "{% endif %}"
    "{% endfor %}"
    "{% endif %}"
    "{% endif %}"
    "{% if verse_string.end_chords %}"
    "{{ verse_string.end_chords|join(' ', attribute='title')}}"
    "{% endif %}"
    "\n\n{{ verse_string.lyrics }}\n"
    "{% else %}"
    "{{ verse_string.chords|join(' ', attribute='title')}}\n"
    "{% endif %}"
    "{% endfor %}"
    "{% endif %}"
    "{% endfor %}"
)

SONG_CHORDS_WITH_TABS_TEMPLATE = (
    Jinja("{% for chord in chords_tabs %}" "{{ chord.title }}:" "{{ chord.tab }}\n" "{% endfor %}")
    + SONG_CHORDS_WITHOUT_TABS_TEMPLATE
)

SONG_MENU = Jinja(
    "<b>{{ song.band.title }} - {{ song.title }}</b> ({{ song.hits_count }}"
    "{% if (song.hits_count|string)[-1:] == '1' %}"
    " просмотр)"
    "{% elif (song.hits_count|string)[-1:] in ['2','3','4'] %}"
    " просмотра)"
    "{% elif (song.hits_count|string)[-1:] in ['5','6','7','8','9','0'] %}"
    " просмотров)"
    "{% endif %}"
)
