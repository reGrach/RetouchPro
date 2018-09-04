from tkinter import *
from tkinter.filedialog import *
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import math


#Объявляем глобальные переменные
global mainImg, canImg
#Объявляем mainImg - списком
mainImg = []
############### ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛОМ

#Функция, создающая копию картинки, для окошка
def Made_lookImg(image):
    if image.size[0] > image.size[1]:
        koef = int(can4Img.configure('width')[4]) / image.size[0]
    else:
        koef = int(can4Img.configure('height')[4]) / image.size[1]
    return image.resize((int(image.size[0] * koef), int(image.size[1] * koef)))

#Функция вставки последнего изображения в окошко из массива главных
def InsertImg():
    global mainImg, canImg
    lastEl = len(mainImg) - 1
    canImg = ImageTk.PhotoImage(Made_lookImg(mainImg[lastEl]))
    can4Img.create_image(int(can4Img.configure('width')[4])/2, int(can4Img.configure('height')[4])/2, image=canImg)

#Функция вставки указанного изображения в окошко
def InsertSpecImg(image):
    global canImg
    image = Made_lookImg(image)
    canImg = ImageTk.PhotoImage(image)
    can4Img.create_image(int(can4Img.configure('width')[4])/2, int(can4Img.configure('height')[4])/2, image=canImg)

#Открытие файла
def OpenFile():
    global mainImg
    #Диалоговое окно открытия файла
    filename = askopenfilename(initialdir = "./",
                               filetypes = (("png files","*.png"), ("gif files","*.gif"), ("jpeg files","*.jpg")))
    mainImg.append(Image.open(filename))
    if mainImg[0].mode != "RGBA":
        mainImg[0] = mainImg[0].convert("RGBA")
    InsertImg()



#Сохранение файла
def SaveFile():
    global mainImg
    last = len(mainImg)-1
    filename = asksaveasfilename(defaultextension='.png',
                                 filetypes = (("png files","*.png"), ("gif files","*.gif"), ("jpeg files","*.jpg")))
    if 'png' in filename:
        mainImg[last].save(filename, 'png')
    elif 'jpg' in filename:
        mainImg[last].save(filename, 'png')
    elif 'gif' in filename:
        mainImg[last].save(filename, 'gif')
    else:
        return
    mainImg.clear()
    mainImg.append(Image.open(filename))
    InsertImg()

#Фиксация изменений в файле
def FiksFile():
    global mainImg
    last = len(mainImg) - 1
    if angle.get() != 0:
        print(2)
        mainImg.append(mainImg[last].rotate(angle.get()))
        angle.set(0)
    if sizeVertCrop.get() != 0 or sizeHorCrop.get() != 0:
        temp = buildCropForm(mainImg[last])
        if form4Crop.get() <=2:
            temp = temp.crop(drawFromCentr1(temp.size, sizeVertCrop.get()))
        else:
            temp = temp.crop(drawFromCentr2(temp.size, sizeHorCrop.get(), sizeVertCrop.get()))
        mainImg.append(temp)
        sizeHorCrop.set(0)
        sizeVertCrop.set(0)
    if sizeBlur.get() != 0:
        print(4)
        mainImg.append(mainImg[last].filter(ImageFilter.GaussianBlur(sizeBlur.get())))
        sizeBlur.set(0)
    if sharpRad.get() != 0 or sharpPerc.get() != 0 or sharpLim.get() != 0:
        print(5)
        mainImg.append(mainImg[last].filter(ImageFilter.UnsharpMask(sharpRad.get(), sharpPerc.get(), sharpLim.get())))
        sharpRad.set(0)
        sharpPerc.set(0)
        sharpLim.set(0)
    InsertImg()

#Отмена изменений в файле
def BackFile():
    global mainImg
    if len(mainImg) == 0: return
    if len(mainImg)!=1: mainImg.pop()
    InsertImg()


############### ФУНКЦИИ ДЛЯ РАБОТЫ ГЕОМЕТРИЕЙ ИЗОБРАЖЕНИЯ

#Отразить по вертикали
def FlipUpDown():
    global mainImg
    if len(mainImg) == 0: return
    last=len(mainImg)-1
    mainImg.append(mainImg[last].transpose(Image.FLIP_TOP_BOTTOM))
    InsertImg()

