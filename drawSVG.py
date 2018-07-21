#!/usr/bin/python3

import svgwrite
from drawModules.shapeDraw import Group, Circle, Rectangal, Rhombus
from drawModules.lineDraw import Lines, lineEvaluation
from drawModules import config
import random



#       self.overlapList = overlapList 


def basic_shapes(name, cm=config.multiConstant):

   dwg = svgwrite.Drawing(filename=name, debug=True)
  #  drawALine(dwg=dwg)
   vlines = dwg.add(dwg.g(id='vline', stroke='blue'))

   hlines = dwg.add(dwg.g(id='hlines', stroke='red'))
   
#    for y in range(40):
#       hlines.add(dwg.line(start=(0*cm, (y)*cm), end=(40*cm, (y)*cm)))
#    vlines = dwg.add(dwg.g(id='hline', stroke='black'))
#    for x in range(40):
#       vlines.add(dwg.line(start=((x)*cm, 0*cm), end=((x)*cm, 40*cm)))
   texts = dwg.add(dwg.g(id='text', stroke='black'))
   shapes = dwg.add(dwg.g(id='shapes', fill_opacity=0))
   polyLines = dwg.add(dwg.g(id='text', stroke='black', fill='none'))
   shapesFilled = dwg.add(dwg.g(id='shapes', fill_opacity=1, stroke='black'))
   rect0 = Rectangal(name='test1', text='Hello World!', groupNumber=1, elementOrder=1, fundation=True)
 
   rect0.drawRect(dwg=dwg,texts=texts,shapes=shapes)
   circle1 = Circle(name='test1', text='hello world！', groupNumber=2, elementOrder=1)
 
   circle1.drawCircle(dwg=dwg,texts=texts,shapes=shapes)
   circle2 = Circle(name='test1', text='hello world！', groupNumber=2, elementOrder=4)
 
   circle2.drawCircle(dwg=dwg,texts=texts,shapes=shapes)
   rect3 = Rectangal(name='test1', text='Hello World!', groupNumber=2, elementOrder=2)

   rect3.drawRect(dwg=dwg,texts=texts,shapes=shapes)
   rect4 = Rectangal(name='test1', text='Hello World!', groupNumber=1, elementOrder=2)
   
   rect4.drawRect(dwg=dwg,texts=texts,shapes=shapes)
   rect5 = Rectangal(name='test1', text='Hello World!', groupNumber=1, elementOrder=3)

   rect5.drawRect(dwg=dwg,texts=texts,shapes=shapes)
   
   rhombus1 = Rhombus(name='test1', text='Hello World!', groupNumber=3, elementOrder=2)

   rhombus1.drawRhom(dwg=dwg,texts=texts,shapes=shapes)
   rect6 = Rectangal(name='test1', text='Hello World!', groupNumber=3, elementOrder=3)

   rect6.drawRect(dwg=dwg,texts=texts,shapes=shapes)
   rect7 = Rectangal(name='test1', text='Hello World!', groupNumber=4, elementOrder=1)
   rect7.drawRect(dwg=dwg,texts=texts,shapes=shapes)
   rect7.relateCollect['down'].append((circle2, 'helloworld'))
   rhombus1.relateCollect['left'].append((circle2, 'helloworld'))
   rhombus1.relateCollect['right'].append((rect6, 'helloworld'))
   rhombus1.relateCollect['down'].append((rect6, 'helloworld'))
   rect4.relateCollect['down'].append((rect6, 'helloworld'))
   circle1.relateCollect['down'].append((rect7, 'helloworld'))
#    rect4.relateCollect['down'].extend([(circle2, 'helloworld')])
   rect3.relateCollect['down'].append((rect6, 'helloworld'))
#    rect3.relateCollect['down'].extend([(rhombus1, 'helloworld')])

   pointList=[]
   lastLineList = []
   overlapX=True
   overlapY=True
   retryTimes = 0
   while (overlapX == True or overlapY ==True) and retryTimes<=50:
      if retryTimes >0:
         pointList = []
         lastLineList =[]
         print('Retry {0} time(s)'.format(retryTimes))
      lines4 = Lines(outObject=rhombus1)
      lines2 = Lines(outObject=rect4)
      lines6 = Lines(outObject=rect7)
      lines3 = Lines(outObject=rect3)
      lines1 = Lines(outObject=circle1)
      lines1.createLinePoints(dwg=dwg, wideBetweenGroups=circle1.groupWide(), shapes=shapesFilled, texts=texts, polyLines=polyLines)
      pointList.extend(lines1.outputLineList)
      lastLineList.extend(lines1.lastLineList)
      lines2.createLinePoints(dwg=dwg, wideBetweenGroups=Group.groupWide(rect4), shapes=shapesFilled, texts=texts, polyLines=polyLines)
      pointList.extend(lines2.outputLineList)
      lastLineList.extend(lines2.lastLineList)
      lines3.createLinePoints(dwg=dwg, wideBetweenGroups=Group.groupWide(rect3), shapes=shapesFilled, texts=texts, polyLines=polyLines)
      pointList.extend(lines3.outputLineList)
      lastLineList.extend(lines3.lastLineList) 
      lines6.createLinePoints(dwg=dwg, wideBetweenGroups=Group.groupWide(rect7), shapes=shapesFilled, texts=texts, polyLines=polyLines)
      pointList.extend(lines6.outputLineList)
      lastLineList.extend(lines6.lastLineList)
      lines4.createLinePoints(dwg=dwg, wideBetweenGroups=Group.groupWide(rhombus1), shapes=shapesFilled, texts=texts, polyLines=polyLines)
      pointList.extend(lines4.outputLineList)
      lastLineList.extend(lines4.lastLineList)
      lineEvl = lineEvaluation(pointList=pointList,lastLineList=lastLineList)
      lineEvl.evaluateOverlap()
      overlapY=lineEvl.overlapX
      overlapX=lineEvl.overlapY
      print (overlapX)
      print (overlapY)
      retryTimes +=1
     
#    drawVerticalLine( dwg=dwg, vlines=vlines,)
#    drawHorizontalLines(pointList=lineEvl.horizontal, dwg=dwg, hlines=hlines,)
   lineEvl.reallyDrawLine(dwg=dwg,vlines=vlines,hlines=hlines)
#    print (lineEvl.overlapPoint)
#    for points in lineEvl.overlapPoint:
#       drawOverlapLines(overlapPoint=points, dwg=dwg, hlines=hlines, vlines=vlines)
   dwg.save()


if __name__ == '__main__':
   basic_shapes('basic_shapes.svg')