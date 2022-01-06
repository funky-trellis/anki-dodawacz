# Copyright 2021 Gryzus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os.path

import src.anki_interface as anki
import src.commands as c
import src.ffmpeg_interface as ffmpeg
import src.help as h
from src.Dictionaries.ahdictionary import ask_ahdictionary
from src.Dictionaries.audio_dictionaries import ahd_audio, lexico_audio, diki_audio, save_audio_url
from src.Dictionaries.farlex import ask_farlex
from src.Dictionaries.lexico import ask_lexico
from src.Dictionaries.utils import hide, request_session
from src.Dictionaries.wordnet import ask_wordnet
from src.colors import R, BOLD, END, YEX, GEX, err_c
from src.data import config, command_to_help_dict, ROOT_DIR, LINUX
from src.input_fields import sentence_input

if LINUX:
    # "Enables command line editing using GNU readline."
    import readline
    readline.read_init_file()

__version__ = 'v1.4.2-2'

required_arg_commands = {
    # commands that take arguments
    '--delete-last': c.delete_cards, '--delete-recent': c.delete_cards,
    '-textwrap': c.set_text_value_commands,
    '-textwidth': c.set_width_settings,
    '-colviewat': c.set_width_settings,
    '-columns': c.set_width_settings,
    '-indent': c.set_width_settings,
    '-note': c.set_free_value_commands,
    '-deck': c.set_free_value_commands,
    '-tags': c.set_free_value_commands,
    '-hideas': c.set_free_value_commands,
    '--audio-path': c.set_audio_path, '-ap': c.set_audio_path,
    '-tsc': c.set_text_value_commands,
    '-dict': c.set_text_value_commands,
    '-dict2': c.set_text_value_commands,
    '-thes': c.set_text_value_commands,
    '-dupescope': c.set_text_value_commands,
    '-audio': c.set_text_value_commands,
    '-recqual': c.set_text_value_commands,
    '--add-note': anki.add_note_to_anki,
    '--field-order': c.change_field_order, '-fo': c.change_field_order,
    '-color': c.set_colors, '-c': c.set_colors,
    '-cd': c.config_defaults,
}
no_arg_commands = {
    '--audio-device': ffmpeg.set_audio_device,
    '-refresh': anki.refresh_cached_notes,
    '--help': h.quick_help, '-help': h.quick_help, '-h': h.quick_help,
    '--help-bulk': h.bulk_help, '--help-define-all': h.bulk_help,
    '--help-commands': h.commands_help, '--help-command': h.commands_help,
    '--help-config': h.commands_help, '--help-conf': h.commands_help,
    '--help-recording': h.recording_help, '--help-rec': h.recording_help,
    '-config': c.print_config_representation, '-conf': c.print_config_representation
}


def search_interface():
    while True:
        word = input('Search $ ').strip()
        if not word:
            continue

        args = word.split()
        cmd = args[0]
        if cmd in no_arg_commands:
            err = no_arg_commands[cmd]()
            if err is not None:
                print(f'{err_c}{err}')
            continue

        if cmd in tuple(command_to_help_dict)[:25]:
            method = c.boolean_commands
            message, usage = command_to_help_dict[cmd], '{on|off}'
        elif cmd in required_arg_commands:
            method = required_arg_commands[cmd]
            message, usage = command_to_help_dict[cmd]
        elif cmd in ('-b', '--browse'):
            anki.gui_browse_cards(query=args[1:])
            continue
        else:
            return word

        try:
            if args[1].strip('-').lower() in ('h', 'help'):
                raise IndexError
        except IndexError:  # Print help
            print(f'{YEX}{message}\n'
                  f'{R}{cmd} {usage}')

            # Print additional information
            if cmd in ('-ap', '--audio-path'):
                print(f'{BOLD}Current audio path:\n'
                      f'{END}{config["audio_path"]}\n')
            elif cmd == '--add-note':
                anki.show_available_notes()
            elif cmd in ('-fo', '--field-order'):
                c._display_field_order()
            elif cmd in ('-c', '-color'):
                c.color_command()
            elif cmd == '-cd':
                print(f'{BOLD}Field names:{END}\n'
                      f'def, exsen, pos, etym, syn, all\n')
        else:
            err = method(*args, message=message)
            if err is not None:
                print(f'{err_c}{err}')


