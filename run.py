import lemonadeImage
import feedforwardNeuralNetwork
import time

'''
x = lemonadeImage.lemonadeImage()
x.loadImage('mountain.bmp')

xE = x.cornerDetectFAST(80)

xN = lemonadeImage.lemonadeImage()
xN.setSize(x.width() - 6, x.height() - 6)
xN.setBpp(24)

xN.setPixelAll((0,0,0))

for i in xE:
    xN.setPixel(i[0] - 3,i[1] - 3,(255,255,255))

xN.saveImage('bmp4.bmp')

xN = x.edgeDetectSobel()
xN.setBpp(24)
xN.saveImage('bmp5.bmp')
'''

x = feedforwardNeuralNetwork.feedforwardNeuralNetwork(3,[5,3,2],'NN1')
c = 0

while True:
    print 'New epoch %d' % (c)

    c += 1

    x.learn([1,1,0,0,1],[1,0],0.1)
    x.learn([0,1,1,1,0],[0,1],0.1)
    x.learn([0,1,1,1,1],[1,1],0.1)
    x.learn([0,1,0,0,0],[0,0],0.1)

    print x.feed([1,1,0,0,1])
    print x.feed([0,1,1,1,0])
    print x.feed([0,1,1,1,1])
    print x.feed([0,1,0,0,0])