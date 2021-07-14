import os
import numpy as np
from PIL import Image

class Web:
    def __init__(self,sizex, sizey):
        self.weight = [[0 for x in range(sizex)] for y in range(sizey)]
        self.mul = [[0 for x in range(sizex)] for y in range(sizey)]
        self.input = [[0 for x in range(sizex)] for y in range(sizey)]
        self.sum = 0
        self.limit = 100000
    def mul_w(self):
        for i in range(len(self.input)):
            for j in range(len(self.input[i])):
                self.mul[i][j] = self.input[i][j]*self.weight[i][j]
    def Sum(self):
        for i in range(len(self.input)):
            for j in range(len(self.input[i])):
                self.sum += self.mul[i][j]
    def Rez(self):
        if self.sum >= self.limit:
            return True
        else:
            return False
    def incW(self):
        for i in range(len(self.weight)):
            for j in range(len(self.weight[i])):
                self.weight[i][j] += self.input[i][j]
    def decW(self):
        for i in range(len(self.weight)):
            for j in range(len(self.weight[i])):
                self.weight[i][j] -= self.input[i][j]

def color_in_bw(arr):
    arr_out = []
    for i in arr:
        arr_buf =[]
        for j in i:
            C = int(0.2989 * j[0] + 0.5870 * j[1] + 0.1140 * j[2])
            arr_buf.append(C)
        arr_out.append(arr_buf)
    return arr_out

# обучалка
def edu():
    wb = Web(120, 120)
    fw = '00.txt'
    file_w = open(fw)
    for i in range(120):
        s = file_w.readline().split()
        for j in range(120):
            wb.weight[i][j] = int(float(s[j]))
    file_w.close()

    for filename in os.listdir('FILES/'):
        img = Image.open('FILES/' + filename)
        wb.input = color_in_bw(np.asarray(img, dtype='uint8'))

        wb.mul_w()
        wb.Sum()
        if (wb.Rez() and filename.find(",1") != -1):
            print("- True, Sum = ", wb.sum)
            wb.decW()
            s += 1
        elif (not wb.Rez() and filename.find(",1") != -1):
            print("- False, Sum = ", wb.sum)
        elif (wb.Rez() and filename.find(",1") == -1):
            print("- True, Sum = ", wb.sum)
        elif (not wb.Rez() and filename.find(",1") == -1):
            print("- False, Sum = ", wb.sum)
            wb.incW()
            s += 1
        f = open(fw, 'w')
        for i in wb.weight:
            s = ' '.join([str(j) for j in i])
            # print(len(s))
            f.write(s + '\n')
        f.close()
        wb.sum = 0
    del wb





def menu():
    print('Обучить? 0 - нет, 1 - да')
    if int(input()) == 1:
        edu()
    print('Для выхода нажмите 0, для продолжения - 1')
    if int(input()) == 1:
        NW = Web(120, 120)
        print('Укажите тестируемый файл')
        filename = input()
        img = Image.open('FILES/' + filename)
        NW.input = color_in_bw(np.asarray(img, dtype='uint8'))
        # открываем файл весов
        print('Укажите файл весов')
        file_w = input()
        f = open(file_w)
        for i in range(len(NW.weight)):
            s = f.readline().split()
            for j in range(len(NW.weight[i])):
                NW.weight[i][j] = int(s[j])
        f.close()

        # распознаём символ методами класса
        NW.mul_w()
        NW.Sum()
        if (NW.Rez()):
            print("- True, Sum = ", NW.sum)
        else:
            print("- False, Sum = ", NW.sum)

        # определяем правильность вывода
        print('Верно? (1 - верно, 0 - нет)')
        boo = int(input())
        if boo == 1:
            del NW
            menu()
        else:
            #print('Новые весы')
            f = open(file_w, 'w')
            if NW.Rez():
                NW.decW()
            else:
                NW.incW()
            for i in NW.weight:
                s = ' '.join([str(j) for j in i])
                #print(s)
                f.write(s + '\n')
            f.close()
            print("весы пересчитаны")
            del NW
            menu()
    else:
        exit(0)




menu()