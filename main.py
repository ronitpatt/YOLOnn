# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import pandas as pd
import statistics
import numpy as np

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def remove_s(temp):
    idx_a = temp.find(',')

    temp = temp[0:idx_a - 1] + temp[idx_a:]
    return temp


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    yolo = pd.read_csv('/Users/ronitp/Downloads/Yolo_singlefile.csv')
   # start = 2500
  #  end = 2585
  #  yolo = yolo.iloc[start:end, ]
  #  yolo.reset_index(inplace=True)
    yolo.astype({'timestamp': 'int32'})

    lbl = yolo['label']
    #print('Label before parsing : ', yolo.loc[42]['label'])
    set_lbl = set(lbl)
    # print(yolo.head())

    # Start Row Idx : 165581


    print(yolo.head)
    print(yolo.shape)

    lst_lbl = []
    for i in set_lbl:
        i = i[7:]  # Parses out 480x640 header of label
        lst_lbl.append(i)

    full_lbl = []

    for x in lst_lbl:

        full_lbl.extend(x.split(','))

    full_lbl_set = set(full_lbl)
    # print(full_lbl_set)

    full_lbl_lst = list(full_lbl_set)  # List of all unique labels with number

    # All Unique Labels without Numbers:
    lbl_alpha = []
    for x in full_lbl_lst:
        x = ''.join([i for i in x if not i.isdigit()])
        lbl_alpha.append(x)

    lbl_alpha_set = set(lbl_alpha)

    lbl_alpha_lst = list(lbl_alpha_set)  # List of all unique labels without number

    # Focus on multiple value labels
    # split by driver
    # Output lowest confidence modules

    set_dlt = ["buss,", "boat,", "cow,", "bicycle,", "wine glass,", "wine glasss",
               "toilet,", "cake,", "sinks,", "horse,", "airplane,", "train,", "cow,",
               "sheep,", "mouse,", "apple,", "bird,", "tv,", "elephant,", "donut,", "skis,",
               "bear,", "fire hydrant,", "potted plant,", "surfboard,", "toothbrush,",
               "dining table,", "bird,", "snowboard,", "zebra,", "broccoli,", "frisbee,",
               "baseball glove,", "teddy bear,", "giraffe", "cat", "banana"]

    # Deleting bad data from dataframe
    yolo['label'] = yolo['label'].str.replace('480x640', '')  # Removes Header

    print('Initial Dimensions: ', yolo.shape)

    # Calculating Confidence Values Per Label
    yolo['confidence'] = yolo['confidence'].str.replace( "tensor\("  , '')
    yolo['confidence'] = yolo['confidence'].str.replace(", device='cuda:0'\)" , '')

    #   unique_lbl = list(yolo.label.unique())
    idx_sing_plural = []
    # Ex: 2 persons -> 2 person
    for num in range(2, 5):
        idx_sing_plural_temp = np.where(yolo["label"].str.count(str(num)) > 0)
        idx_temp_lst = np.array(idx_sing_plural_temp[0]).tolist()
        idx_sing_plural.extend(idx_temp_lst)

    for i in idx_sing_plural:
        temp = str(yolo.loc[i, 'label'])
        if temp.count(',') < 2:
            yolo.loc[i, 'label'] = remove_s(yolo.loc[i, 'label'])

    # idx_split = yolo[yolo['label'].count(',') >= 2].index.tolist()
    idx_split = (np.where(yolo["label"].str.count(',') > 1))
    idx_mult = np.array(idx_split[0]).tolist()
    idx_fin = []
    for g in idx_mult:
        j = yolo.loc[g, 'timestamp']
        k = yolo.loc[g - 1, 'timestamp']
        if j != k:
            idx_fin.append(g)

    # yolo_test = yolo.iloc[idx_tst, :]
    for idx in idx_fin:
        ctr = idx
        z = str(yolo.loc[ctr, 'label'])
        nums = [int(i) for i in z.split() if i.isdigit()]
        plural = []
        for i in range(0, len(nums)):
            if nums[i] > 1:
                plural.append(True)
            else:
                plural.append(False)
        while nums[0] > 0:
            # remove string from back
            if plural[0]:
                yolo.loc[ctr, 'label'] = remove_s(z[0:z.find(',') + 1])
            else:
                yolo.loc[ctr, 'label'] = z[0:z.find(',') + 1]
            nums[0] = nums[0] - 1
            ctr = ctr + 1

        while nums[1] > 0:
            # remove beginning string
            idx_a = z.find(',')
            idx_b = z.find(',', z.find(',') + 1)
            if plural[1]:
                yolo.loc[ctr, 'label'] = remove_s(z[idx_a + 1: idx_b + 1])
            else:
                yolo.loc[ctr, 'label'] = z[idx_a + 1: idx_b + 1]
            nums[1] = nums[1] - 1
            ctr = ctr + 1

        if len(nums) > 2:
            while nums[2] > 0:
                idx_c = z.find(',', idx_b + 1)
                if plural[2]:
                    yolo.loc[ctr, 'label'] = remove_s(z[idx_b + 1: idx_c + 1])
                else:
                    yolo.loc[ctr, 'label'] = z[idx_b + 1: idx_c + 1]
                nums[2] = nums[2] - 1
                ctr = ctr + 1
        if len(nums) > 3:
            while nums[3] > 0:
                if plural[3]:
                    yolo.loc[ctr, 'label'] = remove_s(z[idx_c + 1:])
                else:
                    yolo.loc[ctr, 'label'] = z[idx_c + 1:]
                nums[3] = nums[3] - 1
                ctr = ctr + 1

    for i in range(2, 5):
        yolo['label'] = yolo['label'].str.replace(str(i), str(1))



    #    print(yolo['label'].value_counts())
    #  print(type(yolo['label'].value_counts()))
    # Confidence Value Calculations
    group = yolo.groupby('label')
    # print counts of values [object : value] key data pair
    yolo_con = group.apply(lambda u: u['confidence'].unique())

    con_dic = {}  # Dictionary of labels and their respective average confidence values
    for i, v in yolo_con.items():
        con_lst = [float(x) for x in v]
        con_dic[i] = statistics.mean(con_lst)

    con_dic_sorted = sorted(con_dic.items(), key=lambda w: w[1], reverse=True)
    #print(con_dic_sorted)

    # Dropping Bad Labels Below

    for dlt in set_dlt:
        yolo = yolo[~yolo.label.str.contains(dlt)]

   # yolo = yolo[~yolo['label'].isin(set_dlt)]
    # Calculate Confidence Values here
    print('Final Dimensions : ', yolo.shape)
    print(yolo.head)

    #print('Label After Parsing : ', yolo.loc[0]['label'])

    yolo.to_csv('YOLO_PARSED_July_v1.csv')

    unique_trips = list(yolo.trip.unique())
    unique_trips.sort()
    # print(unique_trips)
    print('Length of unique trips', len(unique_trips))

    #  for i in unique_trips:
    yolo_trip = yolo.loc[yolo['trip'] == i]
    un_lbl_trip = list(yolo_trip.trip.unique())

    #for j in un_lbl_trip:
        # find first instance of j
        # Then check if its in the next 10
        # if not delete


 #   yolo['label'] = yolo['label'].str.replace("airplanes", "airplane")
 #   yolo['label'] = yolo['label'].str.replace("birds", "bird")
 #   yolo['label'] = yolo['label'].str.replace("boats", "boat")
 #   yolo['label'] = yolo['label'].str.replace("bottles", "bottle")
 #   yolo['label'] = yolo['label'].str.replace("bowls", "bowl")
 #   yolo['label'] = yolo['label'].str.replace("buss", "bus")
 #   yolo['label'] = yolo['label'].str.replace("cars", "car")
 #   yolo['label'] = yolo['label'].str.replace("cell phones", "cell phone")
 #   yolo['label'] = yolo['label'].str.replace("chairs", "chair")
 #   yolo['label'] = yolo['label'].str.replace("clocks", "clock")
 #   yolo['label'] = yolo['label'].str.replace("cows", "cow")
 #   yolo['label'] = yolo['label'].str.replace("cups", "cup")
  #  yolo['label'] = yolo['label'].str.replace("donuts", "donut")
  #  yolo['label'] = yolo['label'].str.replace("elephants", "elephant")
  #  yolo['label'] = yolo['label'].str.replace("keyboards", "keyboard")
  #  yolo['label'] = yolo['label'].str.replace("mouses", "mouse")
  #  yolo['label'] = yolo['label'].str.replace("parking meters", "parking meter")
  #  yolo['label'] = yolo['label'].str.replace("persons", "person")
   # yolo['label'] = yolo['label'].str.replace("sheeps", "sheep")
    #yolo['label'] = yolo['label'].str.replace("sinks", "sink")
 #   yolo['label'] = yolo['label'].str.replace("skiss", "skis")
 #   yolo['label'] = yolo['label'].str.replace("suitcases", "suitcase")
  #  yolo['label'] = yolo['label'].str.replace("ties", "tie")
  #  yolo['label'] = yolo['label'].str.replace("toilets", "toilet")
  #  yolo['label'] = yolo['label'].str.replace("traffic lights", "traffic light")
  #  yolo['label'] = yolo['label'].str.replace("trains", "train")
 #   yolo['label'] = yolo['label'].str.replace("trucks", "truck")
 #   yolo['label'] = yolo['label'].str.replace("umbrellas", "umbrella")
#    yolo['label'] = yolo['label'].str.replace("vases", "vase")
#    yolo['label'] = yolo['label'].str.replace("wine glasss", "wine glass")


    print_hi('PyCharm')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
