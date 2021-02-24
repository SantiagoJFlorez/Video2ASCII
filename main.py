#Librerías
import streamlit as st
import numpy as np
import skvideo.io as sk
import random
import os
from skimage import color
from skimage import color
from skimage import io
from PIL import Image
import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw
from sklearn.cluster import KMeans


#Funciones


##Función para cargar imagen

def load_image(imagen_file):
    img1=Image.open(imagen_file)
    return img1

##Función para k-means

def K_Means(_file,K):
    I = load_image(_file)
    I1 = np.asarray(I,dtype=np.float32)/255 
    #Para poder aplicar k-means necesitamos una matriz con tantas filas como píxeles y 
    #para cada fila/pixel 3 columnas, una para cada intensidad de color (rojo, verde y azul).
    #Extraemos cada canal por separado
    R = I1[:,:,0]
    G = I1[:,:,1]
    B = I1[:,:,2]
    #Convertimos las matrices en vectores y construímos la matriz de tres columnas descrita arriba.
    XR = R.reshape((-1, 1))  
    XG = G.reshape((-1, 1)) 
    XB = B.reshape((-1, 1)) 

    X = np.concatenate((XR,XG,XB),axis=1)
    #Agruparemos los 172388 colores en 3 grupos o nuevos colores, que se corresponderán con 
    #los centroides obtenidos con el k-means.
    k_means = KMeans(n_clusters=K)
    k_means.fit(X)

    #Los centroides finales son los nuevos colores y cada pixel tiene ahora una etiqueta que
    # dice a qué grupo o cluster pertenece. 
    centroides = k_means.cluster_centers_
    etiquetas = k_means.labels_
    #A partir de las etiquetas y los colores (intensidades de rojo, verde y azul) de los centroides 
    #reconstruimos la matriz de la imagen utilizando únicamente los colores de los centroides.
    m = XR.shape

    for i in range(m[0]):
        XR[i] = centroides[etiquetas[i]][0]
        XG[i] = centroides[etiquetas[i]][1] 
        XB[i] = centroides[etiquetas[i]][2]
    
    XR.shape = R.shape 
    XG.shape = G.shape
    XB.shape = B.shape 
    XR = XR[:, :, np.newaxis]  
    XG = XG[:, :, np.newaxis]
    XB = XB[:, :, np.newaxis]

    Y = np.concatenate((XR,XG,XB),axis=2)
    return Y


#Función Imagen

def imagen(_file,Clusters):
    st.markdown('**Imagen Cluster**')
    clust_imagen = K_Means (_file,Clusters)
    st.image(clust_imagen,width=1000,height=1000)

#Menu

def main():
    #Título
    st.title("""
    Colores de Imagen 
        """)

    menu=["Home","Imagen"]
    choice = st.sidebar.selectbox('Menu',menu)

    if choice == "Home":
        st.subheader("Home")
        st.write('Hola, que bueno que te encuentres aquí')
        st.markdown('**Si te gusta, has llegado al lugar indicado**')
        st.image(load_image('banner_sincl.jpg'))
        st.image(load_image('banner.jpg'))
        st.write('Imagen con 3 Clusters')

    elif choice == "Imagen":
        st.subheader("Imagen")
        #Subida del archivo
        _file = st.file_uploader(' Sube aquí tu imagen, omite el error',type='jpg')
        if _file is not None:
            #slider Clusters
            Clusters = st.slider('Cuántos Clusters?',2,7,2)
            st.write('Recuerda que entre mayor resolución tenga la imagen, más demorará...')
            #Imprime el original
            st.markdown('**Imagen Original**')
            st.image(load_image(_file),width=1000,height=1000)
            imagen(_file,Clusters)

if __name__ == '__main__':
    main()

