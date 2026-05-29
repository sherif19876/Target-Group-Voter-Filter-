import pandas as pd

# ----------------------------------------------------------------------
# Configuration - adjust file paths and column names as needed
# ----------------------------------------------------------------------
VOTER_FILE = "voter_data.csv"                        # Main voter file
TARGET_NAMES_FILE = "target_names.csv"               # CSV with 'First Name' and 'Last Name' columns
DISTRICTS_FILE = "precincts_city_council_districts.csv"  # Precinct to district mapping
OUTPUT_FILE = "target_group_voters_filtered.csv"     # Output for matched voters

# Voter file expected columns: 'Name First', 'Name Last', 'Precinct', plus others
# ----------------------------------------------------------------------

def load_voter_file(file_path):
    """Load voter CSV, clean column names, and clean precinct numbers."""
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    df.columns = df.columns.str.strip()               # Remove leading/trailing spaces
    # Remove trailing .1 from precinct numbers (e.g., "304.1" -> "304")
    df['Precinct'] = df['Precinct'].astype(str).str.replace(r'\.1$', '', regex=True)
    return df

def load_target_names(file_path):
    """
    Load CSV containing target names.
    Expected columns: 'First Name', 'Last Name'
    Returns two sets: first names and last names (stripped, non‑empty).
    """
    df = pd.read_csv(file_path, encoding='cp1252')
    first_names = set(df['First Name'].dropna().astype(str).str.strip())
    last_names = set(df['Last Name'].dropna().astype(str).str.strip())
    return first_names, last_names

def load_districts(file_path):
    """Load precinct‑to‑district mapping and ensure Precinct is string."""
    df = pd.read_csv(file_path)
    df['Precinct'] = df['Precinct'].astype(str)
    return df

def is_target_voter(row, first_set, last_set):
    """
    Determine if a voter matches any name in the target lists.
    Checks first name against both first‑name and last‑name sets,
    and similarly for last name.
    """
    first = str(row.get('Name First', '')).strip()
    last = str(row.get('Name Last', '')).strip()
    return (
        (first in first_set) or
        (first in last_set) or
        (last in first_set) or
        (last in last_set)
    )

def main():
    print("Loading voter file...")
    voters_df = load_voter_file(VOTER_FILE)
    print(f"  Loaded {len(voters_df)} voters")

    print("Loading target names...")
    first_set, last_set = load_target_names(TARGET_NAMES_FILE)
    print(f"  Loaded {len(first_set)} unique first names, {len(last_set)} unique last names")

    print("Loading district mapping...")
    districts_df = load_districts(DISTRICTS_FILE)
    print(f"  Loaded {len(districts_df)} precinct mappings")

    # Filter voters who match the target name lists
    print("Filtering voters...")
    mask = voters_df.apply(lambda row: is_target_voter(row, first_set, last_set), axis=1)
    target_voters = voters_df[mask]
    print(f"  Found {len(target_voters)} matching voters")

    # Merge with districts to add district columns (optional)
    target_voters_with_districts = pd.merge(target_voters, districts_df, on='Precinct', how='left')

    # Define the columns you want to keep in the output
    # (adjust this list based on your actual voter file columns)
    fields = [
        "Voter ID", 'Name Last', 'Name Suffix', 'Name First', 'Name Middle',
        'Requested public records exemption', 'Residence Address Line 1', 'Residence Address Line 2',
        'Residence City (USPS)', 'Residence State', 'Residence Zipcode', 'Mailing Address Line 1',
        'Mailing Address Line 2', 'Mailing Address Line 3', 'Mailing City', 'Mailing State',
        'Mailing Zipcode', 'Mailing Country', 'Gender', 'Race', 'Birth Date', 'Registration Date',
        'Party Affiliation', 'Precinct', 'Precinct Group', 'Precinct Split', 'Precinct Suffix',
        'Voter Status', 'Congressional District', 'House District', 'Senate District',
        'County Commission District', 'School Board District'
    ]
    # Keep only columns that actually exist in the merged DataFrame
    existing_fields = [col for col in fields if col in target_voters_with_districts.columns]

    # Export filtered data
    target_voters_filtered = target_voters_with_districts[existing_fields]
    target_voters_filtered.to_csv(OUTPUT_FILE, index=False)
    print(f"\nFiltered data exported to '{OUTPUT_FILE}'")

    # Optional: show sample of first/last names for debugging
    print("\nSample of first names from target list:", list(first_set)[:5])
    print("Sample of last names from target list:", list(last_set)[:5])

if __name__ == "__main__":
    main()
