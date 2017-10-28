"""Tools to process script data into a dataframe."""

import os

import numpy as np
import pandas as pd

def get_ids():
    ids = []
    for fname in os.listdir('data'):
        if not fname.startswith('script'):
            continue
        idnum = fname.lstrip('script_')
        idnum = idnum.rstrip('.txt')
        idnum = int(idnum)
        ids.append(idnum)
    return ids

def get_text(idnum):
    fname = 'script_{:03}.txt'.format(idnum)
    with open(os.path.join('data', fname), 'r') as f:
        text = f.read()
    return text

def character_counts(text):
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

def character_df():
    ids = get_ids()
    data = {}
    for idnum in ids:
        text = get_text(idnum)
        counts = character_counts(text)
        data[idnum] = counts
    df = pd.DataFrame(data)
    return df
