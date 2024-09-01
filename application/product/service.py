import pandas as pd

def clean_data(df):
    """for cleaning the product data """

    # Fill missing values
    df['price'].fillna(df['price'].median(), inplace=True)
    df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)
    df['rating'].fillna(df.groupby('category')['rating'].transform('mean'), inplace=True)

    # Ensure numeric columns are indeed numeric
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

    return df
