from math import floor

import cv2
import numpy as np


class ImageHandler:

    def __init__(self, image_1_path, image_2_path):
        self.image_1 = cv2.imread(image_1_path)
        self.image_2 = cv2.imread(image_2_path)
        self.result = self.image_1.copy()

    def iterate(self, calculation):
        """
        Itera sobre a altura e a largura da image_1 e faz o calculo recebido
        :param calculation: função que será chamada no pixel
        """
        # itera sobre a altura da imagem
        for x in range(self.image_1.shape[0]):
            # itera sobre a largura da imagem
            for y in range(self.image_1.shape[1]):
                # itera sobre o GBR
                for z in range(3):
                    try:
                        calculation(x, y, z)
                    except:
                        continue

    def apply_gray_scale(self):
        """
        Aplica a escala de cinza na image_1 e image_2
        """
        def calculate(x, y, z):
            gray[0][x, y] = np.clip(
                0.07 * self.image_1[x, y, 0] + 0.72 * self.image_1[x, y, 1] + 0.21 * self.image_1[x, y, 2], 0, 255)
            gray[1][x, y] = np.clip(
                0.07 * self.image_2[x, y, 0] + 0.72 * self.image_2[x, y, 1] + 0.21 * self.image_2[x, y, 2], 0, 255)

        gray = [np.zeros((self.image_1.shape[0], self.image_1.shape[1]), np.uint8),
                np.zeros((self.image_2.shape[0], self.image_2.shape[1]), np.uint8)]
        self.iterate(calculate)
        self.image_1 = gray[0]
        self.image_2 = gray[1]


    def arithmetic(self, operation):
        """
        Faz o calculo aritimético recebido.
        :param operation: pode ser "+", "-", "/" ou "*"
        """
        def sum(x, y, z):
            self.result[x][y][z] = (int(self.image_1[x][y][z]) + int(self.image_2[x][y][z])) / 2

        def subtraction(x, y, z):
            self.result[x][y][z] = int(self.image_1[x][y][z]) - int(self.image_2[x][y][z])

        def multiplication(x, y, z):
            self.result[x][y][z] = int(self.image_1[x][y][z]) * int(self.image_2[x][y][z])

        def division(x, y, z):
            self.result[x][y][z] = int(self.image_1[x][y][z]) / int(self.image_2[x][y][z])

        if operation == "+":
            self.iterate(sum)
        elif operation == "-":
            self.iterate(subtraction)
        elif operation == "*":
            self.iterate(multiplication)
        elif operation == "/":
            self.iterate(division)

    def isolate(self, color):
        """
        Isola a cor recebida por parametro
        :param color: pode ser "red", "green" ou "blue"
        """
        def isolate_red(x, y, z):
            self.result[x][y][0] = 0
            self.result[x][y][1] = 0

        def isolate_green(x, y, z):
            self.result[x][y][0] = 0
            self.result[x][y][2] = 0

        def isolate_blue(x, y, z):
            self.result[x][y][1] = 0
            self.result[x][y][2] = 0

        if color == "red":
            self.iterate(isolate_red)
        elif color == "green":
            self.iterate(isolate_green)
        elif color == "blue":
            self.iterate(isolate_blue)

    def arithmetic_average(self):
        """
        Faz o calculo de média aritimética das imagens iamge_1 e image_2
        """
        def calculate(x, y, z):
            self.result[x][y] = (int(self.image_1[x][y]) + int(self.image_2[x][y])) / 2

        self.apply_gray_scale()
        self.iterate(calculate)

    def arithmetic_weighted_average(self, weight_1=7, weight_2=3):
        """
        Faz o calculo da média aritimética ponderada das imagens image_1 e image_2
        :param weight_1: peso da image_1
        :param weight_2: peso da image_2
        """
        def calculate(x, y, z):
            self.result[x][y] = ((int(self.image_1[x][y]) * weight_1) + (int(self.image_2[x][y])) * weight_2) / 2

        self.apply_gray_scale()
        self.iterate(calculate)

    def thresholding(self, L=127):
        """
        Faz a limirarização das imagem image_1
        :param L: delimitante do limiar
        """
        def calculate(x, y, z):
            self.result[x][y] = 255 if int(self.image_1[x][y]) > L else 0

        self.apply_gray_scale()
        self.iterate(calculate)

    def convolution(self, mask):
        """
        Faz a convolução genérica da imagem image_1
        :param mask: mask to be used in calculate
        """
        def calculate(x, y, z):
            mask_size = len(mask)
            temp = 0
            for mask_column in range(mask_size):
                x_pos = x + (mask_column - floor(mask_size / 2))
                if x_pos < 0 or x_pos > self.image_1.shape[0] - 1:
                    raise ValueError("Posição de X inválida!")
                for mask_line in range(mask_size):
                    y_pos = y + (floor(mask_size / 2) - mask_line)
                    if y_pos < 0 or y_pos > self.image_1.shape[1] - 1:
                        raise ValueError("Posição de Y inválida!")
                    temp += self.image_1[x_pos][y_pos][z] * mask[mask_line][mask_column]
            self.result[x][y][z] = temp / (mask_size*mask_size)

        self.iterate(calculate)

    def show_image(self):
        cv2.imshow("Resultado", self.result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def run_all(self):
        # image_handler.apply_gray_scale()
        # image_handler.arithmetic("*")
        # image_handler.isolate("green")
        # image_handler.arithmetic_average()
        # image_handler.arithmetic_weighted_average()
        # image_handler.thresholding(20)
        # image_handler.convolution(mask)
        # cv2.imwrite('imagens/original_corr.jpg', img_corr_comum)
          # printa a imagem
        image_handler.show_image()

if __name__ == "__main__":
    image_handler = ImageHandler("imagens/yoda.jpg", "imagens/yoda2.jpg")
    mask = [[1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]]

    # chama todas as funções
    image_handler.run_all()