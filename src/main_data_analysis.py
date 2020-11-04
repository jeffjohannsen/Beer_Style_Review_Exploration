
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_profiling


def make_sample(original_data, sample_size, save_location):
    """Takes a dataset from a csv file
    and creates a random sample that is saved to file.

    Args:
        original_data (str): File path to original dataset.
        sample_size (float): Fraction of original data to be saved as sample.
        save_location (str): File path and name to save sample.

    Returns:
        None
    """
    df = pd.read_csv(original_data)
    sample_df = df.sample(frac=sample_size)
    sample_df.to_csv(save_location)
    return None


def ratings_hist(ax, data):
    N, bins, patches = ax.hist(data.iloc[:, i],
                                bins=[0, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5],
                                align='left', edgecolor='white', linewidth=1)
    ax.set_title(data.columns[i])
    ax.set_ylabel('Count of Ratings')
    ax.set_xlabel('Rating 0 to 5')
    ax.set_ylim(0, 700000)
    ax.set_xticks([0, 1, 2, 3, 4, 5])
    # bar coloring
    colors = ['darkred', 'darkred', 'red', 'red', 'indianred', 'indianred',
                'cornflowerblue', 'royalblue', 'blue', 'blue', 'darkblue', 'darkblue']
    for j in range(len(patches)):
        patches[j].set_facecolor(colors[j])


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
    print(f'Of the {data_points} total data points, {percent_null}% or {null_data_points} are null.')
    
    
    if return_information == 'basic':
        print('----------End of Report----------')
        return None

    print(' ')
    print('-------------------Null Report-------------------------------------------------------------')
    print(' ')

    # Nulls by column
    nulls_by_column = df.isnull().sum().sort_values(ascending=False)
    percent_nulls_by_column = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
    null_report = pd.concat([nulls_by_column, percent_nulls_by_column], axis=1, keys=['Count', 'Percent Null'])
    null_report['Percent Null'] = null_report['Percent Null'] * 100
    print(null_report)
    
    print(' ')
    print('-------------------Memory Usage by Column-------------------------------------------------------------')
    print(' ')

    # Basic Pandas EDA methods
    print(df.memory_usage(deep=True))
    print(' ')
    print('-------------------Basic Info-------------------------------------------------------------')
    print(' ')
    print(df.info())
    print(' ')
    print('-------------------Statistics for numeric columns-------------------------------------------------------------')
    print(' ')
    print(df.describe())
    print(' ')
    print('-------------------Quick Look at the Actual Data-------------------------------------------------------------')
    print(' ')
    print(df.head(10))
    
    # Basic Pandas Plots Showing the Data
    # WARNING: Plots are probably going to be less than stellar till below fix is completed.
    # TODO: Difficult to generalize plot choices to various datasets. Figure this out.
    print(' ')
    print('-------------------Box and Whisker Plots-------------------------------------------------------------')
    print(' ')
    df.plot.box(vert = False, grid = True)
    plt.show()
    print(' ')
    print('-------------------Correlation Matrix-------------------------------------------------------------')
    print(' ')
    corr = df.corr()
    print(corr)
    # plt.show()
    # WARNING: Scatter matrix is heavily resource intensive.
    # TODO: Only show scatter matrix for smaller datasets.
    # pd.plotting.scatter_matrix(df, alpha=0.2)
    print(' ')
    print('-------------------Building and saving a cool HTML report.-------------------------------------------------------------')
    print(' ')
    
    # Fancy Stuff - Pandas Profile Report Generator
    # WARNING: Breaks in my ipython. Works fine in Jupyter.
    # TODO: Investigate below error message
    # ipython error point and message:
    # Summarize dataset:  67%|████████████████████████████████████████████████████████████████████▋                                  | 
    # 18/27 [00:23<00:38,  4.32s/it, Calculate phi_k correlation]: 
    # >>>>>> CommandLine Error: Option 'help-list' registered more than once!
    # >>>>>> LLVM ERROR: inconsistency in registered CommandLine options
    pandas_profile = df.profile_report(title=data_title)
    pandas_profile.to_file(output_file=f'{data_title}.html')

    print('----------End of Report----------')
    return None
    
# TODO: Create pipeline for taking input data, organizing, and outputting SQL file
# TODO: Test SQL database with SQL queries in pysql. Place tests in tests folder.

if __name__ == '__main__':

    plt.style.use('fivethirtyeight')
    plt.rcParams.update({'font.size': 16, 'font.family': 'sans'})

    df = pd.read_csv('../data/beer_reviews.csv')
    
    
    beer_advocate_df = df.copy()

    beer_advocate_df.sample(10)

    print(beer_advocate_df.dtypes)

    corr = df.corr()
    corr.style.background_gradient(cmap='coolwarm').set_precision(2)

    # pd.plotting.scatter_matrix(df, alpha=0.2)

    (beer_advocate_df.isnull().sum()).sum()

    for_violin = df[['review_overall', 'review_aroma', 'review_appearance', 'review_palate', 'review_taste', 'beer_abv']]
    for_violin.info()

    corr2 = for_violin.corr()
    corr2.style.background_gradient(cmap='coolwarm').set_precision(2)

    # pd.plotting.scatter_matrix(for_violin, alpha=0.2)


    
    data = for_violin
    fig, ax = plt.subplots(1,5, figsize=(20,4))

    axex = ax.flatten()
    for i in range(len(axex)):
        N, bins, patches = axex[i].hist(data.iloc[:, i], bins=[0, .5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5], align='left', edgecolor='white', linewidth=1)
        axex[i].set_title(data.columns[i])
        axex[i].set_ylabel('Count of Ratings')
        axex[i].set_xlabel('Rating 0 to 5')
        axex[i].set_ylim(0, 700000)
        axex[i].set_xticks([0, 1, 2, 3, 4, 5])
        colors=['darkred', 'darkred', 'red', 'red', 'indianred', 'indianred', 'cornflowerblue', 'royalblue', 'blue', 'blue', 'darkblue', 'darkblue']
        for j in range(len(patches)):
            patches[j].set_facecolor(colors[j])

    fig.tight_layout()
    plt.savefig('ratings_histogram.png', dpi = 300)

    # WARNING: Below code is a work in progress for the brewery and location explorations. 
    # ## Notes / TODO:
    # * Eliminate null brewery_name rows - Can't track location and other important aspects.
    # * Keep null review_profilename and beer_abv - Will not be focusing ont hese fetures so missing data is not important.
    # * review_time(int) to a pandas date_time

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
    BA_state_df_2 = BA_state_df.groupby('brewery_id').agg({'review_overall': lambda x: round(x.mean(), 2), 'brewery_name' : lambda column: column.iloc[0], 'brewery_id' : [('review_count', 'count')]}).reset_index()
    BA_state_df_2.head(25)
