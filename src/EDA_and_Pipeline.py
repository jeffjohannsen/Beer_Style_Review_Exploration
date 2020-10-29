#
# TODO: Read through Pandas EDA lesson
# TODO: Create function for doing basic EDA
# TODO: Add picture of original data to README
# TODO: Add plot of original data to README (violin probably)
# TODO: Deal with null values

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    
    
    def normal_EDA(file_path, data_type='csv', return_information='basic'):

        if return_information not in ['basic', 'complex']:
            print("Return information value must be ['basic'] or ['complex']")
            return None
        if data_type != 'csv':
            print("normal_EDA only works with csv files currently. Support for other file types will be added in the future")
            return None

        df = pd.read_csv(file_path)

        # Interesting statistics about the data

        # Basic Pandas EDA methods
        print(df.info())
        print(df.describe())
        print(df.head(10))

        # Basic Pandas Plots Showing the Data
    
    
    df = pd.read_csv('../data/beer_reviews.csv')

    beer_advocate_df = df.copy()

    info = beer_advocate_df.info()

    beer_advocate_df.isnull().sum()


    # ## Notes / TODO
    # * Eliminate null brewery_name rows - Can't track location and other important aspects.
    # * Keep null review_profilename and beer_abv - Will not be focusing ont hese fetures so missing data is not important.
    # * review_time(int) to a pandas date_time

    beer_advocate_df_1.describe()

    beer_advocate_df_1.isnull().sum()

    beer_advocate_df_1.dropna(inplace=True)

    beer_advocate_df_1.isnull().sum()

    BA_state_df = beer_advocate_df_1.loc[:, ['brewery_id', 'brewery_name', 'review_overall']]

    BA_state_df.info()

    BA_state_df_agg = BA_state_df.groupby('brewery_name').agg({'brewery_id': [('brewery_id_most_common', lambda x: pd.Series.mode(x)[0]),
                                                            'count',
                                                            ('unique_brewery_ids', lambda x: len(set(x)))],
                                            'review_overall': [('Mean Rating' , lambda x:round(x.mean(), 2))]})

    BA_state_df_agg.reset_index(inplace=True)

    BA_state_df_agg

    BA_state_df_agg.info()

    BA_state_df_2 = BA_state_df.groupby('brewery_id').agg({'review_overall' : lambda x: round(x.mean(), 2), 'brewery_name' : lambda column: column.iloc[0], 'brewery_id' : [('review_count', 'count')]}).reset_index()

    BA_state_df_2.head(25)


    # TODO: Create pipeline for taking input data, organizing, and outputting SQL file
    # TODO: Test SQL database with SQL queries in pysql. Place tests in tests folder.