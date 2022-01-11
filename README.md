# pixel-art-map
> Special thanks to everyone that contributed to the commands file feature @ https://stackoverflow.com/questions/70512775/how-to-group-elements-in-dataframe-by-row/70546452#70546452

Maps an image to a minecraft pixel art.

![Screenshot from 2021-11-16 20-57-54](https://user-images.githubusercontent.com/42689328/142089983-a6928eda-d1be-42cf-ae2e-3733794a7019.png)
## Setting up the development environment
Assuming you have `python >= 3.9` and `pipenv` installed:
```bash
# Cloning the repo 
git clone https://github.com/Eric-Mendes/pixel-art-map.git
cd pixel-art-map/

# Opening the environment and installing the dependencies
pipenv shell
pipenv install
```
##  Running the project
Essentially all you need is to get your image ready and tweak the parameters on the `pixel_art_map/config.ini` file. No manipulation of the `main.py` file is necessary.

1. Get any image you want and put it inside the `images/` folder <strong>OR</strong> copy the url of an image on the internet;

    - <strong>IMPORTANT:</strong> passing an url will download the image into the `images/` folder. If you think that some url looks sketchy, do <strong>not</strong> use it.

2. Correctly pass the path or the url to the image string: 

    - `image=naruto.png` <strong>or</strong>
    - `image=https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png` (*just an example of an url*)

3. Lower the dimensions a little by a factor (<strong>a big pixel art takes a long time to build. Naruto's was made automatically and it took around 3 hours</strong>):

    - `factor=15`

        - *What's the best factor for your image? You have to find that out by trying different numbers when you resize it.

4. `player_x`, `player_y` and `player_z`: the player's position.

5. `auto_build` assumes True or False. By default it is False, which means: do not build automatically.

6. From source, run the code (keep in mind that you need to be inside the pipenv shell):
```bash
python3 pixel_art_map/main.py
```
The output will be inside the `output/` folder and it'll be another folder with the same name of your image. This folder should contain a `map.csv` file where each cell corresponds to a block. Place the blocks by going cell by cell and in the end you'll have your pixel art.
The folder will also have a `metadata.txt` file with metadata about the pixel art, such as a total of all the blocks you'll use and a total by column of the blocks you'll use in them, so that you know how to organize your inventory. Besides that, a `commands.txt` file will also be generated and it will contain the minecraft commands to generate the pixel art quicker than placing the blocks by hand.

## How the code works
1. A 2D array is made with each cell correponding to a pixel and its value as that pixel's RGB tuple;
2. I load blocks.json in a DataFrame. In it is the information of the RGB color that each block assume when looked at in a map.
3. I abstract the RGB tuples as a point in a 3D space with x, y and z;
4. In the end I calculate the lowest euclidian distance between a pixel's tuple and each blocks tuple to decide which block to use to determine which block to use to represent that pixel.