#Отразить по горизонтали
def FlipLeftRight():
    global mainImg
    if len(mainImg) == 0: return
    last=len(mainImg)-1
    mainImg.append(mainImg[last].transpose(Image.FLIP_LEFT_RIGHT))
    InsertImg()

#Повернуть изображение
def RotateImg(self):
    global mainImg
    if len(mainImg) == 0: return
    last=len(mainImg)-1
    newImg = mainImg[last].rotate(angle.get())
    InsertSpecImg(newImg)

#Функция, обрезающая конкретное изображение
def buildCropForm(img):
    tempImg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(tempImg)
    if form4Crop.get() == 1:
        draw.rectangle(drawFromCentr1(tempImg.size, sizeVertCrop.get()), fill=(0, 0, 0, 0))
    if form4Crop.get() == 2:
        draw.ellipse(drawFromCentr1(tempImg.size, sizeVertCrop.get()), fill=(0, 0, 0, 0))
    if form4Crop.get() == 3:
        draw.rectangle(drawFromCentr2(tempImg.size, sizeHorCrop.get(), sizeVertCrop.get()), fill=(0, 0, 0, 0))
    if form4Crop.get() == 4:
        draw.ellipse(drawFromCentr2(tempImg.size, sizeHorCrop.get(), sizeVertCrop.get()), fill=(0, 0, 0, 0))
    return Image.alpha_composite(img, tempImg)


#Определение координат для равносторонних фигур, центр которых совпадает с центром изображения
def drawFromCentr1(size, prec):
    rad = int(prec*max(size)/200)
    return (rad, rad, size[0] - rad, size[1] - rad)

def drawFromCentr2(size, precX, precY):
    radX = int(precX*size[0]/200)
    radY = int(precY*size[1]/200)
    return (radX, radY, size[0] - radX, size[1] - radY)

#Обрезать изображение
def ChangeImg(self):
    global mainImg
    if len(mainImg) == 0: return
    last=len(mainImg)-1
    newImg = buildCropForm(mainImg[last])
    InsertSpecImg(newImg)


############### ФУНКЦИИ ДЛЯ РАБОТЫ С ФИЛЬТРАМИ

#Размыть изображение
def MadeBlur(self):
    global mainImg
    if len(mainImg) == 0: return
    last = len(mainImg) - 1
    newImg = mainImg[last].filter(ImageFilter.GaussianBlur(sizeBlur.get()))
    InsertSpecImg(newImg)

#Натстроить резкость
def MadeSharp(self):
    global mainImg
    if len(mainImg) == 0: return
    last = len(mainImg) - 1
    newImg = mainImg[last].filter(ImageFilter.UnsharpMask(sharpRad.get(), sharpPerc.get(), sharpLim.get()))
    InsertSpecImg(newImg)

#Переход в оттенки серого
def MadeBlackWhite():
    global mainImg
    if len(mainImg) == 0: return
    last = len(mainImg) - 1
    newImg = mainImg[last].convert("RGB")
    width = newImg.size[0]
    height = newImg.size[1]
    draw = ImageDraw.Draw(newImg)
    pix = newImg.load()
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            draw.point((i, j), (S, S, S))
    mainImg.append(newImg)
    InsertSpecImg(newImg)

#ПРОСТЫЕ ФИЛЬТРЫ
def MadeContour():
    global mainImg
    if len(mainImg) == 0: return
    last = len(mainImg) - 1
    mainImg.append(mainImg[last].filter(ImageFilter.CONTOUR))
    InsertImg()

def MadeFindEdges():
    global mainImg
    if len(mainImg) == 0: return
    last = len(mainImg) - 1
    mainImg.append(mainImg[last].filter(ImageFilter.FIND_EDGES))
    InsertImg()


def MadeVHS():
    global mainImg
    if len(mainImg) == 0: return
    last = len(mainImg) - 1
    mainImg.append(mainImg[last].filter(ImageFilter.EDGE_ENHANCE))
    InsertImg()



############### РАБОТА С ОКНОМ
window = Tk() #Создаем окошко
window.geometry('1024x635')#Размеры окна
window.title('RetouchPro')#Заголовок окна
window.configure(bg="white")#Белый фон

#Переменные для запоминания значений элементов
angle = IntVar()
form4Crop = IntVar()
sizeVertCrop = IntVar()
sizeHorCrop = IntVar()
sizeBlur = IntVar()