def manage_audio(dictionary_name, audio_url, phrase, flags):
    def from_diki():
        flag = ''
        for f in flags:
            if f in ('n', 'v', 'a', 'adj', 'noun', 'verb', 'adjective'):
                flag = '-' + f[0]
                break
        url = diki_audio(phrase, flag)
        return save_audio_url(url) if url else ''

    server = config['audio']
    if server == '-':
        return ''

    # Farlex has no audio, so we try to get it from diki.
    if server == 'diki' or dictionary_name == 'farlex':
        return from_diki()

    if server == 'auto' or dictionary_name == server:
        if audio_url:
            return save_audio_url(audio_url)
        print(f'{err_c}The dictionary does not have the pronunciation for {R}{phrase}\n'
              f'{YEX}Querying diki...')
        return from_diki()

    if server == 'ahd':
        audio_url = ahd_audio(phrase)
    elif server == 'lexico':
        audio_url = lexico_audio(phrase)
    else:
        assert False, 'unreachable'

    if audio_url:
        return save_audio_url(audio_url)
    return ''


def save_card_to_file(field_values):
    with open('cards.txt', 'a', encoding='utf-8') as f:
        f.write('\t'.join(field_values[field] for field in config['fieldorder']) + '\n')
    print(f'{GEX}Card successfully saved to a file\n')


def manage_dictionaries(_phrase, flags):
    first_dicts = {
        'ahd': ask_ahdictionary,
        'lexico': ask_lexico, 'l': ask_lexico,
        'idioms': ask_farlex, 'idiom': ask_farlex, 'i': ask_farlex
    }

    dict_flags = []
    for f in flags:
        if f in first_dicts:
            dict_flags.append(f)

    if dict_flags:
        dictionary = None
        for flag in dict_flags:
            dictionary = first_dicts[flag](_phrase, flags=flags)
            # If we don't break out of the for loop, we can query multiple
            # dictionaries by specifying more than one dictionary flag
            if dictionary is not None:
                dictionary.show()
        return dictionary
    else:
        dictionary = first_dicts[config['dict']](_phrase, flags=flags)
        if dictionary is not None:
            dictionary.show()
            return dictionary

    # fallback dictionary section
    if config['dict2'] == '-':
        return None

    second_dicts = {
        'ahd': ask_ahdictionary,
        'lexico': ask_lexico,
        'idioms': ask_farlex
    }
    print(f'{YEX}Querying the fallback dictionary...')
    dictionary = second_dicts[config['dict2']](_phrase, flags=flags)
    if dictionary is not None:
        dictionary.show()
        return dictionary
    if config['dict'] != 'idioms' and config['dict2'] != 'idioms':
        print(f"{YEX}To ask the idioms dictionary use {R}`{_phrase} -i`")


def format_definitions(definitions):
    styles = (
        ('', ''),
        ('<span style="opacity: .6;">', '</span>'),
        ('<small style="opacity: .4;">', '</small>'),
        ('<small style="opacity: .2;"><sub>', '</sub></small>')
    )
    formatted = []
    style_no = len(styles)
    for i, item in enumerate(definitions.split('<br>'), start=1):
        style_i = style_no - 1 if i > style_no else i - 1
        prefix, suffix = styles[style_i]

        prefix += f'<small style="color: #4EAA72;">{i}.</small>  '
        formatted.append(prefix + item + suffix)

    return '<br>'.join(formatted)


