

import pandas as pd
def remove_s(temp):
    idx_a = temp.find(',')

    temp = temp[0:idx_a - 1] + temp[idx_a:]
    return temp

if __name__ == '__main__':

    dict_t = {}

    dict_t[2] = ['label']
    dict_t[2].append('dog')

    cl = []
    cl.append(dict_t)

    print(cl)







def func(yolo):
  for z in yolo['label']:
        # Find number
        ctr = ctr + 1
        nums = [int(i) for i in z.split() if i.isdigit()]
        if z.count(',') >= 2:
            idx_a = z.find(',') - 1
            if nums[0] > 2: # Removes 's' from back of label due to plurality. Ex: persons -> person
                z = z[:idx_a] + z[idx_a + 1:]
            if nums[1] > 2:
                start_idx = idx_a + 2
                idx_c = z.find(',', start_idx)
                z = z[:idx_c] + z[idx_c + 1:]
            while nums[0] > 0:
                # remove string from back
                yolo.loc[ctr, 'label'] = z[0:z.find(',') + 1]
                nums[0] = nums[0] - 1
            while nums[1] > 0:
                # remove beginning string
                yolo.loc[ctr, 'label'] = z[z.find(',') + 1:]
                nums[1] = nums[1] - 1

        z = ''.join([i for i in z if not i.isdigit()])
        z = z.strip()
        # and (z.count(',') >= 2)
        z = str(z)
        if z in set_dlt:
            idx_drop.append(ctr)

