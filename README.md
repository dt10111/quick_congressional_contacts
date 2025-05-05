# quick_congressional_contacts
Quick Congressional Contacts

# Congressional Contact List Generator

A Python script that generates a comprehensive CSV file containing contact information and social media accounts for all current members of the United States Congress.

## Description

This script fetches data from the [unitedstates/congress-legislators](https://github.com/unitedstates/congress-legislators) repository to create an up-to-date list of all current members of Congress, including both the House of Representatives and the Senate. The output is a CSV file with contact information and social media accounts, organized by state (alphabetically) and then by district number.

The CSV includes the following data for each member:
- State (full state name)
- Name (first and last name)
- Party (R, D, or I)
- District (formatted as "XX-##" or "Senate" for senators)
- Phone (Washington DC office number)
- Official website URL
- Official Twitter account
- Official Facebook page
- Official YouTube channel
- Official Instagram account

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - `pyyaml`
  - `requests`

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/congressional-contact-list.git
   cd congressional-contact-list
   ```

2. Install the required packages:
   ```
   pip install pyyaml requests
   ```

## Usage

Run the script to generate the CSV file:

```
python generate_congress_contacts.py
```

The script will:
1. Download the latest data from the unitedstates/congress-legislators repository
2. Process the data to extract the required information
3. Sort the data as specified
4. Create a file named `congressional_contacts.csv` in the current directory

## Example Output

The resulting CSV file will look something like this:

```
State,name,party,district,phone,url,twitter,facebook,youtube,instagram
Alabama,Jerry Carl,R,AL-01,202-225-4931,https://carl.house.gov,RepJerryCarl,RepJerryCarl,UCITAoePHh8NuV0COrAGvQiQ,repjerrycarl
Alabama,Barry Moore,R,AL-02,202-225-2901,https://barrymoore.house.gov,RepBarryMoore,RepBarryMoore,UCR18VNXMBswmRFwlBzCnRLw,repbarrymoore
...
Wyoming,Cynthia Lummis,R,Senate,202-224-3424,https://www.lummis.senate.gov,SenLummis,SenLummis,UCMHUJol05Y4keNxZ2UlcZBQ,senlummis
```

## Data Source

All data is sourced from the [unitedstates/congress-legislators](https://github.com/unitedstates/congress-legislators) project, which is dedicated to providing comprehensive information about the United States Congress in YAML, JSON, and CSV formats.

The project provides the following data files that are used by this script:
- `legislators-current.yaml`: Information about current members of Congress
- `legislators-social-media.yaml`: Official social media accounts for members of Congress

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the [unitedstates/congress-legislators](https://github.com/unitedstates/congress-legislators) project for providing the data in an accessible format.
- The social media information includes only official accounts used for legislative work, not personal or campaign accounts.
