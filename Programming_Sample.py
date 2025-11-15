# https://github.com/AdamMMahmoud

import pandas as pd; import numpy as np; import matplotlib.pyplot as plt; import seaborn as sns
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

df = pd.read_csv("clientX_data.csv")  # Data assumed already cleaned and weekly-level
df["Week Number"] = df["Week Number"].astype(int)
clientX_weekly = df[["Week Number", "Velocity"]].groupby("Week Number").mean().reset_index()

# --- Compute linkage, clustering, and metrics ---
def compute_linkage_scores(weekly_velocity, linkage_methods, k_max, k_to_show=0):
    scores = {}
    vals = weekly_velocity["Velocity"].values.reshape(-1,1)
    for method in linkage_methods:
        Z = linkage(vals, method=method)
        sil, ch, db = [], [], []
        for k in range(2, k_max+1):
            labs = fcluster(Z, t=k, criterion="maxclust")
            sil.append(silhouette_score(vals, labs))
            ch.append(calinski_harabasz_score(vals, labs))
            db.append(davies_bouldin_score(vals, labs))
        best_k = k_to_show if k_to_show else np.argmax(sil) + 2
        scores[method] = {"Z":Z,"best_k":best_k,"sil":sil,"ch":ch,"db":db}
    return scores

# --- Plot clustered seasonal velocity ---
def plot_clustering_pipeline(weekly_velocity, result_dict, method="single"):
    Z = result_dict[method]["Z"]; k = result_dict[method]["best_k"]
    weekly_velocity = weekly_velocity.copy()
    weekly_velocity["Cluster"] = fcluster(Z, t=k, criterion="maxclust")
    plt.figure(figsize=(8,4))
    sns.scatterplot(data=weekly_velocity,x="Week Number",y="Velocity",
                    hue="Cluster",palette="tab10")
    plt.title(f"Seasonality Clusters ({method}, k={k})")
    plt.xlabel("Week"); plt.ylabel("Velocity")
    plt.legend(title="Cluster",bbox_to_anchor=(1.05,1),loc="upper left")
    plt.tight_layout(); plt.show()

# --- Example pipeline execution ---
methods = ["single","average","complete","ward"]
score_results = compute_linkage_scores(clientX_weekly, methods, k_max=10)
plot_clustering_pipeline(clientX_weekly, score_results, method="ward")
