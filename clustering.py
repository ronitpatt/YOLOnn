
import pandas as pd
import statistics
import numpy as np

if __name__ == '__main__':
    yolo = pd.read_csv('/Users/ronitp/Documents/PycharmProjects/YoloParser/YOLO_PARSED_2500.csv')
    # Reindex CSV file after dropped columns
    print(yolo.shape)
    drop_cols = ['Unnamed: 0', 'index']
    yolo.drop(drop_cols, axis=1, inplace=True)
    print(yolo.head(5))
    unique_trips = list(yolo.trip.unique())

    yolo.astype({'timestamp': 'int32'})
    df_list = []

    cluster_dict = {}

    # Use List as Clustering Data Type (Non Static Array Size)

    for trip in unique_trips:
        # Make new DataFrame for each unique trip

        yolo_t = yolo[yolo.trip == trip]

        yolo_t.reset_index(inplace=True)
        dim = yolo_t.shape
        print('DIMENSIONS : ', int(dim[0]) - 1)
        last_idx = yolo_t.last_valid_index()
        tst_param = 1000
        # group by timestamp
        lst_ts_unique = list(yolo_t.timestamp.unique())

        idx_unique = []
        for ts in lst_ts_unique:
            temp_first = (np.where(yolo_t["timestamp"] == ts))
            temp_sec = np.array(temp_first[0]).tolist()
            idx_unique.append(temp_sec)
        # for i in range(0, int(dim[0]) - 1):
        # print(idx_unique)
        print(yolo_t.loc[1]['timestamp'])
        st = [2, 3]
        print(yolo_t.loc[st]['timestamp'])

        # Every 1000 frames

        # Clustering List =
        cluster_temp = []
        # for x in range(0, len(idx_unique)):
        for i in range(0, int(dim[0]) - 1):
            nxt_idx = i + 1
            #  print(idx_unique[x])
            # i = (int(k) for k in idx_unique[x])
            #  nxt_idx = (int(q) for q in idx_unique[x + 1])
            #   i = idx_unique[x][0]
            #  nxt_idx = idx_unique[x+1][0]

            print(i)
            print(nxt_idx)

            # if yolo_t.loc[i]['timestamp'] == yolo_t.loc[nxt_idx]['timestamp']:
            # continue

            if yolo_t.loc[nxt_idx]['timestamp'] - yolo_t.loc[i]['timestamp'] >= tst_param:
                if yolo_t.loc[nxt_idx]['label'] != yolo_t.loc[i]['label']:
                    # Drop Row
                    yolo_t = yolo_t.drop(i, axis=0)
                    continue
                # Do not need else will automatically loop back to next i
                else:
                    continue

            bool_drop = True

            while yolo_t.loc[nxt_idx]['timestamp'] - yolo_t.loc[i]['timestamp'] < tst_param:

                if str(yolo_t.loc[nxt_idx]['label']) == str(yolo_t.loc[i]['label']):
                    # Exit While loop
                    bool_drop = False
                    break
                else:
                    nxt_idx = nxt_idx + 1

                if nxt_idx == last_idx + 1:  # Special case when loop reaches end of dataframe
                    break

            if bool_drop:
               # lst_drop = []
              #  ts_target = yolo_t.loc[i]["timestamp"]
               # ts = np.where(yolo_t["timestamp"] == ts_target)
                yolo_t = yolo_t.drop(i, axis=0)
            # If reaches here Drop Row
        df_list.append(yolo_t)
        cluster_dict[trip] = cluster_temp
    res = pd.concat(df_list)
    print('SHAPE')
    print(res.shape)
    res.to_csv('res_cluster_small.csv')
    #yolo.to_csv('Clustering_testing.csv')



        # Loop through each label and see if it is in the next timestamp


