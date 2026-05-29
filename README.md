# Target-Group-Voter-Filter-
This script loads a large voter file, a list of target names (first and last), and an optional precinct‑to‑district mapping. It identifies voters whose first or last name matches any name in the target lists (flexible matching: first name can match a target first or last name, and same for last name). The resulting filtered data (with selected columns) is saved as a CSV.

Key features:

Cleans precinct numbers (removes trailing .1)

Uses set operations for fast name lookup

Flexible matching (cross‑checks first/last names against both name lists)

Merges with district mapping if available (handles missing columns gracefully)

Exports only the columns you specify

Use case:
Ideal for extracting specific demographic or community groups from a voter roll using a curated list of names. For example, identifying voters belonging to a particular ethnic, religious, or cultural group based on name lists.

Requirements:

Python 3.6+

pandas

Input files (adjust paths in the script):

voter_data.csv – Must contain Name First, Name Last, Precinct, and any other columns you wish to export.

target_names.csv – Must contain columns First Name and Last Name.

precincts_city_council_districts.csv (optional) – Used to add district information.

Output:

target_group_voters_filtered.csv – All rows from the voter file that match the target name lists, with only the selected columns.
