import random
import numpy as np
from collections import defaultdict
import pandas as pd
from algorithm.Recommendation import Recommendation
from Network.Multithread_Server import Server
from Network.Multithread_UDP_Server import UDP_Server
from algorithm.Place import Place




def recommendation():
    ################################ Arrange k-means #############################################
    f_means = "Data/Results/k_means.csv"
    centers = pd.read_csv(f_means)
    centers = centers[["ID", "Latitude", "Longitude"]].dropna()

    ################################# Arrange cluster data ########################################
    cluster_data = {}

    # Save each store in their respective cluster
    f_cluster = "Data/Results/Cluster_"
    f_cluster_sufix = ".csv"

    #
    cluster_prefix = "cluster_"

    for i_index in range(len(centers.columns)):
        file_name = f_cluster + str(i_index) + f_cluster_sufix
        df_stores = pd.read_csv(file_name)
        #df_stores["Congestion"] = random.randint(0, 200)
        #df_stores["Capacity"] = random.randint(200, 300)
        columns_titles = ["Y", "X", "Name", "cluster", "Congestion", "Capacity"]
        df_stores = df_stores.reindex(columns=columns_titles)
        df_stores = df_stores.rename(columns={'Y': 'Latitude', 'X': 'Longitude'})

        cluster_data[cluster_prefix + str(i_index)] = df_stores

    ##################################### Class call ##########################################
    rec = Recommendation(centers,cluster_data, 0.3, 0.5, 0.2)
    #ll  = rec.get_distance_list(( 20.67715178768269, -103.43001294075434 ))

    dd = rec.get_recommendation_list(3, 20.67715178768269, -103.43001294075434)
    rec.update_congestion(rec.estimate_congestion(dd,1,0.3))

    for place in dd:
        print(place)




if __name__ == "__main__" \
               "":
    # recommendation()


    flg_tcp=True

    ################################ Arrange k-means #############################################
    f_means = "Data/Results/k_means.csv"
    centers = pd.read_csv(f_means)
    centers = centers[["ID", "Latitude", "Longitude"]].dropna()

    ################################# Arrange cluster data ########################################
    cluster_data = {}

    # Save each store in their respective cluster
    f_cluster = "Data/Results/Cluster_"
    f_cluster_sufix = ".csv"

    #
    cluster_prefix = "cluster_"

    for i_index in range(len(centers.columns)):
        file_name = f_cluster + str(i_index) + f_cluster_sufix
        df_stores = pd.read_csv(file_name,encoding='latin1')
        columns_titles = ["Y", "X", "Name", "cluster", "Congestion", "Capacity"]
        df_stores = df_stores.reindex(columns=columns_titles)
        df_stores = df_stores.rename(columns={'Y': 'Latitude', 'X': 'Longitude'})

        cluster_data[cluster_prefix + str(i_index)] = df_stores


    if flg_tcp:
    # TCP server
        server = Server("localhost", 9999, "localhost", 9877, "ummisco.gama.network.common.CompositeGamaMessage", 2048, "./contents/string")
        server.create_recommendation_instance(centers, cluster_data)
        # print(server.call_recommendation("{-103.43280802636433,20.68353951312682,0.0}"))
        server.run_server()
    else:
        server = UDP_Server("localhost", 9999, "localhost", 9877,2048)
        server.create_recommendation_instance(centers, cluster_data)
        server.run_server()