sharpRad = IntVar()
sharpPerc = IntVar()
sharpLim = IntVar()


#Считываем иконки и меняем их размер для вставки в картинку
icon = [Image.open("./icons/iconopen.png"), Image.open("./icons/iconsave.png"), Image.open("./icons/iconfiks.png"), Image.open("./icons/iconback.png"),
        Image.open("./icons/iconflip1.png"), Image.open("./icons/iconflip2.png")]
for ii in range(4): icon[ii] = ImageTk.PhotoImage(icon[ii].resize((50, 50)))
for ii in [4, 5]: icon[ii] = ImageTk.PhotoImage(icon[ii].resize((25, 25)))

################ КНОПКИ ДЛЯ РАБОТЫ С ФАЙЛОМ

#Создаем рамку
frame4File = Frame(window, bg="white", relief=GROOVE, highlightthickness = 2, highlightbackground = "blue")
frame4File.grid(row=1, column=0, padx=5, pady=15)

#Создаем кнопки
butOpen = Button(frame4File, image=icon[0], command = OpenFile, activebackground="blue", activeforeground="white", bd=0, bg="white")
butOpen.grid(row=1, column=1, padx=15, pady=5)
butSave = Button(frame4File, image=icon[1], command = SaveFile, activebackground="blue", activeforeground="white", bd=0, bg="white")
butSave.grid(row=1, column=2, padx=15, pady=5)
butFiks = Button(frame4File, image=icon[2], command = FiksFile, activebackground="blue", activeforeground="white", bd=0, bg="white")
butFiks.grid(row=1, column=3, padx=15, pady=5)
butBack = Button(frame4File, image=icon[3], command = BackFile, activebackground="blue", activeforeground="white", bd=0, bg="white")
butBack.grid(row=1, column=4, padx=15, pady=5)

################ ОБЛАСТЬ РАБОТЫ С ГЕОМЕТРИЕЙ

#Создаем рамку
frame4Geom = Frame(window, bg="white", relief=GROOVE, highlightthickness = 2, highlightbackground = "blue")
frame4Geom.grid(row=2, column=0, padx=15, pady=5)
#Создаем заголовок
titleGeom = Label(frame4Geom, text="РАБОТА С ФОРМОЙ", font=("Times", "14", "bold italic"), bg="white")
titleGeom.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
#набор элементов для функции'ОТРАЗИТЬ'
titleFlip = Label(frame4Geom, text="Отразить изображение", font=("Times", "12"), bg="white")
titleFlip.grid(row=1, column=0, padx=5, sticky=W)
butFlipUD = Button(frame4Geom, image=icon[4],activebackground="blue",borderwidth=2, width=62,
                   activeforeground="white", bg="white", command=FlipUpDown)
butFlipUD.grid(row=1, column=1)
butFlipLR = Button(frame4Geom, image=icon[5],activebackground="blue",borderwidth=2, width=62,
                      activeforeground="white", bg="white", command=FlipLeftRight)
butFlipLR.grid(row=1, column=2, padx=5)

#набор элементов для функции 'ПОВЕРНУТЬ'
titleFlip = Label(frame4Geom, text="Повернуть изображение", font=("Times", "12"), bg="white")
titleFlip.grid(row=2, column=0, padx=5, sticky=W)
scaleRotate = Scale(frame4Geom, variable=angle, orient=HORIZONTAL, bd=0,  from_=0, to=360,
                    bg="white", length=140, command=RotateImg)
scaleRotate.grid(row=2, column=1, columnspan=2, pady=5)

#набор элементов для функции 'ОБРЕЗАТЬ'
titleCrop = Label(frame4Geom, text="Обрезать изображение", font=("Times", "12"), bg="white")
titleCrop.grid(row=3, column=0, columnspan=3)
butCut1 = Radiobutton(frame4Geom, text = "Квадрат", variable = form4Crop, value = 1, bg="white", font=("Times", "12"))
butCut1.select()
butCut1.grid(row=4, column=0, sticky=W)
butCut2 = Radiobutton(frame4Geom, text = "Круг", variable = form4Crop, value = 2, bg="white", font=("Times", "12"))
butCut2.grid(row=5, column=0, sticky=W)
butCut3 = Radiobutton(frame4Geom, text = "Прямоугольник", variable = form4Crop, value = 3, bg="white", font=("Times", "12"))
butCut3.grid(row=6, column=0, sticky=W)
butCut4 = Radiobutton(frame4Geom, text = "Эллипс", variable = form4Crop, value = 4, bg="white", font=("Times", "12"))
butCut4.grid(row=7, column=0, sticky=W)
scaleCutVert = Scale(frame4Geom, variable = sizeVertCrop, bg="white", bd=0, command=ChangeImg)
scaleCutVert.grid(row=4, rowspan=4, column=1, pady=0)
scaleCutHor = Scale(frame4Geom, variable = sizeHorCrop, bg="white",  bd=0, command=ChangeImg)
scaleCutHor.grid(row=4, rowspan=4, column=2, pady=0)


