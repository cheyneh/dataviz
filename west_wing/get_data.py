
import os
import sys

import numpy as np
import pandas as pd

import requests
# from html.parser import HTMLParser
import bs4


DATA_FOLDER = 'data'
_SCRIPTS_FOLDER = 'scripts'
SCRIPTS_FOLDER = os.path.join(DATA_FOLDER, _SCRIPTS_FOLDER)


url = 'http://www.westwingtranscripts.com/search.php?flag=getTranscript&id={}'


def get_all_scripts(start_id=None, max_id=None):
    if start_id:
        script_id = start_id - 1
    else:
        script_id = 0  

    while True:
        script_id += 1
        if max_id and script_id > max_id:
            break
        print('getting {}'.format(script_id))

        resp = requests.get(url.format(script_id))
        if resp.status_code == 404:
            break

        decoded = resp.content.decode(errors='ignore')
        bs = bs4.BeautifulSoup(decoded, 'lxml')
        scripts = bs.find_all('pre')
        if len(scripts) > 1:
            print('more than one <pre> environment, skipping')
            continue
        elif len(scripts) < 1:
            print('no transcript for id: {}, skipping'.format(script_id))
            continue
        script = scripts[0]
        fname = 'script_{:03}.txt'.format(script_id)
        full_fname = os.path.join(SCRIPTS_FOLDER, fname)
        with open(full_fname, 'w') as f:
            f.write(script.text)

def organize_seasons():
    url = 'https://en.wikipedia.org/wiki/List_of_The_West_Wing_episodes'
    resp = requests.get(url)
    decoded = resp.content.decode(errors='ignore')
    soup = bs4.BeautifulSoup(decoded, 'lxml')
    episode_tables = soup.find_all(attrs={'class': 'wikiepisodetable'})
    data = {}
    for tbl_idx, tbl in enumerate(episode_tables):
        season = tbl_idx + 1
        rows = tbl.find_all('tr')
        for row_idx, row in enumerate(rows):
            if row_idx == 0:
                # if we're at the header, skip it
                continue
            first_cell = row.find('th')
            cells = row.find_all('td')
            # need some logic for the ones which have an hrule in the row (2
            # part episodes)
            if '\n' in first_cell.text:
                episode_numbers = first_cell.text.split('\n\n')
                try:
                    episode_num = [int(n) for n in episode_numbers]
                except:
                    print(first_cell.text)
                    raise
                # continue
            else:
                episode_num = int(first_cell.text)
            episode_data = {
                    'season'  : season,
                    'title'   : cells[1].text.strip('"'),
                    'director': cells[2].text,
                    'writer'  : cells[3].text
                    }
            if isinstance(episode_num, list):
                for num in episode_num:
                    data[num] = episode_data
            else:
                data[episode_num] = episode_data
    df = pd.DataFrame(data).T
    df.to_csv(os.path.join(DATAFOLDER, 'season_data.csv'))
    return df

def rename_files():
    for fname in os.listdir(SCRIPTS_FOLDER):
        if not fname.startswith('script_'):
            continue
        idnum = fname.lstrip('script_')
        idnum = idnum.rstrip('.txt')
        idnum = int(idnum)
        new_fname = 'script_{:03}.txt'.format(idnum)

        print('changing {} to {}'.format(fname, new_fname))
        with open(os.path.join(SCRIPTS_FOLDER, fname), 'r') as f:
            text = f.read()
        with open(os.path.join(SCRIPTS_FOLDER, new_fname), 'w') as f:
            f.write(text)
        os.remove(os.path.join(SCRIPTS_FOLDER, fname))

def main():
    if len(sys.argv) == 1:
        print('arguments can be {get_scripts, seasons, rename}')
    elif sys.argv[1] == 'get_scripts':
        get_all_scripts()
    elif sys.argv[1] == 'seasons':
        organize_seasons()
    elif sys.argv[1] == 'rename':
        rename_files()
    else:
        print('arg not recognized')


if __name__ == '__main__':
    main()




        


