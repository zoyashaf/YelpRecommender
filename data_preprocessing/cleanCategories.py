import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------- List of categories that need to be cleaned ------------------------
## all cateogires we want to drop either because 
## (1) they are irrlevant
## (2) all restaurants in that cateogory share another tag as well
random_categories = ['Apartments', 'Arcades', 'Art Galleries', 'Aquariums', 'Adult Entertainment', 'Arabic',
                     'Active Life', 'Arts & Entertainment','Arts & Crafts','Appliances', 'Bar Crawl', 'Adult',
                     'Health Markets', 'Boat Charters','Bike Repair/Maintenance','Bikes', 'Books','Boating',
                     'Bowling','Barbers','Cabaret','Cultural Center','Christmas Trees','Cooking Classes',
                     'Custom Cakes','Community Service/Non-Profit','Convenience Stores','Cooking Schools',
                     'Country Clubs','Caterers','Cafeteria','Dance Clubs','Eatertainment','Education',
                     'Event Planning & Services','Flowers & Gifts','Fitness & Instruction','Fruits & Veggies', 'Furniture Stores',  
                     'Food',  'Fashion','Gift Shops','Gyms','Grocery','Hotels',  'Home Services','Jazz & Blues',
                     'Karaoke','Landmarks & Historical Buildings','Local Services','Local Flavor','Lounges',
                     'Mass Media','Music Venues','Musicians','Party & Event Planning','Personal Chefs',
                     'Public Services & Government', 'Photographers', 'Pubs','Pool Halls','Real Estate',
                     'Resorts', 'Restaurants','Social Clubs','Souvenir Shops', 'Shopping','Specialty Schools',
                     'Tobacco Shops', 'Tours',  'Venues & Event Spaces','Wholesale Stores','Teppanyaki',
                     'Heating & Air Conditioning/HVAC','Kitchen & Bath','Pretzels','Religious Organizations',
                     'Restaurant Supplies','Salvadoran', 'Travel Agents','Travel Services','Wholesalers',
                     'Yelp Events','Herbs & Spices','Nicaraguan', 'Pop-up Shops', 'Discount Store','Drugstores', 'Vape Shops',
                     'Vitamins & Supplements','Health & Medical','Nutritionists','Smokehouse', 'Parks', 'Holiday Decorations',
                     'Day Spas','Hair Salons', 'Performing Arts','Skin Care', 'Supernatural Readings',
                     'Tabletop Games','Sports Wear','Organic Stores','Professional Services','Indoor Playcentre',
                     'Kids Activities', 'Sporting Goods','Mags', 'Tree Services','Sporting Goods', 'Home Decor',
                     'Golf', 'Herbal Shops''Shared Office Spaces','Beauty & Spas', 'Music & Video',
                      'Swimming Pools', 'Shared Office Spaces','Gas Stations','Wedding Planning', 'Cards & Stationery',
                      'Nurseries & Gardening','Party Supplies', 'Electronics Repair','Health Markets','Home & Garden', 'British', 
                      'Malaysian', 'Egyptian', 'Polish', 'Russian', 'Ukrainian','Burmese','Arabic', 'Shanghainese', 'Argentine', 'Laotian',
                      'Acai Bowls', 'Shanghainese','Haitian','Candy Stores','Szechuan','Venezuelan','Basque','Pasta Shops','Empanadas', 'Fondue', 'Argentine', 
                      'Pan Asian','Kebab','Lebanese','Pakistani','Colombian','Halal','Falafel']


categories_to_combine = [['Distilleries', 'Wine & Spirits', 'Wine Tasting Room', 'Bars', 'Beer', 'Brewpubs', 'Breweries', 'Wineries', 'Nightlife'],
                        ['Auction Houses', 'Farmers Market'], ['Coffee & Tea', 'Coffee Roasteries', 'Cafes'],
                        ['Waffles', 'Bagels', 'Creperies', 'Breakfast & Brunch'],
                        ['Ice Cream & Frozen Yogurt', 'Gelato'],
                        ['Peruvian', 'Caribbean', 'Cuban',"Brazilian", 'Mexican', 'Tacos', 'Honduran', 'Tapas/Small Plates', 'Latin American'], 
                        ['Meat Shops', 'Butcher'], ['Poke','Hawaiian'], 
                        ['Greek', 'Mediterranean', 'Middle Eastern', 'Morrocan'],
                        ["Korean", "Taiwanese", "Noodles", "Ramen", "Chinese", "Dim Sum", "Japanese", "Asian Fusion"],
                        ['Vegan', 'Vegetarian'], ['Filipino', "Vietnamese", "Thai"],
                        ["German", 'Brasseries', "French", "Italian", "Irish", "Spanish", 'Modern European'],
                        ["Burgers", "Hot Dogs", 'Fish & Chips',"Pizza", 'Chicken Wings'],
                        ['Chocolatiers & Shops', 'Donuts', 'Desserts', 'Bakeries','Macarons', 'Patisserie/Cake Shop', 'Bakeries', 'Cupcakes'],
                        ['American (New)', 'American (Traditional)', 'Barbeque', 'Cheesesteaks', 'Southern', 'Steakhouses'], ['African', 'Ethiopian']]