def main_loop(query):
    field_values = {
        'def': '',
        'syn': '',
        'exsen': '',
        'phrase': '',
        'pz': '',
        'pos': '',
        'etym': '',
        'audio': '',
        'recording': '',
        '-': '',
    }

    dict_query, *flags = query.split(' -')
    flags = [x.strip('-') for x in flags]

    if dict_query in ('-rec', '--record'):
        ffmpeg.capture_audio()
        return

    if '<' in dict_query and '>' in dict_query:
        searched_phrase = dict_query.split('<', 1)[-1].rsplit('>', 1)[0]
        if not searched_phrase:
            return
        zdanie = dict_query
    else:
        searched_phrase, zdanie = dict_query, ''

    if 'rec' in flags or 'record' in flags:
        field_values['recording'] = ffmpeg.capture_audio(searched_phrase)

    dictionary = manage_dictionaries(searched_phrase, flags)
    if dictionary is None:
        return

    if not config['createcards']:
        # Use the first phrase to always make the correct query.
        # e.g. preferred -> prefer
        t = ask_wordnet(dictionary.phrases[0])
        if t is not None:
            t.show()
        return

    if not zdanie:  # if sentence wasn't passed as a query
        zdanie = sentence_input()
        if zdanie is None:
            return

    dictionary_contents = dictionary.input_cycle()
    if dictionary_contents is None:
        return
    field_values.update(dictionary_contents)

    phrase = field_values['phrase']
    if dictionary.allow_thesaurus:
        thesaurus = ask_wordnet(
            phrase.split()[0] if 'also' in phrase.split() else phrase
        )
        if thesaurus is not None:
            thesaurus.show()
            thesaurus_contents = thesaurus.input_cycle()
            if thesaurus_contents is None:
                return
            field_values.update(thesaurus_contents)

    field_values['audio'] = manage_audio(dictionary.name,
                                         field_values['audio'],
                                         phrase,
                                         flags)
    # Format card content.
    if zdanie:
        field_values['pz'] = zdanie
    else:
        if config['tsc'] != '-':
            if field_values['exsen']:
                field_values['pz'] = field_values['exsen']
                field_values['exsen'] = ''
            else:
                if config['tsc'] == 'strict':
                    field_values['pz'] = phrase
                    field_values['phrase'] = ''

    # hide phrase in content
    for elem in ('pz', 'def', 'exsen', 'syn'):
        content = field_values[elem]
        if content and config[f'u{elem}']:
            field_values[elem] = hide(content, phrase)

    if config['cardpreview']:
        dictionary.display_card(field_values)

    # format card content
    for key, val in field_values.items():
        field_values[key] = val.replace("'", "&#39;").replace('"', '&quot;')

    if config['formatdefs']:
        field_values['def'] = format_definitions(field_values['def'])
    if '<br>' not in field_values['pz']:
        field_values['pz'] = field_values['pz'] \
            .replace('>', '</b>').replace('<', '<b style="color: #91cb7d;">', 1)

    print()
    if config['ankiconnect']:
        anki.add_card_to_anki(field_values)
    if config['savecards']:
        save_card_to_file(field_values)


def main():
    if config['audio_path'] == 'Cards_audio':
        # Providing the absolute path solves an occasional PermissionError on Windows.
        t = os.path.join(ROOT_DIR, 'Cards_audio')
        if not os.path.exists(t):
            os.mkdir(t)

    print(f'{BOLD}- Anki card generator {__version__} -{END}\n'
          'type `-h` for usage and configuration\n\n')

    while True:
        users_query = search_interface()
        if not users_query.startswith('--define-all'):
            main_loop(users_query)
            continue

        # Search for the "define_all" like file.
        for file in os.listdir():
            file = file.lower()
            if file.startswith('define') and 'all' in file:
                define_file = file
                break
        else:
            print(f'{err_c}Could not find {R}"define_all.txt"{err_c} file.\n'
                  f'Create one and paste your list of queries there.')
            continue

        _, _, sep = users_query.partition(' ')
        sep = sep.strip()
        if not sep:
            sep = '\n'

        with open(define_file, 'r') as f:
            lines = [x.strip().strip(sep) for x in f if x.strip().strip(sep)]

        if not lines:
            print(f'{R}"{define_file}"{err_c} file is empty.')
            continue

        for line in lines:
            for query in line.split(sep):
                query = query.strip()
                if query:
                    main_loop(query)

        print(f'{YEX}** {R}"{define_file}"{YEX} has been exhausted **\n')


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        request_session.close()
