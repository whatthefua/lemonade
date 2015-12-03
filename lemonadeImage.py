############################################################
# defines class lemonadeImage
# stores an image, and defines operations that can be performed on the image
# attributes: __width - width of image
#             __height - height of image
#             __bpp - bit depth of image
#             __imgTab - pixels of image in triples (r,g,b)
############################################################

class lemonadeImage:
    def __init__(self):
        """
        initialises an instance of lemonadeImage
        :arguments: none
        :return: none
        """
        self.__width = 0
        self.__height = 0
        self.__imgTab = []

    def setSize(self, width, height):
        """
        sets the dimensions of the instance
        :arguments: width - desired width of instance
                    height - desired height of instance
        :return: none
        """
        self.__width = width
        self.__height = height

        for i in range(width):
            self.__imgTab.append([(0,0,0)] * height)

    def setBpp(self,bpp):
        """
        sets the bit depth (bit per pixel) of instance
        :arguments: bpp - desired bit depth
        :return: none
        """
        self.__bpp = bpp

    def setPixel(self, x, y, colour):
        """
        sets a pixel of instance
        :arguments: x - x coordinate of pixel
                    y - y coordinate of pixel
                    colour - desired colour of pixel, in triple (r,g,b)
        :return: none
        """
        self.__imgTab[x][y] = colour

    def setPixelAll(self, colour):
        """
        sets every pixel of instance
        :arguments: colour - desired colour of pixel, in triple (r,g,b)
        :return: none
        """
        for i in range(self.__width):
            for j in range(self.__height):
                self.__imgTab[i][j] = colour

    def getPixel(self, x, y):
        """
        gets a pixel of instance
        :arguments: x - x coordinate of pixel
                    y - y coordinate of pixel
        :return: colour of selected pixel, in triple (r,g,b)
        """
        return self.__imgTab[x][y]

    def width(self):
        """
        gets the width of instance
        :arguments: none
        :return: width of instance
        """
        return self.__width

    def height(self):
        """
        gets the height of instance
        :arguments: none
        :return: height of instance
        """
        return self.__height

    def loadImage(self, src):
        """
        load an image from src and store image data in instance
        :arguments: src - path to image file
        :return: none
        """
        if (src[-3] == 'b') and (src[-2] == 'm') and (src[-1] == 'p'):  #bitmap file
            fp = open(src,'rb')
            fp.read(18)

            self.__width = 0
            self.__height = 0

            for i in range(4):
                self.__width += int(fp.read(1).encode('hex'),16) * 256 ** i

            for i in range(4):
                self.__height += int(fp.read(1).encode('hex'),16) * 256 ** i

            self.setSize(self.__width, self.__height)

            fp.read(2)

            self.__bpp = 0

            for i in range(2):
                self.__bpp += int(fp.read(1).encode('hex'),16) * 256 ** i

            fp.read(24)

            if self.__bpp == 24:
                for j in range(self.__height - 1,-1,-1):
                    c = 0

                    for i in range(self.__width):
                        b = int(fp.read(1).encode('hex'),16)
                        g = int(fp.read(1).encode('hex'),16)
                        r = int(fp.read(1).encode('hex'),16)

                        self.__imgTab[i][j] = (r,g,b)

                        c += 3

                    while c % 4 != 0:
                        fp.read(1)
                        c += 1

    def saveImage(self, targ):
        """
        saves instance into an image file
        :arguments: targ - path to save file
        :return: none
        """
        if (targ[-3] == 'b') and (targ[-2] == 'm') and (targ[-1] == 'p'):  #bitmap file
            fp = open(targ,'wb')
            fp.write(b'\x42\x4D')

            if self.__bpp == 24:
                c = self.__width * 3

                while c % 4 != 0:
                    c += 1

                size = 54 + c * self.__height
                sizeArr = [size % 256, (size / 256) % 256, (size / 65536) % 256, (size / 1048576) % 256]
                fp.write(bytearray(sizeArr))

                fp.write(b'\x00\x00\x00\x00')
                fp.write(b'\x36\x00\x00\x00')
                fp.write(b'\x28\x00\x00\x00')

                widthArr = [self.__width % 256, (self.__width / 256) % 256, (self.__width / 65536) % 256, (self.__width / 1048576) % 256]
                fp.write(bytearray(widthArr))

                heightArr = [self.__height % 256, (self.__height / 256) % 256, (self.__height / 65536) % 256, (self.__height / 1048576) % 256]
                fp.write(bytearray(heightArr))

                fp.write(b'\x01\x00\x18\x00')
                fp.write(b'\x00\x00\x00\x00')

                size -= 54
                sizeArr = [size % 256, (size / 256) % 256, (size / 65536) % 256, (size / 1048576) % 256]
                fp.write(bytearray(sizeArr))

                fp.write(b'\x13\x0B\x00\x00')
                fp.write(b'\x13\x0B\x00\x00')
                fp.write(b'\x00\x00\x00\x00')
                fp.write(b'\x00\x00\x00\x00')

                for j in range(self.__height - 1,-1,-1):
                    c = 0

                    for i in range(self.__width):
                        arr = [self.__imgTab[i][j][0],self.__imgTab[i][j][1],self.__imgTab[i][j][2]]
                        fp.write(bytearray(arr))
                        c += 3

                    while c % 4 != 0:
                        fp.write(b'\x00')
                        c += 1

    def greyscaleAverage(self):
        for i in range(self.__width):
            for j in range(self.__height):
                avg = (self.__imgTab[i][j][0] + self.__imgTab[i][j][1] + self.__imgTab[i][j][2]) / 3
                self.__imgTab[i][j] = (avg,avg,avg)

    def edgeDetectSobel(self):
        """
        runs Sobel edge detection operator on instance
        :arguments: none
        :return: result of Sobel edge detection
        """
        res = lemonadeImage()
        res.setSize(self.__width - 2, self.__height - 2)

        for i in range(1,self.__width - 1):
            for j in range(1,self.__height - 1):
                rD = abs((self.__imgTab[i - 1][j - 1][0] + 2 * self.__imgTab[i][j - 1][0] + self.__imgTab[i + 1][j - 1][0])\
                        - (self.__imgTab[i - 1][j + 1][0] + 2 * self.__imgTab[i][j + 1][0] + self.__imgTab[i + 1][j + 1][0]))\
                        + abs((self.__imgTab[i + 1][j - 1][0] + 2 * self.__imgTab[i + 1][j][0] + self.__imgTab[i + 1][j + 1][0])\
                        - (self.__imgTab[i - 1][j - 1][0] + 2 * self.__imgTab[i - 1][j][0] + self.__imgTab[i - 1][j + 1][0]))

                gD = abs((self.__imgTab[i - 1][j - 1][1] + 2 * self.__imgTab[i][j - 1][1] + self.__imgTab[i + 1][j - 1][1])\
                        - (self.__imgTab[i - 1][j + 1][1] + 2 * self.__imgTab[i][j + 1][1] + self.__imgTab[i + 1][j + 1][1]))\
                        + abs((self.__imgTab[i + 1][j - 1][1] + 2 * self.__imgTab[i + 1][j][1] + self.__imgTab[i + 1][j + 1][1])\
                        - (self.__imgTab[i - 1][j - 1][1] + 2 * self.__imgTab[i - 1][j][1] + self.__imgTab[i - 1][j + 1][1]))
                
                bD = abs((self.__imgTab[i - 1][j - 1][2] + 2 * self.__imgTab[i][j - 1][2] + self.__imgTab[i + 1][j - 1][2])\
                        - (self.__imgTab[i - 1][j + 1][2] + 2 * self.__imgTab[i][j + 1][2] + self.__imgTab[i + 1][j + 1][2]))\
                        + abs((self.__imgTab[i + 1][j - 1][2] + 2 * self.__imgTab[i + 1][j][2] + self.__imgTab[i + 1][j + 1][2])\
                        - (self.__imgTab[i - 1][j - 1][2] + 2 * self.__imgTab[i - 1][j][2] + self.__imgTab[i - 1][j + 1][2]))

                D = max(rD,gD,bD) / 8

                res.setPixel(i - 1,j - 1,(D,D,D))

        return res

    def cornerDetectHarris(self, Lambda = 0.04):
        """
        runs Harris corner detection algorithm on instance
        :arguments: (Lambda) - lambda value used in algorithm, default 0.04
        :return: result of Harris corner detection
        """
        res = lemonadeImage()
        res.setSize(self.__width - 4,self.__height - 4)

        xM = []
        yM = []

        for i in range(1,self.__width - 1):
            xM.append([0] * (self.__height - 2))
            yM.append([0] * (self.__height - 2))

            for j in range(1,self.__height - 1):
                rxD = (self.__imgTab[i + 1][j - 1][0] + self.__imgTab[i + 1][j][0] + self.__imgTab[i + 1][j + 1][0])\
                    - (self.__imgTab[i - 1][j - 1][0] + self.__imgTab[i - 1][j][0] + self.__imgTab[i - 1][j + 1][0])

                gxD = (self.__imgTab[i + 1][j - 1][1] + self.__imgTab[i + 1][j][1] + self.__imgTab[i + 1][j + 1][1])\
                    - (self.__imgTab[i - 1][j - 1][1] + self.__imgTab[i - 1][j][1] + self.__imgTab[i - 1][j + 1][1])

                bxD = (self.__imgTab[i + 1][j - 1][2] + self.__imgTab[i + 1][j][2] + self.__imgTab[i + 1][j + 1][2])\
                    - (self.__imgTab[i - 1][j - 1][2] + self.__imgTab[i - 1][j][2] + self.__imgTab[i - 1][j + 1][2])

                ryD = (self.__imgTab[i - 1][j + 1][0] + self.__imgTab[i][j + 1][0] + self.__imgTab[i + 1][j + 1][0])\
                    - (self.__imgTab[i - 1][j - 1][0] + self.__imgTab[i][j - 1][0] + self.__imgTab[i + 1][j - 1][0])

                byD = (self.__imgTab[i - 1][j + 1][1] + self.__imgTab[i][j + 1][1] + self.__imgTab[i + 1][j + 1][1])\
                    - (self.__imgTab[i - 1][j - 1][1] + self.__imgTab[i][j - 1][1] + self.__imgTab[i + 1][j - 1][1])

                gyD = (self.__imgTab[i - 1][j + 1][2] + self.__imgTab[i][j + 1][2] + self.__imgTab[i + 1][j + 1][2])\
                    - (self.__imgTab[i - 1][j - 1][2] + self.__imgTab[i][j - 1][2] + self.__imgTab[i + 1][j - 1][2])

                xM[i - 1][j - 1] = max(rxD,gxD,bxD)
                yM[i - 1][j - 1] = max(ryD,gyD,byD)

        H = []
        M = 0

        for i in range(1,self.__width - 3):
            H.append([0] * (self.__height - 4))

            for j in range(1,self.__height - 3):
                x2 = xM[i - 1][j - 1] ** 2 + xM[i - 1][j] ** 2 + xM[i - 1][j + 1] ** 2\
                     + xM[i][j - 1] ** 2 + xM[i][j] ** 2 + xM[i][j + 1] ** 2\
                     + xM[i + 1][j - 1] ** 2 + xM[i + 1][j] ** 2 + xM[i + 1][j + 1] ** 2
                
                y2 = yM[i - 1][j - 1] ** 2 + yM[i - 1][j] ** 2 + yM[i - 1][j + 1] ** 2\
                     + yM[i][j - 1] ** 2 + yM[i][j] ** 2 + yM[i][j + 1] ** 2\
                     + yM[i + 1][j - 1] ** 2 + yM[i + 1][j] ** 2 + yM[i + 1][j + 1] ** 2

                xy = xM[i - 1][j - 1] * yM[i - 1][j - 1] + xM[i - 1][j] * yM[i - 1][j] + xM[i - 1][j + 1] * yM[i - 1][j + 1]\
                     + xM[i][j - 1] * yM[i][j - 1] + xM[i][j] * yM[i][j] + xM[i][j + 1] * yM[i][j + 1]\
                     + xM[i + 1][j - 1] * yM[i + 1][j - 1] + xM[i + 1][j] * yM[i + 1][j] + xM[i + 1][j + 1] * yM[i + 1][j + 1]

                H[i - 1][j - 1] = max(0,x2 * y2 - xy * xy - Lambda * (x2 + y2))
                M = max(H[i - 1][j - 1],M)

        if(M == 0):
            for i in range(self.__width - 4):
                for j in range(self.__height - 4):
                    res.setPixel(i,j,(0,0,0))
        else:
            for i in range(self.__width - 4):
                for j in range(self.__height - 4):
                    res.setPixel(i,j,(int(round(255 * H[i][j] / M)),int(round(255 * H[i][j] / M)),int(round(255 * H[i][j] / M))))

        return res

    def cornerDetectFAST(self, threshold):
        res = []
        check1 = [(0,-3),(3,0),(3,3),(-3,0)]
        check2 = [(0,-3),(1,-3),(2,-2),(3,-1),(3,0),(3,1),(2,2),(1,3),(0,3),(-1,3),(-2,2),(-3,1),(-3,-1),(-3,0),(-2,-2),(-1,-3)]
        avg = []

        for i in range(self.__width):
            avg.append([0] * self.__height)
            for j in range(self.__height):
                avg[i][j] = (self.__imgTab[i][j][0] + self.__imgTab[i][j][1] + self.__imgTab[i][j][2]) / 3

        for i in range(3,self.__width - 3):
            for j in range(3,self.__height - 3):
                d = 0
                b = 0
                m = 0

                for k in range(4):
                    if avg[i + check1[k][0]][j + check1[k][1]] <= avg[i][j] - threshold:
                        m = max(m,b)
                        d += 1
                        b = 0
                    elif avg[i + check1[k][0]][j + check1[k][1]] >= avg[i][j] + threshold:
                        m = max(m,d)
                        b += 1
                        d = 0

                    m = max(m,d,b)

                if(m >= 3):
                    d = 0
                    b = 0
                    m = 0

                    for k in range(16):
                        if avg[i + check2[k][0]][j + check2[k][1]] <= avg[i][j] - threshold:
                            m = max(m,b)
                            d += 1
                            b = 0
                        elif avg[i + check2[k][0]][j + check2[k][1]] >= avg[i][j] + threshold:
                            m = max(m,d)
                            b += 1
                            d = 0

                        m = max(m,d,b)

                    if(m >= 12):
                        res.append((i,j))

        return res