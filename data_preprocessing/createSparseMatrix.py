import pandas as pd
import numpy as np
from tqdm import tqdm
from multiprocess import Pool, cpu_count ## used to parallelize code 
from utils import process_user ## function which creates pivot table 

## importing business data to find which business_ids correspond to restaurants 
business_data = pd.read_csv('./raw_business.csv')
restaurants = business_data[business_data.categories.fillna('-').str.lower().str.contains('restaurant')]

## separating out reviews which correspond to restaurants 
reviews_data = pd.read_csv('./raw_reviews.csv')
reviews_data.drop('Unnamed: 0', axis =1, inplace = True)

## cities of interest for recommender system
cities = ['Philadelphia','Tampa','Indianapolis','Nashville','Tucson','New Orleans','Edmonton','Saint Louis','Reno']

"""
The following for loop interates through every city in the cities array. It

* finds which businesses are located in that specific city and saves the corresponding reviews
* uses the multiprocess toolbox to use all available CPUS to parallelize pivot table formation
* Process_user: 
    For each user in reviews, process_user first drops any duplicate reviews i.e. if one user rated one restaurant more than once with 
    the same rating, we drop every review after the first. Then, we group by business_id in case the user has rated one restaurant more than 
    once with different ratings and take the average of those ratings. In the case, where the user has only rated a restaurant once (which is the
    majority case) this just returns the star rating. Then we create a pivot table which switches the rows and columns so that the output dataframe
    has rows which are all the user_ids and columns which are all the business_ids. The value in the returned dataframe is the star rating the user
    gave. 
    The dataframe is then converted to a dictionary and returned. 
* The output of process_user is appended to formatted_data_list which is a list of dictionaries (where the dictionary represents the pivot table for each user)
* Once all the users have been processed, formatted_data_list is converted back into a dataframe
* Note: dictionary and lists are used for appending instead of directly appending dataframes to reduce run time of script 
"""

for city in cities:
    biz_ids = restaurants['business_id'].loc[restaurants['city']== city]
    reviews = reviews[reviews['business_id'].isin(biz_ids)]

    formatted_data_list = []
    users = reviews['user_id'].unique()
    with Pool(cpu_count()) as pool:
        results = []
        with tqdm(users, ncols=0) as pbar:
            for user in pbar:
                subset = reviews.loc[reviews['user_id'] == user]
                result = pool.apply_async(process_user, args=(subset,))
                formatted_data_list.append(result.get())

    output = pd.DataFrame.from_records(formatted_data_list)
    output.to_csv('./formatted_data/{}.csv'.format(city))