################ ОБЛАСТЬ РАБОТЫ С ФИЛЬТРАМИ
frame4Filter = Frame(window, bg="white", relief=GROOVE, highlightthickness = 2, highlightbackground = "blue")
frame4Filter.grid(row=3, column=0, padx = 15, pady = 5)
#Создаем заголовок
titleFilter = Label(frame4Filter, text="РАБОТА С ФИЛЬТРАМИ", font=("Times", "14", "bold italic"), bg="white")
titleFilter.grid(row=0, column=1, columnspan=4, padx=15)
#набор элементов для функции 'РАЗМЫТЬ'
titleBlur = Label(frame4Filter, text="Размытие по Гауссу", font=("Times", "12"), bg="white")
titleBlur.grid(row=1, column=1, padx=5, sticky =W)
scaleBlur = Scale(frame4Filter, variable=sizeBlur, orient=HORIZONTAL, bd=0,
                    bg="white", length=170, command=MadeBlur)
scaleBlur.grid(row=1, column=2, columnspan=3)

#набор элементов для функции 'РЕЗКОСТЬ'
titleSharp = Label(frame4Filter, text="Настройки резкости", font=("Times", "12"), bg="white")
titleSharp.grid(row=2, column=1, padx=5, sticky=W)

nameRad = Label(frame4Filter, text="радиус", font=("Times", "9"), bg="white")
nameRad.grid(row=2, column=2)
scaleSharpRad = Scale(frame4Filter, variable=sharpRad, bd=0, bg="white", length=110, command=MadeSharp)
scaleSharpRad.grid(row=3, rowspan=4, column=2, stick=W)

namePerc = Label(frame4Filter, text="процент", font=("Times", "9"), bg="white")
namePerc.grid(row=2, column=3)
scaleSharpPerc = Scale(frame4Filter, variable=sharpPerc, bd=0, bg="white", length=110, command=MadeSharp)
scaleSharpPerc.grid(row=3,  rowspan=4, column=3)

nameLim = Label(frame4Filter, text="порог", font=("Times", "9"), bg="white")
nameLim.grid(row=2, column=4)
scaleSharpLim = Scale(frame4Filter, variable=sharpLim, bd=0, bg="white", length=110, command=MadeSharp)
scaleSharpLim.grid(row=3, rowspan=4, column=4, pady=5)

#набор элементов для функции 'Оттенки серого'
butB_W = Button(frame4Filter, text = "Оттенки серого", font=("Times", "11"), command=MadeBlackWhite,
                activebackground="blue", activeforeground="white", bd=2, bg="white", width=15)
butB_W.grid(row=3, column=1)

#набор элементов для ПРОСТЫХ ФИЛЬТРОВ
butContour = Button(frame4Filter, text="Контур", font=("Times", "11"), command=MadeContour,
                    activebackground="blue", borderwidth=2, width=15, bg="white")
butContour.grid(row=4, column=1)

butFindEdges = Button(frame4Filter, text="Поиск кромок", font=("Times", "11"), command=MadeFindEdges,
                    activebackground="blue", borderwidth=2, width=15, bg="white")
butFindEdges.grid(row=5, column=1)

butVHS = Button(frame4Filter, text="Как в 90-е", font=("Times", "11"), command=MadeVHS,
                    activebackground="blue", borderwidth=2, width=15, bg="white")
butVHS.grid(row=6, column=1)

################ ОБЛАСТЬ ДЛЯ ВЫВОДА ИЗОБРАЖЕНИЯ
can4Img = Canvas(window, bg="white", height=600, width=630)
can4Img.grid(row=1, rowspan=3, column=1, padx=15, pady=15, sticky = N)

window.mainloop()

