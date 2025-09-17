import pandas as pd
import numpy as np

from place_name_mappings import arrond_names, prov_names, region_names, prov_to_region

def preproc_sheet(df_sheet:pd.DataFrame):
    cats_immobilière  = df_sheet.iloc[0].dropna().values
    df_sheet         = df_sheet.drop(0)
    df_sheet.columns = df_sheet.iloc[0]
    df_sheet.columns.name = ""
    
    df_sheet.drop(columns=[0.0], inplace=True)
    df_sheet=df_sheet.drop(1).reset_index(drop=True)
    
    df_sheet = df_sheet.iloc[:,:25]

    nan_positions =  [i for i, col in enumerate(df_sheet.columns) if pd.isna(col)]
    
    df0 = df_sheet.iloc[:, 0:nan_positions[0]]
    dfs = []

    cat_map = {"Toutes les maisons avec 2, 3, 4 ou plus de façades (excl. appartements)": "all_houses",
               "Maisons avec 2 ou 3 façades (type fermé + type demi-fermé)": "attached_houses", 
               'Maisons avec 4 ou plus de façades (type ouvert)': "detached_houses",
               "Appartements": "Appartment",
               "Alle huizen met 2, 3, 4 of meer gevels (excl. appartementen)": "all_houses",
               "Huizen met 2 of 3 gevels (gesloten + halfopen bebouwing)":"attached_houses",
               "Huizen met 4 of meer gevels (open bebouwing)": "detached_houses", 
               "Appartementen": "Appartment"
               }

    for i in range(len(nan_positions) -1):
        df = pd.concat( [ df0 , df_sheet.iloc[:, nan_positions[i]+1:nan_positions[i+1]  ] ], axis=1 ) 
        df["category"] = cats_immobilière[i] #i
        df.category= df.category.map(cat_map)
        df.columns = ["refnis", "commune", "year", "period", "n_trans", "q2", "q1", "q3", "category"]

        df.refnis = df.refnis.astype(np.int32)
        df.year   = df.year.astype(np.int32)

        dfs.append(df)

    return dfs 

def get_wide_df(dfs):
    """
    category reference: {0: "all_houses", 1: "attached_houses", 2:"detached_houses",3:"Appartment"}
    
    """
    for i in range(4):
        dfs[i].columns = ['refnis', 'commune', 'year', 'period', f'n_{i}', f'q2_{i}', f'q1_{i}', f'q3_{i}', f'cat_{i}']
    
    parallel_df = pd.concat( dfs, axis=1)
    parallel_df = parallel_df.loc[:, ~parallel_df.columns.duplicated()].copy()
    parallel_df.drop(["cat_0","cat_1","cat_2","cat_3"],axis=1,inplace=True)

    parallel_df.n_1 = parallel_df.n_1.apply(lambda x: 0 if pd.isna(x) else x)
    parallel_df.n_2 = parallel_df.n_2.apply(lambda x: 0 if pd.isna(x) else x)
    parallel_df.n_0 = parallel_df.n_0.apply(lambda x: 0 if pd.isna(x) else x)
    parallel_df.n_3 = parallel_df.n_3.apply(lambda x: 0 if pd.isna(x) else x)

    return parallel_df


def get_ref_df(filename:str, sheet_name:str):
    excell_df   = pd.read_excel(filename, sheet_name = sheet_name)
    dfs         = preproc_sheet(excell_df)
    ref_df      = get_wide_df(dfs)
    return ref_df


def refnis_to_arrondissment(x: int):
    """
    To be used like: 
    df["arrond"] = df["refnis"].apply(refnis_to_arrondissment)
    """
    return int(str(x)[:2]) 

def get_arrondissement_from_code(code: int):
    return arrond_names[code]
    
def arrond_to_prov(arrond: int):
    if arrond < 20 or arrond >= 30:
        return int(str(arrond)[0]+ "0000")
    if arrond == 21:
        return 0
    if arrond in [23, 24]:
        return 20001
    if arrond == 25:
        return 20002

