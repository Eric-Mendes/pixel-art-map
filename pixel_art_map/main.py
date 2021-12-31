from math import sqrt

import numpy as np
import pandas as pd
from PIL import Image


def distance(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

df_blocks = pd.read_json("./blocks.json")
df_blocks.drop([0], inplace=True)

def decide_color(pxl):
    df_blocks['distance'] = df_blocks['rgb'].apply(lambda rgb: distance([int(i) for i in rgb], pxl))

    df_blocks.sort_values(by='distance', inplace=True)
    print(df_blocks.iloc[0])
    return df_blocks.iloc[0]['blocks']


img = Image.open(r'./cbf.png').convert("RGB")
img = img.resize((img.size[0]//4, img.size[1]//4))
arr = np.array(img)

result = []
for row in arr:
    r = []
    for col in row:
        dc = decide_color(col)
        r.append(dc)
    result.append(r)


pd.DataFrame(result).to_csv(path_or_buf="creeper_head.csv", index=False, header=False)
