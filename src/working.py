import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt


df = pd.read_csv('../data/full_data/beer_reviews.csv')

df_ratings = df[['review_overall', 'review_aroma', 'review_appearance', 'review_palate', 'review_taste']]
correlation_matrix = df_ratings.corr()
# correlation_matrix.style.background_gradient(cmap='coolwarm').set_precision(2)

sn.heatmap(correlation_matrix, cmap='coolwarm', annot=True, )
plt.show()