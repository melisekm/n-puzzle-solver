import numpy as np
import cv2
import os
import glob


def drawImages(nodes):
    vstup = input("Chcete vytvorit obrazky?: ")
    if vstup != "y":
        return

    files = glob.glob("../images/*")
    if len(files) != len(nodes):
        for f in files:
            os.remove(f)

    print("Vytvaram obrazky..")
    sizeX = 40
    sizeY = 50

    x = sizeX * len(nodes[0].stav[0]) - 5
    y = sizeY * len(nodes[0].stav) - 5

    for index, node in enumerate(nodes):
        stav = node.stav
        img = np.zeros((y, x, 1), dtype="uint8")

        size = sizeX / sizeY
        posY = 30
        for sublist in stav:
            posX = 3
            for cislo in sublist:
                text = str(cislo)

                if len(text) == 2:
                    org = (posX - 7, posY)
                else:
                    org = (posX, posY)

                font = cv2.FONT_HERSHEY_SIMPLEX
                color = (255, 255, 255)
                thickness = 1
                img = cv2.putText(img, text, org, font, size, color, thickness, cv2.LINE_AA)

                posX += sizeX
            posY += sizeY

        filename = "..\\images\\" + "stav-" + str(index) + ".png"
        cv2.imwrite(filename, img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

    print("Done")
    video = input("Chcete vytvorit video? ffmpeg je potrebny: ")
    if video == "y":
        if len(nodes[0].stav) * len(nodes[0].stav[0]) > 9:
            rychlost = 5  # je to skor rychlost spomalenia :D
        else:
            rychlost = 10
        os.system(
            'cmd /c "C:/Users/melis/Desktop/ffmpeg/bin/ffmpeg.exe -loglevel quiet -y -f image2 -i "C:/Users/melis/Desktop/Dropbox/5.semester/UI/Zadanie 2/images/stav-%d.png" -vcodec mpeg4  -vf "setpts='
            + str(rychlost)
            + '*PTS" video.avi"'
        )
        preview = input("Preview?: ")
        if preview == "y":
            os.system(
                r'cmd /c "C:\Users\melis\Desktop\ffmpeg\bin\ffplay.exe -loglevel quiet video.avi'
            )
