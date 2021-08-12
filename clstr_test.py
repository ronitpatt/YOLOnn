import pandas as pd
import statistics
import numpy as np

if __name__ == '__main__':
    yolo = pd.read_csv('/Users/ronitp/Documents/PycharmProjects/YoloParser/YOLO_PARSED_small.csv')
    # Reindex CSV file after dropped columns
    yolo['label'] = yolo['label'].str.strip()
    print(yolo.shape)
    # drop_cols = ['Unnamed: 0', 'index']
    drop_cols = ['Unnamed: 0']
    yolo.drop(drop_cols, axis=1, inplace=True)
    print(yolo.head(5))
    unique_trips = list(yolo.trip.unique())

    yolo.astype({'timestamp': 'int32'})
    df_list = []

    # Use List as Clustering Data Type (Non Static Array Size)
    dict_trips = {}
    for trip in unique_trips:
        # Make new DataFrame for each unique trip

        yolo_t = yolo[yolo.trip == trip]

        yolo_t.reset_index(inplace=True)
        dim = yolo_t.shape
        print('DIMENSIONS : ', int(dim[0]) - 1)
        last_idx = yolo_t.last_valid_index()
        # IMPORTANT : Variable dictating hyper-parameter for clusters
        tst_param = 1000
        # group by label
        lbl_group = yolo_t.label.unique()

        dict_occur = {}
        # Find indices of each unique label in trip dataframe
        for lbl in lbl_group:
            temp_first = (np.where(yolo_t["label"] == lbl))
            temp_sec = np.array(temp_first[0]).tolist()
            dict_occur[lbl] = temp_sec

       # print(dict_occur)
        dict_fin = {}  # dict_fin = dictionary of labels and corresponding timestamps for labels
        clusters = []
       # timestamps = []


        for key, value in dict_occur.items():
           # value[0] = yolo.loc[value[0]]['timestamp']
            dict_fin[key] = list((yolo_t.loc[value]['timestamp']))

            clstr_temp = []
            dict_clusters = {}
           final_flag = False
            for idx in range(1, len(dict_fin[key])):
                prev_idx = idx - 1
                prev_prev_idx = prev_idx - 1 # Look deeper into this # Might have to start loop at 2 index
                # dict_fin[key][prev_idx] outputs a timestamp

                # Think about last cluster?
                # Various Cases below:
                # 
                if dict_fin[key][prev_idx] == dict_fin[key][len(dict_fin[key]) - 1]:
                    if final_flag:

                    break
                # Make special case for first index
                elif dict_fin[key][idx] - dict_fin[key][prev_idx] < tst_param:
                    clstr_temp.append(dict_fin[key][prev_idx])
                    final_flag = True

                elif dict_fin[key][prev_idx] - dict_fin[key][prev_prev_idx] < tst_param:
                    clstr_temp.append(dict_fin[key][prev_idx])
                    dict_clusters[key] = clstr_temp
                    clusters.append(dict_clusters)
                    dict_clusters = {}
                    clstr_temp = []
                else:
                    dict_clusters[key] = clstr_temp
                    clusters.append(dict_clusters)
                    clstr_temp = []
                    dict_clusters = {}
                    dict_clusters[key] = dict_fin[key][prev_idx]
                    clusters.append(dict_clusters)
                    dict_clusters = {}

      #  print(clusters)
            # If reaches here Drop Row
       # df_list.append(yolo_t)
        dict_trips[trip] = clusters
    #res = pd.concat(df_list)
    #print('SHAPE')
    #print(res.shape)
    #res.to_csv('res_cluster_small.csv')
    print(dict_trips)
    print('RAN SUCCESSFULLY : 0 ERRORS')
    # yolo.to_csv('Clustering_testing.csv')

    # Loop through each label and see if it is in the next timestamp


