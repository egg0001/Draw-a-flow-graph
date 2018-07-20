#!/usr/bin/python3

import svgwrite
from drawModules.shapeDraw import Group, Circle, Rectangal, Rhombus
from drawModules.lineDraw import Lines
from drawModules import config 


def drawVerticalLine(pointList, dwg, vlines, cm=config.multiConstant):
   for pL in pointList:
      vlines.add(dwg.line(start=(pL[0][0]*cm, pL[0][1]*cm), 
                          end=(pL[1][0]*cm, pL[1][1]*cm)))

def drawHorizontalLines(pointList, dwg, hlines, cm=config.multiConstant):
   for pL in pointList:
      hlines.add(dwg.line(start=(pL[0][0]*cm, pL[0][1]*cm), 
                          end=(pL[1][0]*cm, pL[1][1]*cm)))  

def drawOverlapLines(overlapPoint, dwg, hlines, vlines, cm=config.multiConstant):
#    print(overlapPoint)
   vlines.add(dwg.line(start=((overlapPoint[0]-0.1)*cm, overlapPoint[1]*cm), 
                          end=((overlapPoint[0]-0.1)*cm, (overlapPoint[1]-0.1)*cm)))
   hlines.add(dwg.line(start=((overlapPoint[0]-0.1)*cm, (overlapPoint[1]-0.1)*cm),
                          end=((overlapPoint[0]+0.1)*cm, (overlapPoint[1]-0.1)*cm)))
   vlines.add(dwg.line(start=((overlapPoint[0]+0.1)*cm, (overlapPoint[1]-0.1)*cm), 
                          end=((overlapPoint[0]+0.1)*cm, (overlapPoint[1])*cm)))                          

class lineEvaluation():
   def __init__(self, pointList):
      self.pointList=pointList
      self.overlapList =[]
      self.overlapPoint = []
      self.vertical = []
      self.horizontal = []
      self.overlapX = False
      self.overlapY = False

   def evaluateOverlap(self):

      vertical = []
      horizontal = []
      overlapList = [] # overlapList = [[(p1),(p2)], [(p3), (p4)].....]
      overpalLineList=[]
      for pL in self.pointList:
         if pL[0][0] == pL[1][0]:
            vertical.append(pL)
         else:
            horizontal.append(pL)
      for h in horizontal:
         h.sort()
         mayOverlapPointList = []
         for v in vertical:
            v.sort()
            if (h[0][1]<v[1][1]) and (h[0][1]>v[0][1]) and (h[0][0]<v[0][0]) and (h[1][0]>v[0][0]):
               mayOverlapPointList.append((v[0][0],h[0][1]))  # [(p1), (p2),(p3).....]

         if mayOverlapPointList:
        #     print (mayOverlapPointList)
            self.overlapPoint.extend(mayOverlapPointList)
            segmentList = mayOverlapPointList
            segmentList.extend(h)
            segmentList.sort()
            for segment in segmentList:
        #        print (segment)
               if segmentList.index(segment) == 0:
                  nextSegmentIndex = 1
                  self.horizontal.append([(segment[0], segment[1]), 
                                          (segmentList[nextSegmentIndex][0]-0.1, segmentList[nextSegmentIndex][1])])
               elif segmentList.index(segment) < (len(segmentList)-2):
                  nextSegmentIndex = segmentList.index(segment) +1
                  self.horizontal.append([(segment[0]+0.1, segment[1]), 
                                          (segmentList[nextSegmentIndex][0]-0.1, segmentList[nextSegmentIndex][1])])
               elif segmentList.index(segment) == (len(segmentList)-2):

                  nextSegmentIndex = segmentList.index(segment) +1

                  self.horizontal.append([(segment[0]+0.1, segment[1]), 
                                           (segmentList[nextSegmentIndex][0], segmentList[nextSegmentIndex][1])])
               else:
                  pass
            overpalLineList.append(h)
      for v in vertical:
         currentLine = v
         vertical.remove(v)
         for others in vertical:
            currentLine.sort()
            others.sort()
            if others[0][0] == currentLine[0][0] and currentLine[1][1]>others[0][1]:
               self.overlapX = True
               break
      for h in horizontal:
         currentLine = h
         horizontal.remove(h)
         for others in horizontal:
            currentLine.sort()
            others.sort()
            if others[0][1] == currentLine[0][1] and currentLine[1][0]>others[0][0]:
               self.overlapY = True
               break
      for pL in self.pointList:
         if pL[0][0] == pL[1][0]:
            self.vertical.append(pL)
         elif pL[0][1] == pL[1][1] and (pL not in overpalLineList):
            self.horizontal.append(pL)
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
   rhombus1.relateCollect['left'].append((circle2, 'helloworld'))
   rect4.relateCollect['down'].append((rect6, 'helloworld'))
   circle1.relateCollect['down'].append((rect4, 'helloworld'))
#    rect4.relateCollect['down'].extend([(circle2, 'helloworld')])
#    rect3.relateCollect['down'].append((rect6, 'helloworld'))
   lines4 = Lines(outObject=rhombus1)
   lines2 = Lines(outObject=rect4)
   rect3.relateCollect['down'].extend([(rhombus1, 'helloworld')])
   lines3 = Lines(rect3)

   lines1 = Lines(outObject=circle1)
   pointList=[]
   pointList.extend(lines1.drawLines(dwg=dwg, wideBetweenGroups=circle1.groupWide(), shapes=shapesFilled, texts=texts, polyLines=polyLines))
   pointList.extend(lines2.drawLines(dwg=dwg, wideBetweenGroups=Group.groupWide(rect4), shapes=shapesFilled, texts=texts, polyLines=polyLines))
   pointList.extend(lines3.drawLines(dwg=dwg, wideBetweenGroups=Group.groupWide(rect3), shapes=shapesFilled, texts=texts, polyLines=polyLines))
   pointList.extend(lines4.drawLines(dwg=dwg, wideBetweenGroups=Group.groupWide(rhombus1), shapes=shapesFilled, texts=texts, polyLines=polyLines))
   lineEvl = lineEvaluation(pointList)
   lineEvl.evaluateOverlap()
   print(lineEvl.overlapX)
   print(lineEvl.overlapY)
   drawVerticalLine(pointList=lineEvl.vertical, dwg=dwg, vlines=vlines,)
   drawHorizontalLines(pointList=lineEvl.horizontal, dwg=dwg, hlines=hlines,)
   
#    print (lineEvl.overlapPoint)
   for points in lineEvl.overlapPoint:
      drawOverlapLines(overlapPoint=points, dwg=dwg, hlines=hlines, vlines=vlines)
   dwg.save()


if __name__ == '__main__':
   basic_shapes('basic_shapes.svg')