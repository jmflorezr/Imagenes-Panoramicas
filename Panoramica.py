import cv2
import sys
import os
import numpy as np


Norbey Marin.
Julian Mauricio Florez

"""este metodo devuelve la concatenacon de 2 imagenes"""
def concatImagen(img1, img2):
    return cv2.hconcat([img1, img2])# concatena 2 imagenes de manera Horizontal

"""este metodo se encarga de  tomar las imagenes concatenadas, dibuja los puntos
    devuelve una imagen con los puntos, y una lista con los puntos seleccionados"""
def tomarPunto(idImg, image_draw, colorPunto):
    points = []
    def click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
    cv2.namedWindow(idImg)
    cv2.setMouseCallback(idImg, click)
    points1 = []
    point_counter = 0
    while True:
        cv2.imshow(idImg, image_draw)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("x"):
            points1 = points.copy()
            points = []
            break
        if len(points) > point_counter:
            point_counter = len(points)
            cv2.circle(image_draw, (points[-1][0], points[-1][1]), 3, colorPunto, -1)
    cv2.destroyWindow(idImg) #una vez selecionados los puntos cierra la imagen
    return image_draw, points1 # retorna la imagen con los puntos y los puntos

""" ------------------------------------------------------------------------------------------------------- """
if __name__ == '__main__':
    path = sys.argv[1]
    contenido = os.listdir(path) # obtiene lista con las imagenes que estan disponibles
    dic_img = {}# crea diccionario para identificar las imagenes
    red = [0, 0, 255] #color para pintar puntos
    blue = [255, 0, 0]#color para pintar puntos
    listaTransformaciones = []# aqui se guardan las trasformaciones de las imagenes. 1y2 2y3...n-1 y n
    # Este for llena el diccionario con el nombre de las imagnes
    for i in range(len(contenido)):
        dic_img[i] = contenido[i]

    # imprime id de imagenes para que el usuario seleccione
    print("Imagnes disponibles")
    for i in range(len(dic_img)):
        print(i, dic_img[i])

    sel = int(input( "¿cual imagen desea usar como referencia? " ))# eleccion de imagen
    listImgConcat = [] #aqui van a estar todas las imagenes concatenadas
    """este for concatena las imagenes 0y1, 1y2.....N-1 y N
    y las almacena en una lista"""
    for i in range(0, len(dic_img)-1):
        img1 = cv2.imread(path + '\\' + dic_img[i])# lee la imagen1
        img2 = cv2.imread(path + '\\' + dic_img[i+1])# lee la imagen1
        listImgConcat.append(concatImagen(img1, img2)) #adiciona la imagen concatenada a una lista

    #se visualiza cada una de las imagenes concatenadas, se elijen 4 puntosdel objeto de ref

    punto1 = []
    punto2 = []
    punt2=[]
    y = listImgConcat[0].shape[0] #obtiene el tamaño en y de la imagen
    x = (listImgConcat[0].shape[1]) / 2#obtiene el tamaño en x de la imagen

    cant = len(listImgConcat) #cantidad de imagenes concatenadas
    """en este for se van a visualizar todas las imagenes concatenadas
    y el usuario va a pintar los puntos rojos y luego los azules"""
    for i in range(len(listImgConcat)):
        idImg = "Imagen concatenada " + str(i) #Identifica cada una de las imagenes
        img, punto1 = tomarPunto(idImg, listImgConcat[i], red) #llama al metodo que pinta rojo
        print("Punto 1 seleccionado ", i, "/", cant, "--->  ", punto1)

        img, punt2 = tomarPunto(idImg, img, blue) #Llama al metodo que pinta Azul

        for j in range(len(punt2)):
            pt2 = punt2[j][0]-x, punt2[j][1] # compensa ancho de la imagen derecha
            punto2.append(pt2)

        print("Punto 2 seleccionado ", i, "/", cant, "--->  ", punto2)
        cv2.waitKey(1)
        N = min(len(punto1), len(punto2))
        assert N >= 4, 'At least four points are required'

        pts1 = np.array(punto1[:N])
        pts2 = np.array(punto2[:N])
        H, _ = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)

        image_warped = cv2.warpPerspective(img1, H, (img1.shape[1], img1.shape[0]))
        listaTransformaciones.append(image_warped) #agrega la trasformacion a la lista
        #cv2.imshow("Image", img1)
        #cv2.imshow("Imagen", img2)
        cv2.imshow("Image warped",image_warped)
        image_warped.astype(np.float)
        cv2.waitKey(0)


    print("se realizaron ", len(listaTransformaciones), "trasformaciones")

    """ aqui creo una panoramica con las imagenes disponibles------------------------"""
    images = [] # esta lista va a contener todas las imagenes que hay en el directorio
    for i in range(0, len(dic_img)):
        im1 = cv2.imread(path + '\\' + dic_img[i])# lee la imagen
        images.append(im1)# agrega la imagen

    stitcher = cv2.Stitcher.create() #crea el stitcher
    (status, result) = stitcher.stitch(images)# recibe las imagenes y crea la panoramica

    if (status == cv2.STITCHER_OK): #verifica que este bien
        print("panoramica  generado")
    else:
        print("panorama no generado")

    cv2.imshow("panoramica buscada", result) #muestra la panoramica
    cv2.waitKey(0)


    cv2.destroyAllWindows( )