
import os
import sys
import datetime
import json

import requests
import bs4

from config import CONFIG

SEASON = CONFIG['season']
RUNDLE = CONFIG['season']
url_template = 'https://learnedleague.com/match.php?{}&{}&{}'
day_url = url_template.format(SEASON, '{}',  RUNDLE)


def parse_match_day(day=1):

    def get_match_table():
        url = day_url.format(day)
        resp = requests.get(url)

        assert resp.status_code == 200
        html = resp.content.decode(errors='ignore')
        soup = bs4.BeautifulSoup(html, 'lxml')

        tables = soup.find_all('table')
        is_data_table = lambda t: ('summary' in t.attrs 
                and t.attrs['summary'].startswith('Data table'))

        data_table = [t for t in tables if is_data_table(t)][0]
        return data_table

    def parse_table(t):
        # data_dict = {}
        data_list = []
        rows = data_table.find_all('tr')
        header = rows[0]
        # skip the header and the last three data rows
        for row in rows[1: -3]:
            data = {}
            cells = row.find_all('td')
            pts_results = cells[:6]
            points = [int(c.text) for c in pts_results]
            def get_result(c):
                mapping = {'c1': 'Correct', 'c0': 'Wrong', 'cF': 'Forfeit'}
                cls = c.attrs['class'][0]
                return mapping[cls]
            results = [get_result(c) for c in pts_results]
            for idx, q_num in enumerate(range(1, 7)):
                data[f'points_{q_num}'] = points[idx]
                data[f'result_{q_num}'] = results[idx]

            data['rank'] = int(cells[6].findChild().text)
            data['wins'] = int(cells[8].text)
            data['losses'] = int(cells[9].text)
            data['ties'] = int(cells[10].text)
            data['points'] = int(cells[11].text)
            data['mpd'] = int(cells[12].text)
            data['tmp'] = int(cells[13].text)
            data['tca'] = int(cells[14].text)
            data['de'] = float(cells[15].text)
            data['fl'] = int(cells[16].text)
            data['3pt'] = int(cells[17].text)

            username = cells[7].text.strip()
            data['username'] = username

            data_list.append(data)
        return data_list

    data_table = get_match_table()
    parsed_data = parse_table(data_table)
    return parsed_data

def get_all_data():
    # uses a list since json can't handle numerics as keys
    all_data = []
    for day in range(1, 26):
        print(day)
        data = parse_match_day(day=day)
        all_data.append(data)
    return all_data

def save_data(data, fname=f'data_LL{SEASON}.json'):
    full_fname = os.path.join('data', fname)
    with open(full_fname, 'w') as f:
        json.dump(data, f)

def load_data():
    fname = f'data_LL{SEASON}.json'
    full_fname = os.path.join('data', fname)
    with open(full_fname, 'r') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    all_data = get_all_data()
    save_data(all_data)





