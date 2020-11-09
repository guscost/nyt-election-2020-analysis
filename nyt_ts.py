import pandas as pd
import pprint
import requests
 
def collapse_results_by_party(results_by_candidate, candidates):
    results_by_party = {}
    for candidate, count in iter(results_by_candidate.items()):
        party = candidates[candidate]['party']
        results_by_party[party] = results_by_party.get(party, 0) + count
 
    return results_by_party
 
states = [
 'Alaska', 'Alabama', 'Arkansas', 'Arizona', 'California', 'Colorado',
 'Connecticut', 'Delaware', 'Florida', 'Georgia',
 'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana', 'Kansas', 'Kentucky',
 'Louisiana', 'Massachusetts', 'Maryland', 'Maine', 'Michigan',
 'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North Carolina',
 'North Dakota', 'Nebraska', 'New Hampshire', 'New Jersey', 'New Mexico',
 'Nevada', 'New York', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
 'Utah', 'Virginia', 'Vermont', 'Washington', 'Wisconsin',
 'West Virginia', 'Wyoming',
]
 
all_results = {}
for state in states:
    print(f'Downloading {state}')
    formatted_state = state.lower().replace(' ', '-')

    # Scrape data for this state and store as a dict
    state_response = requests.get(f'https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/race-page/{formatted_state}/president.json')    
    all_results[formatted_state] = state_response.json()
    
    # Archive the response JSON too
    with open(f'scrapes/{formatted_state}.json', 'wb') as f:
        f.write(state_response.content)

# python3-ported but otherwise basically verbatim from 
# https://threadreaderapp.com/thread/1325592112428163072.html
records = []
for state, state_results in iter(all_results.items()):
    race = state_results['data']['races'][0]
 
    for candidate in race['candidates']:
        if candidate['party_id'] == 'republican':
            candidate['party'] = 'rep'
        elif candidate['party_id'] == 'democrat':
            candidate['party'] = 'dem'
        else:
            candidate['party'] = 'trd'
    candidates = { candidate['candidate_key']: candidate for candidate in race['candidates'] }
 
    for data_point in race['timeseries']:
        data_point['state']             = state
        data_point['expected_votes']    = race['tot_exp_vote']
        data_point['trump2016']         = race['trump2016']
        data_point['votes2012']         = race['votes2012']
        data_point['votes2016']         = race['votes2016']
 
        vote_shares = collapse_results_by_party(data_point['vote_shares'], candidates)
        for party in ['rep', 'dem', 'trd']:
            data_point['vote_share_{}'.format(party)] = vote_shares.get(party, 0)
 
        data_point.pop('vote_shares')
        records.append(data_point)
 
time_series_df = pd.DataFrame.from_records(records)
time_series_df.to_csv('output/nyt_ts.csv', encoding='utf-8')
