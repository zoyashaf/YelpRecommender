import pandas as pd

"""
Function: Process_user 
Input: user_data, a dataframe containing all the businesses a single user has reviewed
Output: pivot_dict, a dictionary form of the pivoted_df, which is a dataframe containing one row (user_id) with N columns where
        N is the number of restaurants the user has reviewed. The value is the average star rating given by that user for that restuarant 
"""

def process_user(user_data):

    user = user_data['user_id'].iat[0]
    subset = user_data.drop_duplicates(['business_id', 'stars'], keep='first').reset_index()
    grouped_df = subset.groupby('business_id', as_index=False)['stars'].mean()
    grouped_df['user_id'] = user
    pivoted_df = pd.pivot(grouped_df, index='user_id', columns='business_id', values='stars')
    pivoted_df['user_id'] = user

    pivot_dict = pivoted_df.to_dict(orient='records')[0]
   
    
    return pivot_dict