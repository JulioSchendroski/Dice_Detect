import numpy as np
import cv2 as cv

img = cv.VideoCapture('http://192.168.15.108:8080/video') #Atribui ao objeto uma url para leitura de video, conectado com o Ipv4 da rede

while True:
    #Processamento da imagem para obter apenas os pontos de interesse, utilizando binarização
    _,frame = img.read() #Faz a leitura da imagem recebida pela url
    resized = cv.resize(frame,(600,400))
    imgGray = cv.cvtColor(resized,cv.COLOR_BGR2GRAY)
    blur = cv.medianBlur(imgGray,19)
    _,bin = cv.threshold(blur,120,255,cv.THRESH_BINARY)

    #Detecção dos pontos de interesse do dado, utilizando Blob para determinar a pontuação do dado
    detectObj = cv.SimpleBlobDetector_create()
    keyPoints = detectObj.detect(bin)
    blob = cv.drawKeypoints(resized,keyPoints,np.array([]),(0,0,255),cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv.putText(blob,("Points : ")+str(len(keyPoints)),(15,60),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1,cv.LINE_AA)

    #Definir os contornos do dado para realizar a contagem do numero total de dados na câmera
    conts,_ = cv.findContours(bin,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(blob,conts,-1,(0,255,255),2)
    cv.putText(blob,("Dice : ")+str(len(conts)),(15,30),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,255),1,cv.LINE_AA)
     
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
        elif (area > 9000):
            cv.putText(blob,"Area: {0:2.1f}".format(area),center,cv.FONT_HERSHEY_SIMPLEX,1,(232, 60, 37),3)
            cv.putText(blob,"Perimeter: {0:2.1f}".format(perimeter),(cx,cy+30),cv.FONT_HERSHEY_SIMPLEX,1,(232, 60, 37),3)

    key = cv.waitKey(1) #Define-se uma chave para condicional
    if key == ord("e"): #Caso a tecla "e" for selecionado, as janelas se fecham
        break #Para a execução
    cv.imshow("Original",bin)
    cv.imshow("Process", blob)

