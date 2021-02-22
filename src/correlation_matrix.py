import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == "__main__":

    df = pd.read_csv("../data/full_data/beer_reviews.csv")

    df_ratings = df[
        [
            "review_overall",
            "review_aroma",
            "review_appearance",
            "review_palate",
            "review_taste",
        ]
    ]
    correlation_matrix = round(df_ratings.corr(), 2)

    fig, ax = plt.subplots(figsize=(10, 5))
    # Generate a mask for the upper and lower triangles.
    mask_upper = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    mask_lower = np.tril(np.ones_like(correlation_matrix, dtype=bool))
    # Draw the heatmap with the masks
    ax1 = sns.heatmap(
        correlation_matrix,
        mask=mask_upper,
        cmap="coolwarm",
        linewidths=0.5,
        annot=True,
        fmt=".2f",
        annot_kws={"fontsize": 16},
        xticklabels=False,
        yticklabels=False,
    )
    ax2 = sns.heatmap(
        correlation_matrix,
        mask=mask_lower,
        cmap="coolwarm",
        linewidths=0.5,
        annot=True,
        fmt=".2f",
        annot_kws={
            "fontsize": 16,
        },
        cbar=False,
    )
    x_y_labels = ["Overall", "Aroma", "Appearance", "Palate", "Taste"]
    ax2.set_xticklabels(x_y_labels, rotation=0, fontsize=16)
    ax2.set_yticklabels(x_y_labels, rotation=0, fontsize=16)
    ax2.set_title(
        "Beer Ratings Correlation Matrix", fontsize=20, fontweight="bold"
    )
    # Colorbar label fontsize
    cbar = ax2.collections[0].colorbar
    cbar.ax.tick_params(labelsize=16)
    # plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()
