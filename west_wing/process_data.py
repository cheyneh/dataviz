"""Tools to process script data into a dataframe."""

import os

import numpy as np
import pandas as pd

DATA_FOLDER = 'data'
_SCRIPTS_FOLDER = 'scripts'
SCRIPTS_FOLDER = os.path.join(DATA_FOLDER, _SCRIPTS_FOLDER)

LINES_TO_SKIP = ['FADE', 'CUT', 'ACT', 'MAN']

def get_ids():
    ids = []
    for fname in os.listdir(SCRIPTS_FOLDER):
        if not fname.startswith('script'):
            continue
        idnum = fname.lstrip('script_')
        idnum = idnum.rstrip('.txt')
        idnum = int(idnum)
        ids.append(idnum)
    return ids

def get_text(idnum):
    fname = 'script_{:03}.txt'.format(idnum)
    with open(os.path.join(SCRIPTS_FOLDER, fname), 'r') as f:
        text = f.read()
    return text


def get_character_counts(text):
    """Reads through a script, pulls out the character names and counts the
    number of lines each character has in that episode. This gets a little hacky
    to work with the script format."""

    # these dictionaries help to process the names
    str_mappings = {
            '[': '',
            ']': '',
            '.': ''
            }
    name_mappings = {
            'C.J.': 'CJ',
            'MRS BARTLETT': 'ABBEY'
            }
    def process_str(s):
        res = s
        for key in str_mappings:
            res = res.replace(key, str_mappings[key])
        return res

    paragraphs = text.split('\n\n')
    characters = []
    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        if len(lines) < 2:
            continue
        first_line = process_str(lines[0])
        if first_line.isupper():
            character = first_line.split()[0]
            if character.startswith('MR'):
                character = ' '.join(first_line.split()[:2])
        else:
            continue
        if character in name_mappings:
            character = name_mappings[character]
        characters.append(character)
    speaker_counts = {}
    for name in characters:
        if name in speaker_counts:
            speaker_counts[name] += 1
        else:
            speaker_counts[name] = 1
    return speaker_counts

def get_character_counts_o(text):
    paragraphs = text.split('\n\n')
    speakers = [p.split('\n')[0] for p in paragraphs]
    first_names = []
    for s in speakers:
        try:
            fn = s.split()[0]
            fn = fn.split("'")[0]
        except:
            continue
        if fn == 'C.J':
            fn = 'CJ'
        if fn.isupper():
            first_names.append(fn)
    speaker_counts = {}
    for name in first_names:
        if name in speaker_counts:
            speaker_counts[name] += 1
        else:
            speaker_counts[name] = 1
    return speaker_counts

def get_season_df():
    season_df = pd.read_csv(os.path.join(DATA_FOLDER, 'season_data.csv'),
            index_col=0)
    return season_df

def get_character_df():
    ids = get_ids()
    data = {}
    for idnum in ids:
        text = get_text(idnum)
        counts = get_character_counts(text)
        data[idnum] = counts
    df = pd.DataFrame(data)
    return df

def get_all_data():
    """Returns a data frame columns for each character and rows for each
    episode. Columns are sorted by total number of lines."""
    character_df = get_character_df().T
    season_df = get_season_df()
    df = character_df.join(season_df['season'], how='inner')
    df['episode'] = df.index
    df = df.set_index(['season', 'episode'], drop=True)

    total_counts = df.sum(axis=0).sort_values(ascending=False)
    total_counts = total_counts[~total_counts.index.isin(LINES_TO_SKIP)]
    df = df.loc[:, total_counts.index]
    df = df.fillna(0).astype(np.int)
    return df




