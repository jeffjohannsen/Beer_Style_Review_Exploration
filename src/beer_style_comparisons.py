# WARNING: Code is a collections of pieces that are not meant to be run together.
# TODO: Convert major pieces of code to functions to fix ^^
# TODO: Remove remnants of notebook testing.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scipy.stats as stats

def weighted_mean(data, base_mean, weight):
   """Helper function for creating a weighted mean from two pandas dataframe columns.

   Args:
       data (Pandas Dataframe): Overall dataset
       base_mean (str): Column with means.
       weight (str): Column with weights.

   Returns:
       float: Weighted Mean rounded to 2 decimals.
   """
   m = data[base_mean]
   w = data[weight]
   try:
      return ((m * w).sum() / w.sum()).round(2)
   except ZeroDivisionError:
      return m.mean().round(2)

if __name__ == '__main__':

   plt.style.use('fivethirtyeight')
   plt.rcParams.update({'font.size': 16, 'font.family': 'sans'})

   df = pd.read_csv('../data/beer_reviews.csv')
   bsdf = df.copy()

   bsdf = bsdf.loc[:, ['beer_style', 'review_overall', 'review_aroma', 'review_appearance', 'review_palate', 'review_taste']]
   print(bsdf)

   bsdf_grouped = bsdf.groupby('beer_style').agg({'beer_style': 'count', 'review_overall': ['std', 'mean'], 'review_aroma': ['std', 'mean'], 'review_appearance': ['std', 'mean'], 'review_palate': ['std', 'mean'], 'review_taste': ['std', 'mean']}).round(2).reset_index()
   print(bsdf_grouped)

   bsdf_grouped.sort_values(('beer_style', 'count'), ascending=False, inplace=True)
   print(bsdf_grouped)

   bsdf_grouped.reset_index(inplace=True)

   bsdf_t20 = bsdf_grouped.loc[:, [('beer_style', ''), ('beer_style','count'), ('review_overall', 'mean'), ('review_overall', 'std')]]
   bsdf_t20.columns = bsdf_t20.columns.droplevel()
   bsdf_t20.columns = ['beer_style', 'beer_style_review_count', 'review_overall_mean', 'review_overall_std']
   print(bsdf_t20)
   bsdf_t20.info()

   new = bsdf_t20[['beer_style', 'review_overall_mean', 'beer_style_review_count']]
   new.sort_values('review_overall_mean', ascending=False)
   # bsdf_high_1 = bsdf_high.loc[:1, :]
   # bsdf_high
      
   beer_style_weighted_mean = weighted_mean(bsdf_t20, 'review_overall_mean', 'beer_style_review_count')

   print(round(bsdf_t20['review_overall_mean'].mean(), 2))

   #-------------------------------------------------------------------------------------------------#

   # Hypothesis Testing

   # H0: American IPA Review Overall Mean <= Max Review Overall Mean  
   # H1: American IPA Review Overall Mean > Max Review Overall Mean  
   # Alpha: 0.05  
   # One-Tailed Test  
   # Talk about the issues with large sample tests, iid issues, and other problems.
   # Are two reviews of the same beer by the same person at different times independent?

   AIPA = df[df['beer_style'] == 'American IPA']
   AIPA = AIPA['review_overall']
   AWA = df[df['beer_style'] == 'American Wild Ale']
   AWA = AWA['review_overall']
   print(stats.mannwhitneyu(AIPA, AWA, alternative='greater'))
   print(stats.ttest_1samp(AIPA, 3.82))

   american_ipa_overall_ratings = bsdf[bsdf['beer_style'] == 'American IPA']
   american_ipa_overall_ratings.reset_index(inplace=True)
   american_ipa_overall_ratings

   american_ipa_overall_ratings = american_ipa_overall_ratings[['beer_style', 'review_overall']]
   american_ipa_overall_ratings

   american_ipa_mean = round(american_ipa_overall_ratings['review_overall'].mean(), 2)
   print(f'American IPA: {american_ipa_mean}')
   highest_rated_beer_style_mean_rating = max(bsdf_t20['review_overall_mean']) 
   print(f'Highest: {highest_rated_beer_style_mean_rating}')
   average_rated_beer_style = weighted_mean(bsdf_t20, 'review_overall_mean', 'beer_style_review_count')
   print(f'Weighted Average: {average_rated_beer_style}')
   unweighted_average_rated_beer_style = round(bsdf_t20['review_overall_mean'].mean(), 2)
   print(f'Unweighted Average: {unweighted_average_rated_beer_style}')

   test_stat, p_value = stats.ttest_1samp(american_ipa_overall_ratings['review_overall'], highest_rated_beer_style_mean_rating)
   print(f'Test Statistic:{test_stat}, P-Value:{p_value/2}')
   if (p_value/2) < 0.05:    # alpha value is 0.05 or 5% - one-tailed so divide p-value in half
      print("Reject Null Hypothesis")
   else:
      print("Fail to Reject Null Hypothesis")

   test_stat, p_value = stats.ttest_1samp(american_ipa_overall_ratings['review_overall'], average_rated_beer_style)
   print(f'Test Statistic:{test_stat}, P-Value:{p_value/2}')
   if (p_value/2) < 0.05:    # alpha value is 0.05 or 5% - one-tailed so divide p-value in half
      print("Reject Null Hypothesis")
   else:
      print("Fail to Reject Null Hypothesis")

   #-----------------------------------------------------------------------------------------------------#

   # Plotting

   # Top 10 by Review Count- Color Coded by Style - Mean Rating at Top

   fig, ax = plt.subplots(figsize=(10,10))    
   fig.tight_layout()

   # data
   x_data = np.arange(10)
   y_data = bsdf_t20.loc[:9, 'beer_style_review_count']
   mean_review_count = bsdf_t20['beer_style_review_count'].mean()

   # plotting
   bar_colors = ['orangered', 'orangered', 'orangered', 'k', 'k', 'k', 'tab:brown', 'tab:brown', 'tab:brown', 'tab:brown']
   ax.bar(x_data, y_data, color=bar_colors)

   ax.set_title("Top 10 Most Popular Craft Beer Styles", fontweight="bold") 
   # ax.set_xlabel("Beer Style")
   ax.set_ylabel("Review Count", fontweight="bold")
   ax.set_ylim(0, 120000)
   ax.set_xticks(x_data)
   ax.set_xticklabels(bsdf_t20.loc[:9, 'beer_style'], rotation = 45, ha="right", fontweight='bold')
   legend_elements = [Line2D([0], [0], color='orangered', lw=20, label='IPAs'),
                     Line2D([0], [0], color='k', lw=20, label='Darker/Heavier Styles \n (Stouts, Porters)'),
                     Line2D([0], [0], color='tab:brown', lw=20, label='Other Beer Styles')]
                     
   ax.legend(handles=legend_elements)
   plt.savefig('most_popular_top_10.png', dpi = 300, bbox_inches='tight')


   # Scatter Plot of Review Counts vs. Mean Rating

   # basic setup - Don't forget imports, style, and master font size/family.
   fig, ax = plt.subplots(figsize=(12,12))    
   fig.tight_layout()

   # data
   x_data = bsdf_t20['beer_style_review_count']
   y_data = bsdf_t20['review_overall_mean']
   mean_rating = bsdf_t20['review_overall_mean'].mean()
   mean_review_count = bsdf_t20['beer_style_review_count'].mean()

   # plotting
   ax.scatter(x_data, y_data)
   ax.set_title("Beer Style Review Count vs Rating") 
   ax.set_xlabel("Review Count")
   ax.set_ylabel("Rating")
   ax.set_ylim(0, 5)


   # Top 10 by Mean Rating
   # * Only beers in top 50% of review count (~10000 reviews)

   bsdf_t20['beer_style_review_count'].quantile(0.50)

   bsdf_mean_sort = bsdf_t20[bsdf_t20['beer_style_review_count'] > 10000]
   bsdf_mean_sort = bsdf_mean_sort.sort_values('review_overall_mean', ascending=False)
   bsdf_mean_sort.reset_index(inplace=True)
   bsdf_mean_sort.drop('index', axis=1, inplace=True)
   bsdf_mean_sort.head(12)

   fig, ax = plt.subplots(figsize=(10,10))    
   fig.tight_layout()

   # data
   x_data = np.arange(10)
   y_data = bsdf_mean_sort.loc[:9, 'review_overall_mean']
   mean_review_count = bsdf_mean_sort['beer_style_review_count'].mean()

   # plotting
   bar_colors = ['tab:brown', 'tab:brown', 'k', 'k', 'orangered', 'tab:brown', 'orangered', 'tab:brown', 'k', 'orangered']
   ax.bar(x_data, y_data, color=bar_colors)
   ax.set_title("Top 10 Highest Rated Craft Beer Styles", fontweight="bold") 
   # ax.set_xlabel("Beer Style")
   ax.set_ylabel("Rating", fontweight="bold")
   ax.set_ylim(3.8, 4.2)
   ax.set_xticks(x_data)
   ax.set_xticklabels(bsdf_mean_sort.loc[:9, 'beer_style'], rotation = 45, ha="right", fontweight='bold')
   legend_elements = [Line2D([0], [0], color='orangered', lw=20, label='IPAs'),
                     Line2D([0], [0], color='k', lw=20, label='Darker/Heavier Styles \n (Stouts, Porters)'),
                     Line2D([0], [0], color='tab:brown', lw=20, label='Other Beer Styles')]
                     
   ax.legend(handles=legend_elements)
   plt.savefig('highest_rated_top_10.png', dpi = 300, bbox_inches='tight')


   fig, ax = plt.subplots(figsize=(10,4))    
   fig.tight_layout()

   # data
   x_data = bsdf_t20['review_overall_mean'] 
   # y_data = bsdf_mean_sort.loc[:9, 'review_overall_mean']
   # mean_review_count = bsdf_mean_sort['beer_style_review_count'].mean()

   # plotting
   ax.boxplot(x_data, vert=False, widths=.6, patch_artist=True,
               flierprops = dict(marker='o', markerfacecolor='orangered', markersize=12, linestyle='none', alpha=.5),
               medianprops = dict(linestyle='-', linewidth=2.5, color='k'),
               whiskerprops = dict(linestyle='-', linewidth=2.5, color='k'), 
               capprops = dict(linestyle='-', linewidth=2.5, color='k'), 
               boxprops = dict(linestyle='-', linewidth=2.5, color='k', facecolor='orangered'))
   y = np.random.uniform(-0.07, 0.07, size=len(x_data))
   ax.plot(x_data, .5+y, marker='.', color='orangered', linestyle='', alpha=0.5, markersize=25)
   ax.axvline(x=3.97, ymin=0, ymax=1, linestyle=':', color='b', label=' American IPA - 3.97 \n Rank: 14th out of 104 \n 87th Percentile')

   ax.set_title("Craft Beer Style Ratings Distribution", fontweight="bold") 
   ax.set_xlabel('Rating out of 5', fontweight='bold')
   ax.set_yticks([0])
   ax.set_xlim(2.5,4.5)
   ax.legend(loc='upper left')
   plt.savefig('beer_style_ratings_distribution_Amer_IPA.png', dpi = 300, bbox_inches='tight')
   # ax.set_xticklabels(bsdf_mean_sort.loc[:9, 'beer_style'], rotation = 45, ha="right", fontweight='bold');

   #----------------------------------------------------------------------------------------------------#

   # Percentiles and Rank 

   print(bsdf_t20)

   bsdf_t20['review_overall_rank'] = bsdf_t20['review_overall_mean'].rank(axis=0, method='min', ascending=False)
   bsdf_t20['review_overall_rank'] = bsdf_t20['review_overall_rank'].astype(int)
   print(bsdf_t20)

   bsdf_t20['review_overall_percentile'] = ((1 - bsdf_t20['review_overall_mean'].rank(axis=0, method='max', ascending=False, pct=True).round(2))*100).astype(int)
   print(bsdf_t20)
