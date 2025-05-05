#!/usr/bin/env python3
"""
Congressional Contact List Generator

This script pulls data from the unitedstates/congress-legislators repository
and creates a CSV file with contact information for all current members of Congress,
organized by state (alphabetically) and then by district number.

Columns: State, name, party, district, phone, url
"""

import csv
import os
import sys
import yaml
import requests
from collections import defaultdict

def download_yaml_file(url, local_filename=None):
    """Download a YAML file from GitHub."""
    if local_filename is None:
        local_filename = url.split('/')[-1]
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-200 status codes
        
        with open(local_filename, 'wb') as f:
            f.write(response.content)
        
        return local_filename
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)

def load_yaml_data(filename):
    """Load data from a YAML file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data
    except (yaml.YAMLError, IOError) as e:
        print(f"Error loading YAML file: {e}")
        sys.exit(1)

def get_state_name(state_abbr):
    """Convert state abbreviation to full state name."""
    state_names = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
        'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
        'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
        'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
        'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
        'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
        'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
        'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
        'DC': 'District of Columbia', 'PR': 'Puerto Rico', 'AS': 'American Samoa', 'GU': 'Guam',
        'MP': 'Northern Mariana Islands', 'VI': 'U.S. Virgin Islands'
    }
    return state_names.get(state_abbr, state_abbr)

def district_sort_key(district_info):
    """Create a sorting key for districts to ensure proper ordering."""
    state, member = district_info
    if member['district'] == 'Senate':
        # Place senators after representatives
        return (state, 999)
    try:
        # Extract the district number from district format like "CA-01"
        district_num = int(member['district'].split('-')[1])
        return (state, district_num)
    except (IndexError, ValueError):
        # Handle special cases like "AL-AL" (at-large)
        return (state, 0)

def process_legislators_data(current_legislators, legislators_social_media=None):
    """Process legislators data into the format needed for the CSV."""
    members_by_state = defaultdict(list)
    
    # Create a lookup for social media info if available
    social_media_lookup = {}
    if legislators_social_media:
        for entry in legislators_social_media:
            bioguide_id = entry.get('id', {}).get('bioguide')
            if bioguide_id:
                social_media = entry.get('social', {})
                social_media_lookup[bioguide_id] = social_media
    
    for legislator in current_legislators:
        # Skip if no term information
        if 'terms' not in legislator:
            continue
        
        # Get the current/most recent term
        current_term = legislator['terms'][-1]
        
        # Only include current legislators
        if 'end' in current_term and current_term['end'] < '2025-01-01':
            continue
        
        # Get legislator's name
        first_name = legislator.get('name', {}).get('first', '')
        last_name = legislator.get('name', {}).get('last', '')
        name = f"{first_name} {last_name}"
        
        # Get state information
        state_abbr = current_term.get('state')
        state = get_state_name(state_abbr)
        
        # Get party
        party = current_term.get('party', '')
        if party == 'Republican':
            party = 'R'
        elif party == 'Democrat':
            party = 'D'
        elif party == 'Independent':
            party = 'I'
        
        # Get district information
        term_type = current_term.get('type')
        if term_type == 'sen':
            district = 'Senate'
        elif term_type == 'rep':
            district_num = current_term.get('district')
            if district_num == 0:
                district = f"{state_abbr}-AL"  # At-large district
            else:
                district = f"{state_abbr}-{district_num:02d}"
        else:
            district = ''
        
        # Get contact information
        phone = current_term.get('phone', '')
        url = current_term.get('url', '')
        
        # Get social media information if available
        twitter = ''
        facebook = ''
        youtube = ''
        instagram = ''
        
        # Get bioguide_id for social media lookup
        bioguide_id = legislator.get('id', {}).get('bioguide')
        if bioguide_id and bioguide_id in social_media_lookup:
            social = social_media_lookup[bioguide_id]
            twitter = social.get('twitter', '')
            facebook = social.get('facebook', '')
            youtube = social.get('youtube', '')
            instagram = social.get('instagram', '')
        
        # Create member entry
        member = {
            'State': state,
            'name': name,
            'party': party,
            'district': district,
            'phone': phone,
            'url': url,
            'twitter': twitter,
            'facebook': facebook,
            'youtube': youtube,
            'instagram': instagram
        }
        
        members_by_state[state].append(member)
    
    # Sort entries by state name alphabetically, then by district number
    sorted_members = []
    for state in sorted(members_by_state.keys()):
        # Sort representatives by district number, then add senators
        state_members = sorted(
            [(state, member) for member in members_by_state[state]],
            key=district_sort_key
        )
        sorted_members.extend([member for _, member in state_members])
    
    return sorted_members

def write_csv(members, output_file='congressional_contacts.csv'):
    """Write the processed data to a CSV file."""
    fieldnames = ['State', 'name', 'party', 'district', 'phone', 'url', 
                 'twitter', 'facebook', 'youtube', 'instagram']
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(members)
        
        print(f"Successfully created {output_file} with {len(members)} entries")
        return True
    except IOError as e:
        print(f"Error writing CSV file: {e}")
        return False

def main():
    print("Downloading and processing data from unitedstates/congress-legislators...")
    
    # URLs for the data files
    current_legislators_url = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/main/legislators-current.yaml'
    social_media_url = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/main/legislators-social-media.yaml'
    
    # Download data files
    current_legislators_file = download_yaml_file(current_legislators_url)
    social_media_file = download_yaml_file(social_media_url)
    
    # Load data
    current_legislators = load_yaml_data(current_legislators_file)
    social_media = load_yaml_data(social_media_file)
    
    # Process data
    members = process_legislators_data(current_legislators, social_media)
    
    # Write to CSV
    write_csv(members)
    
    # Clean up downloaded files
    os.remove(current_legislators_file)
    os.remove(social_media_file)

if __name__ == "__main__":
    main()
