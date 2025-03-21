import pandas as pd

from manuscript import inout

def gwas_catalog(table):
    """
    Load and process GWAS catalog data.
    Parameters:
    table (str): The type of GWAS catalog data to load. Must be one of 'associations' or 'studies'.
    Returns:
    pd.DataFrame: A pandas DataFrame containing the processed GWAS catalog data.
    Raises:
    ValueError: If the provided table is not in the allowed list ['associations', 'studies'].
    The function performs the following steps:
    - Reads the GWAS catalog data from a specified internal path.
    - Renames the 'PUBMEDID' column to 'pubmed_id'.
    - Converts column names to lowercase.
    - Converts specific columns to appropriate data types (int, float, str).
    - Replaces hyphens in column names with underscores.
    """

    allowed = ['associations', 'studies']
    if table not in allowed:
        raise ValueError('Table not in allowed list: {}'.format(allowed))
    
    if table == 'associations':
        p = inout.get_internal_path('data/resources/ebi/gwas_catalog/2025-01-08/full/gwas_catalog_v1.0.2-associations_e113_r2025-01-08.tsv')
        df = pd.read_csv(p, sep='\t', low_memory=False)
        df = df.rename(columns={'PUBMEDID': 'pubmed_id'})
        df = _lower_captions(df)
        df.columns = [x.replace(' ', '_') for x in df.columns]
        as_int = ['pubmed_id']
        as_float = ['upstream_gene_distance', 'downstream_gene_distance', 'p-value', 'pvalue_mlog', 
                    'or_or_beta', 'intergenic', 'merged']
        as_numbers = as_int + as_float
        df.loc[:, as_int] = df.loc[:, as_int].astype(int)
        df.loc[:, as_float] = df.loc[:, as_float].astype(float)
        as_string = [x for x in df.columns if x not in as_numbers]
        df.loc[:, as_string] = df.loc[:, as_string].astype(str)
        df.columns = df.columns.str.replace('-', '_')

    elif table == 'studies':
        p = inout.get_internal_path('data/resources/ebi/gwas_catalog/2025-01-08/studies/gwas-catalog-v1.0.3.1-studies-r2025-01-08.tsv')
        df = pd.read_csv(p, sep='\t', low_memory=False)
        df = df.rename(columns={'PUBMEDID': 'pubmed_id'})
        df = _lower_captions(df)
        df.columns = [x.replace(' ', '_') for x in df.columns]
        as_numbers = [
            'pubmed_id', 'association_count',
        ]
        df.loc[:, as_numbers] = df.loc[:, as_numbers].astype(int)
        as_string = [x for x in df.columns if x not in as_numbers]
        df.loc[:, as_string] = df.loc[:, as_string].astype(str)
        df.columns = df.columns.str.replace('-', '_')

    return df

def _lower_captions(df):
    df.columns = [x.lower() for x in df.columns]
    return df

def pubmed_searchlist(table):
    """
    Load and process pubmed results from advanced search (pubmed ID output).
    Parameters:
    table (str): Which pubmed list to load. Must be one of 'CCDG' or 'CMG'.
    Returns:
    pd.DataFrame: A pandas DataFrame containing a list of pubmed IDs.
    Raises:
    ValueError: If the provided table is not in the allowed list ['CCDG', 'CMG'].
    The function performs the following steps:
    - Reads the pubmed data csv from a specified internal path.
    - Creates a "pubmed_id" column name
    """

    allowed = ['CCDG', 'CMG']
    if table not in allowed:
        raise ValueError('Table not in allowed list: {}'.format(allowed))
    
    if table == 'CCDG':
        p = inout.get_internal_path('data/resources/affiliations/pmid_Centers_for_Common_Disease_Genomics.txt')
        df = pd.read_csv(p, low_memory=False, header=None)
        df.columns = ['pubmed_id']

    elif table == 'CMG':
        p = inout.get_internal_path('data/resources/affiliations/pmid_Centers_for_Mendelian_Genomics.txt')
        df = pd.read_csv(p, low_memory=False, header=None)
        df.columns = ['pubmed_id']

    return df