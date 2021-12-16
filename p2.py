import pandas as pd

placement = pd.DataFrame(columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))

indexx = 0
for p1 in ['quarry', 'factory', 'market']:
    indexx = indexx + 1
    for p2 in ['quarry', 'factory', 'market']:
        indexx = indexx + 1
        for p3 in ['quarry', 'factory', 'market']:
            indexx = indexx + 1
            for p4 in ['quarry', 'factory', 'market']:
                indexx = indexx + 1
                for p5 in ['quarry', 'factory', 'market']:
                    indexx = indexx + 1
                    for p6 in ['quarry', 'factory', 'market']:
                        indexx = indexx + 1
                        for p7 in ['quarry', 'factory', 'market']:
                            indexx = indexx + 1
                            for p8 in ['quarry', 'factory', 'market']:
                                indexx = indexx + 1
                                for p9 in ['quarry', 'factory', 'market']:
                                    indexx = indexx + 1
                                    for p10 in ['quarry', 'factory', 'market']:
                                        indexx = indexx + 1
                                        for p11 in ['quarry', 'factory', 'market']:
                                            indexx = indexx + 1
                                            for p12 in ['quarry', 'factory', 'market']:
                                                indexx = indexx + 1
                                                placement.loc[indexx] = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11,
                                                                         p12]

placement.to_csv('cases.csv')