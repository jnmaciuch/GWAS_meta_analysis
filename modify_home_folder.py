import os
import pandas as pd
from pathlib import Path

# Define save location
home = str(Path.home())

path_to_settings = os.path.join(
    str(Path.home()), 'Documents', 'data_paths')

path_to_settings = os.path.join(
        path_to_settings,
        'allele_frequency.csv'
    )

# Load template
df = pd.read_csv("../allele_frequency_TEMPLATE.csv")

# Modify path
df.at[0, 'value'] = "/projects/p31982/allele_frequency" # CHANGE PATH NAME HERE
df.at[0, 'comment'] = "Updated " + f'{datetime.datetime.now():%Y-%m-%d}'

# Save file
df.to_csv(path_to_settings, index = False)