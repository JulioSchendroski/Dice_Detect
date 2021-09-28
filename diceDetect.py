import numpy as np
import cv2 as cv

img = cv.imread('C:\\Codes\\ifsp_ic_julio\\2021-16-08\\Imagens\\dice.jpg')

def imageProcess (src, medianBlur, threshValue,flag): #Processamento da imagem para retirar apenas as infromações necessárias, como os pontos do dado, ou apenas seu contorno externo
    imgGray = cv.cvtColor(src,cv.COLOR_BGR2GRAY) 
    blur = cv.medianBlur(imgGray,medianBlur)
    _,bin = cv.threshold(blur,threshValue,255,flag)
    return bin #Retorna a imagem binarizada

def blobFinder(blob,dst): #Detector de Blob (circulos e bolhas) na imagem
    detectObj = cv.SimpleBlobDetector_create() #Define a um objeto um método de identificar circulos
    keyPoints = detectObj.detect(blob) #Define-se quais serão os pontos chaves na imagem já processada
    blobs = cv.drawKeypoints(dst, keyPoints,np.array([]),(0,0,255),cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) #contorna-se na imagem original os pontos identificados
    cv.putText(blobs,("Quantidade total de pontos : ")+str(len(keyPoints)),(15,60),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv.LINE_AA)
    return blobs


def contourFinder(src,dst,measure):
    conts,_ = cv.findContours(src,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE) #Identifica os contornos na imagem
    cv.drawContours(dst,conts,-1,(0,255,255),2)
    cv.putText(dst,("Quantidade de dados : ")+str(len(conts)),(15,25),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,255),1,cv.LINE_AA)
    for cont in conts:
        M = cv.moments(cont) #Função para determinar o centro dos objetos, através de momento
        cx = int(M['m10']/M['m00']) #Identifica o centro do objeto nas abscissas
        cy = int(M['m01']/M['m00']) #Identifica o centro do objeto nas ordenadas
        center = (cx,cy)
        form = cv.isContourConvex(cont) #Verifica se o contorno é convexo, utilizado para verificar se é aberto ou fechado 
        area = cv.contourArea(cont) #Atribui-se a medida de aréas de objetos fechados
        perimeter = cv.arcLength(cont,True) #Perimetro de objetos fechados, definido por True
        if form is True:
            print("There's an open contour!") #Caso há contorno aberto
        elif (area > measure):
            cv.putText(img,"Area: {0:2.1f}".format(area),center,cv.FONT_HERSHEY_SIMPLEX,1,(232, 60, 37),3)
            cv.putText(img,"Perimeter: {0:2.1f}".format(perimeter),(cx,cy+30),cv.FONT_HERSHEY_SIMPLEX,1,(232, 60, 37),3)
            print(area)
            print(perimeter)
            print()
        



PipeFinder = imageProcess(img,19,12,cv.THRESH_BINARY_INV)
contourFinder(PipeFinder,img,10)




imgCont = imageProcess(img,19,210,cv.THRESH_BINARY)
#210 - identifica os 5 dados e uma área desejada, 220 -  identifica apenas 2 dados com área pequena, 200 - com áreas juntas
imgBlob = imageProcess(img,13,12,cv.THRESH_BINARY_INV)
contourFinder(imgCont,img,8000)
blob = blobFinder(imgBlob,img)

cv.imwrite('Dados Processados.jpg',blob)




cv.imshow("Resultado",blob)
cv.waitKey(0)


