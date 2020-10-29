#
# TODO: Read through Pandas EDA lesson
# TODO: Create function for doing basic EDA
# TODO: Add picture of original data to README
# TODO: Add plot of original data to README (violin probably)
# TODO: Deal with null values

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_profiling

if __name__ == '__main__':
    
    
    def normal_EDA(file_path, data_title, file_type='csv', return_information='complex', header=0, names=[]):
        """Takes in a data fie and does typical exploratory data analysis including overview statistics, 
           null value reports, visualizations, and other useful info.

        Args:
            file_path (str): Location of the file to be explored.
            data_title (str): What you want to name your data.
            file_type (str, optional): Input file type. Defaults to 'csv'.
            return_information (str, optional): 'basic' or 'complex' report. Defaults to 'complex'.
            header (int or None, optional): Pandas read file header values location parameter. Defaults to 0.
            names (list, optional): Pandas read file column name parameter. Defaults to [].

        Returns:
            None: Creates and saves a html file and prints a lot to standard output.
        """
        # Future functionality
        # TODO: Pass in pandas file reading parameters (header, names)
        if return_information not in ['basic', 'complex']:
            print("Return information value must be ['basic'] or ['complex']")
            return None
        if file_type != 'csv':
            print("normal_EDA only works with csv files currently. Support for other file types will be added in the future")
            return None
        
        # Reading in the data depending on the file type
        # Base case
        df = pd.read_csv(file_path)
        # TODO: add functionality for other file types. > df = pd.read_[file_type](file_path)
        
        print(f'Quick overview of {data_title} from {file_path}.')
        print(f'More extensive report has been saved to file.')
        # Interesting statistics about the data
        shape = df.shape
        data_points = shape[0] * shape[1] # could also use df.size
        print(f'This dataset has {shape[0]} rows and {shape[1]} columns, creating {data_points} total data points.')
        null_data_points = (df.isnull().sum()).sum()
        percent_null = round((null_data_points / data_points), 3) * 100
        print(f'Of the {data_points} total data points, {percent_null} or {null_data_points} are null')
        
        if return_information == 'basic':
            return None

        # Nulls by column
        nulls_by_column = df.isnull().sum().sort_values(ascending=False)
        percent_nulls_by_column = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
        null_report = pd.concat([nulls_by_column, percent_nulls_by_column], axis=1, keys=['Count', 'Percent Null'])
        null_report['Percent Null'] = null_report['Percent Null'] * 100
        print(null_report)

        # Basic Pandas EDA methods
        print(f'Memory Usage by Column: {df.memory_usage(deep=True)}')
        print(f'Basic Info: {df.info()}')
        print(f'Statistics for int/float columns: {df.describe()}')
        print(f'Quick Look at the orginal data: {df.head(10)}')
        
        # Basic Pandas Plots Showing the Data
        # WARNING: Plots are probably going to be less than stellar till below fix is completed.
        # TODO: Difficult to generalize plot choices to various datasets. Figure this out.
        df.plot.box(vert = False, grid = True)
        corr = df.corr()
        corr.style.background_gradient(cmap='coolwarm').set_precision(2)
        # WARNING: Scatter matrix is heavily resource intensive.
        # TODO: Only show scatter matrix for smaller datasets.
        # pd.plotting.scatter_matrix(df, alpha=0.2)

        # Fancy Stuff - Pandas Profile Report Generator
        pandas_profile = df.profile_report(title=data_title)
        pandas_profile.to_file(output_file=f'{data_title}.html')

        print('----------End of Report----------')
        return None
    


    # WARNING: Code is a work in progress for the brewery and location explorations. 
    # ## Notes / TODO
    # * Eliminate null brewery_name rows - Can't track location and other important aspects.
    # * Keep null review_profilename and beer_abv - Will not be focusing on these features so missing data is not as important.
    # * review_time(int) to a pandas date_time

    df = pd.read_csv('../data/beer_reviews.csv')
    beer_advocate_df = df.copy()
    info = beer_advocate_df.info()

    beer_advocate_df.describe()
    beer_advocate_df.isnull().sum()
    beer_advocate_df.dropna(inplace=True)
    beer_advocate_df.isnull().sum()

    BA_state_df = beer_advocate_df.loc[:, ['brewery_id', 'brewery_name', 'review_overall']]
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