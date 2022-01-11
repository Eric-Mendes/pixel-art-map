import json
import os
import urllib.request
from collections import Counter
from configparser import ConfigParser
from contextlib import suppress
from math import sqrt

import numpy as np
import pandas as pd
import validators
from PIL import Image


def script(df, **kwargs):
    player_pos = [
        kwargs.get("player_x", 0),
        kwargs.get("player_y", 0),
        kwargs.get("player_z", 0),
    ]
    z = (df != df.shift()).cumsum()
    zri = z.reset_index()
    ix_name = z.index.name
    co_name = z.columns.name
    for i in z:
        v = zri.groupby(i)[ix_name].agg(["first", "last"])
        s = {co_name: i}
        e = {co_name: i}
        for _, r in v.iterrows():
            s[ix_name] = r["first"]
            e[ix_name] = r["last"]
            material = df.loc[r["first"], i]
            yield f'fill {s["x"] + player_pos[0]} {0 + player_pos[1]} {s["z"] + player_pos[2]} {e["x"] + player_pos[0]} {0 + player_pos[1]} {e["z"] + player_pos[2]} {material.split(",")[0].strip()}'


if __name__ == "__main__":
    config_parser = ConfigParser()
    config_parser.read("pixel_art_map/config.ini")
    default_configs = config_parser["DEFAULT"]

    def distance(p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

    df_blocks = pd.read_json("./blocks_treated.json")
    df_blocks.drop([0], inplace=True)

    def decide_color(pxl):
        df_blocks["distance"] = df_blocks["rgb"].apply(
            lambda rgb: distance([int(i) for i in rgb], pxl)
        )

        df_blocks.sort_values(by="distance", inplace=True)
        return df_blocks.iloc[0]["blocks"]

    image_name = default_configs["image"]
    if validators.url(image_name):
        urllib.request.urlretrieve(image_name, f"images/{os.path.split(image_name)[1]}")
        image_name = os.path.split(image_name)[1]

    img = Image.open(f"images/{image_name}").convert("RGB")

    FACTOR = int(default_configs["factor"])
    img = img.resize((img.size[0] // FACTOR, img.size[1] // FACTOR))
    arr = np.array(img)

    result = []
    for row in arr:
        r = []
        for col in row:
            dc = decide_color(col)
            r.append(dc)
        result.append(r)

    image_name = os.path.splitext(image_name)[0]  # same as above but without extension
    with suppress(FileExistsError):
        os.mkdir(f"output/{image_name}")

    df = pd.DataFrame(result)
    df.to_csv(path_or_buf=f"output/{image_name}/map.csv", index=False, header=False)

    txt = "All blocks used\n".title()
    arr = df.to_numpy().flatten()
    all_blocks = {
        key.split(",")[0].strip(): val for key, val in dict(Counter(arr)).items()
    }

    txt += f"{json.dumps(all_blocks, indent=4)}\n"
    txt += "-" * 30
    txt += "\nBlocks used per column:"

    for i, col in enumerate(df.columns):
        txt += f"\nColumn {i+1}.\n"
        txt += f"{json.dumps({key.split(',')[0].strip(): val for key, val in dict(Counter(df[col])).items()}, indent=4)}\n"
        txt += "-" * 30

    with open(f"output/{image_name}/metadata.txt", "w") as file:
        file.write(txt)

    pack_mcmeta = {
        "pack": {
            "pack_format": 8,
            "description": f"This datapack will generate the image ({image_name}) in your world",
        }
    }
    load_json = {"values": ["pixelart-map:load"]}
    tick_json = {"values": ["pixelart-map:tick"]}

    datapack_path = f"output/{image_name}/datapack/{image_name}-PAM"

    with suppress(FileExistsError):
        os.makedirs(f"{datapack_path}/data/minecraft/tags/functions")
        os.makedirs(f"{datapack_path}/data/pixelart-map/functions")

    with open(f"{datapack_path}/pack.mcmeta", "w") as file:
        file.write(json.dumps(pack_mcmeta, indent=4))
    with open(f"{datapack_path}/data/minecraft/tags/functions/load.json", "w") as file:
        file.write(json.dumps(load_json, indent=4))
    with open(f"{datapack_path}/data/minecraft/tags/functions/tick.json", "w") as file:
        file.write(json.dumps(tick_json, indent=4))

    with open(
        f"{datapack_path}/data/pixelart-map/functions/tick.mcfunction", "w"
    ) as file:
        file.write("")

    # label the axes
    df = df.rename_axis(index="z", columns="x")

    # select which axis to make major
    a = list(
        script(
            df,
            player_x=int(default_configs["player_x"]),
            player_y=int(default_configs["player_y"]),
            player_z=int(default_configs["player_z"]),
        )
    )
    b = list(
        script(
            df.T,
            player_x=int(default_configs["player_x"]),
            player_y=int(default_configs["player_y"]),
            player_z=int(default_configs["player_z"]),
        )
    )
    res = min([a, b], key=len)
    with open(
        f"{datapack_path}/data/pixelart-map/functions/load.mcfunction", "w"
    ) as file:
        file.write("\n".join(res))
