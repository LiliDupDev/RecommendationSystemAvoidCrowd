from haversine import haversine, Unit
from collections import defaultdict
import numpy as np
import math
import pandas as pd
from .Place import Place, Congestion_Level

class Recommendation:
    # self.cluster_data     # Dictionary that contains all cluster data
    # self.cluster_number   # Int that contains the total number of clusters
    # self.cluster_prefix = "cluster_"  # This variable only works to call the dictionary data
    # self.centers          # k-means
    # self.weight_distance
    # self.weight_congestion

    # f_name: Datasource file in CSV
    # cluster_directory: Directory that contains the clusters' data
    def __init__(self, centers, cluster_dictionary, weight_distance, weight_congestion, weight_threshold, threshold=0.25):
        self.cluster_prefix = "cluster_"
        self.centers = centers
        self.cluster_data = cluster_dictionary
        self.cluster_number = len(centers.index)
        self.weight_distance = weight_distance
        self.weight_congestion = weight_congestion
        self.weight_threshold = weight_threshold
        self.congestion_threshold = threshold

    # Returns a dictionary with the cluster key and the distance between the center's cluster and coordinates
    def get_distance_list(self, coordinates):
        source = coordinates

        distance_list = {}
        # Calculate distance to means to find a cluster for searching
        for center in self.centers.values:
            if len(center) >= 3:
                target = (center[1], center[2])
                distance_list[self.cluster_prefix + str(int(center[0]))] = haversine(source, target)
            else:
                raise Exception("Column order must be: ID, Latitude, Longitude")

        return distance_list

    # places: an integer that indicates the maximum number of places to be returned as recommendations
    # Return a list with the recommendations sorted by payoff
    def get_recommendation_list(self, places, latitude, longitud):
        places_count = places
        coordinates = (latitude, longitud)
        distance_list = self.get_distance_list(coordinates)

        recommendation_list = list()
        df_cluster = pd.DataFrame(self.cluster_data["cluster_0"])
        df_cluster = df_cluster.iloc[0:0]

        for w in sorted(distance_list, key=distance_list.get):
            # Get cluster
            df_cluster=df_cluster.append(self.cluster_data[w],ignore_index = True) #LD


            if(df_cluster.shape[0]>places):
                # Calculate distance
                df_cluster["distance"] = df_cluster.apply(lambda x: haversine(coordinates, (x["Latitude"], x["Longitude"])),axis=1)

                # Normalize distance
                df_cluster["dist_norm"] = np.where(df_cluster["distance"] == 0, 0.0,
                                                   df_cluster["distance"].min() / df_cluster["distance"])
                # Correccion 11/03/2021 Cambiar el calculo de la normalizacion de distancia para prbar la penalizacion de umbral
                #df_cluster["dist_norm"] = df_cluster["distance"] / df_cluster["distance"].max()

                # Normalize Estimated Congestion
                df_cluster["e_congestion"] = df_cluster["Congestion"] / df_cluster["Capacity"]
                #df_cluster["cong_norm"] = df_cluster["e_congestion"] / df_cluster["e_congestion"].max()
                # Correción 04/03/2021:
                df_cluster["cong_norm"] = np.where(df_cluster["e_congestion"]==0, 0.0, df_cluster["e_congestion"].min() / df_cluster["e_congestion"])
                    #df_cluster["e_congestion"].min() / df_cluster["e_congestion"]

                # Correccion 11/03/2021 Bonus
                df_cluster["bonus"] = np.where(df_cluster["e_congestion"] > self.congestion_threshold, 0,1)

                # Payoff
                df_cluster["payoff"] = df_cluster["cong_norm"] * self.weight_congestion + df_cluster["dist_norm"] * self.weight_distance + df_cluster["bonus"] * self.weight_threshold

                # Sort by payoff
                df_cluster = df_cluster.sort_values("payoff", ascending=False)

                # Iterate over rows in dataframe
                for index, row in df_cluster.head().iterrows():
                    target = (row["Latitude"], row["Longitude"])

                    place = Place(row["Name"], haversine(coordinates, target), target, row["payoff"], row["e_congestion"],
                                  w)
                    recommendation_list.append(place)
                    places_count -= 1
                    if places_count <= 0:
                        break

                if places_count <= 0:
                    break

        # sort by payoff
        newlist = sorted(recommendation_list, key=lambda x: x.payoff,  reverse=True)  # recomendation_list.sort(key=lambda x: x.payoff)

        return newlist

    def update_congestion(self, place):
        # Get cluster that contains the place
        df_current_cluster = self.cluster_data[place.cluster].query(
            "Latitude==" + str(place.Y) + " & " + "Longitude==" + str(place.X))

        for index, row in df_current_cluster.head().iterrows():
            self.cluster_data[place.cluster].at[index, "Congestion"] += 1

    def estimate_congestion(self, recommendation_list, level_k, precision):
        # Logit level k

        if level_k == 1:
            # level 0 player select randomly
            player_level_0_pick = recommendation_list[np.random.randint(len(recommendation_list), size=1)[0]]

            # Level 1 player try to maximizes its payoff
            for place in recommendation_list:
                # Add the utility to payoff
                place.utility = ((place.payoff) + place.congestion_level.value) + (
                            player_level_0_pick.payoff + player_level_0_pick.congestion_level.value)

                # Logit level
                place.model_probability = math.exp(precision * place.utility)

            newlist = sorted(recommendation_list, key=lambda x: x.model_probability, reverse=True)

            # Element with the highest utility
            return newlist[0]

        else:
            raise Exception("Only level_k=1 is available")