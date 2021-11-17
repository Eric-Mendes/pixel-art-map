# pixel-art-map
Este código mostra um mapa para uma pixel art de qualquer imagem no minecraft.

![Screenshot from 2021-11-16 20-57-54](https://user-images.githubusercontent.com/42689328/142089983-a6928eda-d1be-42cf-ae2e-3733794a7019.png)
## Como funciona
1. Crio um array 2d onde cada célula contém a tupla RGB para cada pixel da imagem;
2. Carrego blocks.json em um dataframe. Nele eu tenho a informação do RGB com que cada bloco fica ao ser olhado em um mapa;
3. Abstraio as tuplas RGB como um ponto no espaço com x, y e z;
4. Por fim calculo a menor distância euclidiana entre a tupla do pixel e a tupla de cada conjunto de blocos para decidir qual bloco usar para representar um determinado pixel.