titles = ['Alcohol','Markets','Coffee_and_Tea', 'Breakfast', 
        'Frozen_Desserts', 'Latin American', 'Butcher', 'Hawaiian/Poke', 'Mediterranean',
        'East Asian', 'Vegan/Vegetarian', 'Southeast Asian', 'European', 'Fast Food', 'Desserts', 'American', 'African']

# -------------------------------------------------------Functions to help cleaning  ------------------------
"""
combineCols(names, col_llist, df)
    names = list of names of new columns 
    col_list = list of lists where each sublist contains the columns to combine
    df = original df 
    function to combine columns so that it takes two columns such as 'Nightlife' and 'Pubs'and creates 
    a new column of 0s and 1s which is 1 whereever Nightlife or Pubs is 1
    the two original columns are dropped from the dataframe and the new column is concatenated 
"""
def combineCols(names, col_list, df): 
    for name, cols in zip(names, col_list):
        
        # create a new column with the maximum value between the selected columns using a lambda function
        new_col = df[cols].apply(lambda row: max(row), axis=1)

        # drop the selected column
        df = df.drop(cols, axis=1)
        # add new column
        df[name] = new_col
    
    return df


"""
cleanStrings(df)

    df = original df 
    finds categories such as ' Acai Bowls' and 'Acai Bowls' and combines them into one 

"""
def cleanStrings(df):

    dummy_counts = dummies.sum().to_dict()
    for key in dummy_counts.keys():

        key = key.strip()
        cols = dummies.filter(like=key).columns.tolist()
        #print(cols)

        if len(cols) > 1: 
            # create a new column with the maximum value between the selected columns using a lambda function
            new_col = dummies[cols].apply(lambda row: max(row), axis=1)
            #print(examp_df)
            # drop the selected columns
            dummies = dummies.drop(cols, axis=1)

            # add new column
            dummies[key] = new_col

    columns = [col.strip() for col in dummies.columns]
    dummies.columns = columns

    return dummies


# -------------------------- main cleaning function --------------------------
"""
cleanCats(merged_df)

    merged_df = original df --> should be merged df of businesses and reviews with the categories column of the original business df 
        i.e. merged_df = pd.merge(reviews, restaurants, on='business_id')
             merged_df.columns = 'review_id', 'user_id', 'business_id', 'stars', 'text', 'biz_stars', 'biz_review_count', 'categories'

    output: merged_df concatenated with cleaned one-hot encoded categories 
"""
def cleanCats(merged_df):

    ## one-hot encodes categories
    dummies = merged_df['categories'].str.get_dummies(sep=',')

    ## cleans up titles since some categories are written as ' Acai Bowls' and 'Acai Bowls'
    dummies2 = cleanStrings(dummies) 

    ## finds which of the random categoies are in the input df and drops them 
    to_drop = [col for col in random_categories if col in dummies2.columns]
    dummies_filtered = dummies2.drop(to_drop, axis = 1) # left with 179 columns 

    # combines columns defined in categoties_to_combine 
    dummies_filtered = combineCols(titles, categories_to_combine, dummies_filtered)

    # combines the original df with the cleaned one hot encoded df 
    nola_final = pd.concat([merged_df, dummies_filtered], axis = 1)

    ## drops rows with businesses labeled as automotive and bed & breakfast
    nola_final = nola_final[nola_final['Automotive'] != 1]
    nola_final = nola_final[nola_final['Bed & Breakfast'] != 1]
    nola_final = nola_final.drop(['Automotive', 'Bed & Breakfast'], axis = 1)

    return nola_final.reset_index(drop=True)

