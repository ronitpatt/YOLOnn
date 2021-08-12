for z, i in zip(yolo2['label'].items(), idx_tst):
    # z = str(yolo2.loc[i, 'label'])
    #
    # 3 persons, 2 dogs
    # 1 person, 2 dogs
    z = str(z)
    print(z)
    nums = [int(i) for i in z.split() if i.isdigit()]
    idx_a = z.find(',') - 1
    if nums[0] > 1:  # Removes 's' from back of label due to plurality. Ex: persons -> person
        z = z[:idx_a] + z[idx_a + 1:]
        print('FAIL')
    if nums[1] > 1:
        start_idx = idx_a + 2
        idx_c = z.find(',', start_idx)
        z = z[:idx_c] + z[idx_c + 1:]
        print('FAIL')
    # if nums[2]
    ctr = i
    while nums[0] > 0:
        # remove string from back
        yolo.loc[ctr, 'label'] = z[0:z.find(',') + 1]
        nums[0] = nums[0] - 1
        ctr = ctr + 1
        print(z[0:z.find(',') + 1])
    while nums[1] > 0:
        # remove beginning string
        yolo.loc[ctr, 'label'] = z[z.find(',') + 1:]
        nums[1] = nums[1] - 1
        ctr = ctr + 1
        print(z[z.find(',') + 1:])
    # if while nums2