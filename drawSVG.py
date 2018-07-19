#!/usr/bin/python3

import svgwrite
import random
from svgwrite import cm, mm



 


# a rect obj should has name, text, group number, size(internal) in point(internal), out point(internal), out connections.

class Group():
   def __init__(self, groupNumber, elementOrder):
      self.groupNumber = groupNumber
      self.elementOrder = elementOrder
      self.wideBetweenGroups={}
   
   def groupWide(self, objectList):
      groupList = []
      for obj in objectList:
         groupList.append(obj.groupNumber)
      groupList = list(set(groupList))
      self.wideBetweenGroups.update({0:(0,2)})
      for gL in groupList:
         maxWide = 0
         for obj in objectList:
            if obj.groupNumber == gL and ((obj.shapeLocation[0]+obj.shapeSize[0]) > maxWide):
              maxWide = obj.shapeLocation[0]+obj.shapeSize[0]
         self.wideBetweenGroups.update({gL:(maxWide,maxWide+4)})

class Circle(Group):
   def __init__(self, groupNumber, elementOrder, name, text, outConnection):
      Group.__init__(self, groupNumber, elementOrder)
      self.name=name
      self.text=text
      self.shapeSize= ()
      self.textLocation = ()
      self.shapeLocation = ()
      self.inPoint = ()
      self.outPointL = None
      self.outPointD = ()
      self.outPointR = None
      self.relateCollect = {'down': [], 'left': [], 'right': []}  # {'left': obj1, 'down':obj2, 'right' obj3}

   def drawCircle(self, dwg, texts, shapes, objectList):
      wordsNum = len(self.text.encode('utf-8'))
      objectList.sort(key=lambda x: x.elementOrder)
      objectList.sort(key=lambda x: x.groupNumber)
      index = objectList.index(self)
      if (objectList[index-1].groupNumber == self.groupNumber):
         self.textLocation = (objectList[index-1].textLocation[0], self.elementOrder*5)
      elif objectList[index-1].groupNumber != self.groupNumber:
         longestText = []
         for obj in objectList:
            if obj.groupNumber == (self.groupNumber -1):
              longestText.append((obj.shapeLocation[0]+obj.shapeSize[0]))
         longestText.sort()
         newTextlocationX = longestText[-1]*(self.groupNumber - objectList[index-1].groupNumber)
         self.textLocation = ((newTextlocationX+ 5), self.elementOrder*5) 
      text = dwg.text(text=self.text, insert=(self.textLocation[0]*cm,self.textLocation[1]*cm), style='font-size:{0}'.format(0.7/0.0352))
      texts.add(text)
      text = dwg.text(text=self.text, insert=(self.textLocation[0]*cm,self.textLocation[1]*cm), style='font-size:{0}'.format(0.7/0.0352))
      print (self.textLocation)    
      self.shapeLocation = (self.textLocation[0]-0.55, self.textLocation[1])
      self.shapeSize=(wordsNum*0.3, 0.3)
      center=(self.shapeLocation[0]+self.shapeSize[0]/2, self.shapeLocation[1])
      r=self.shapeSize[0]/2
      circle=dwg.circle(center=(center[0]*37.79, center[1]*37.79), r=r*37.79, stroke='blue', stroke_width=3)
      self.inPoint=(center[0], center[1]-r)
      self.outPointD=(center[0], center[1]+r)
      shapes.add(circle)
      

class Rhombus(Group):
   def __init__(self, groupNumber, elementOrder, name, text, outConnection):
      Group.__init__(self, groupNumber, elementOrder)
      self.name=name
      self.text=text
      self.shapeSize= ()
      self.textLocation = ()
      self.shapeLocation = ()
      self.inPoint = ()
      self.outPointL = ()
      self.outPointD = ()
      self.outPointR = ()
      self.relateCollect = {'down': [], 'left': [], 'right': []}  # {'left': obj1, 'down':obj2, 'right' obj3}
   
   def drawRhom(self, dwg, texts, shapes, objectList):
      wordsNum = len(self.text.encode('utf-8'))
      objectList.sort(key=lambda x: x.elementOrder)
      objectList.sort(key=lambda x: x.groupNumber)
      index = objectList.index(self)
      if index == 0:
         self.textLocation = (self.groupNumber*4, self.elementOrder*5)   # Seems could be used to sed a size style 
      elif (objectList[index-1].groupNumber == self.groupNumber):
         self.textLocation = (objectList[index-1].textLocation[0], self.elementOrder*5)
      elif objectList[index-1].groupNumber != self.groupNumber:
         longestText = []
         for obj in objectList:
            if obj.groupNumber == (self.groupNumber -1):
              longestText.append((obj.shapeLocation[0]+obj.shapeSize[0]))
         longestText.sort()
         newTextlocationX = longestText[-1]*(self.groupNumber - objectList[index-1].groupNumber)
         self.textLocation = ((newTextlocationX+ 5), self.elementOrder*5)
      text = dwg.text(text=self.text, insert=(self.textLocation[0]*cm,self.textLocation[1]*cm), style='font-size:{0}'.format(0.7/0.0352))
      texts.add(text)
      text = dwg.text(text=self.text, insert=(self.textLocation[0]*cm,self.textLocation[1]*cm), style='font-size:{0}'.format(0.7/0.0352))
      self.shapeLocation = (self.textLocation[0]-1, self.textLocation[1]-0.2)
      self.shapeSize=(wordsNum*0.42, 1.2)
      rhomList=[(self.shapeLocation[0]*37.79, self.shapeLocation[1]*37.79),
                ((self.shapeLocation[0]+self.shapeSize[0]/2)*37.79, (self.shapeLocation[1]-self.shapeSize[1])*37.79),
                ((self.shapeLocation[0]+self.shapeSize[0])*37.79, self.shapeLocation[1]*37.79),
                ((self.shapeLocation[0]+self.shapeSize[0]/2)*37.79, (self.shapeLocation[1]+self.shapeSize[1])*37.79),
                (self.shapeLocation[0]*37.79, self.shapeLocation[1]*37.79)]

      rhom=dwg.polygon(points=rhomList, stroke='blue', stroke_width=3)
      self.inPoint=(self.shapeLocation[0]+self.shapeSize[0]/2, self.shapeLocation[1]-self.shapeSize[1])
      self.outPointR=(self.shapeLocation[0]+self.shapeSize[0], self.shapeLocation[1])
      self.outPointL=self.shapeLocation   
      self.outPointD=(self.shapeLocation[0]+self.shapeSize[0]/2, self.shapeLocation[1]+self.shapeSize[1])
      shapes.add(rhom)

class Rectangal(Group):
   def __init__(self, groupNumber, elementOrder, name, text, outConnection, fundation=False):
      Group.__init__(self, groupNumber, elementOrder)
      self.name=name
      self.text=text
      self.shapeSize= ()
      self.textLocation = ()
      self.shapeLocation = ()
      self.inPoint = ()
      self.outPointD = ()
      self.outPointR = None
      self.outPointL = None
      self.relateCollect = {'down': [], 'left': [], 'right': []}
      self.foundation = fundation
   
   def drawRect(self, dwg, texts, shapes, objectList):
      wordsNum = len(self.text.encode('utf-8'))
      objectList.sort(key=lambda x: x.elementOrder)
      objectList.sort(key=lambda x: x.groupNumber)
      index = objectList.index(self)
      if index == 0:
         self.textLocation = (self.groupNumber*4, self.elementOrder*5)   # Seems could be used to set a size style 
      elif (objectList[index-1].groupNumber == self.groupNumber):
         self.textLocation = (objectList[index-1].textLocation[0], self.elementOrder*5)
      elif objectList[index-1].groupNumber != self.groupNumber:
         longestText = []
         for obj in objectList:
            if obj.groupNumber == (self.groupNumber -1):
              longestText.append((obj.shapeLocation[0]+obj.shapeSize[0]))
         longestText.sort()
         newTextlocationX = longestText[-1]*(self.groupNumber - objectList[index-1].groupNumber)
         self.textLocation = ((newTextlocationX+ 5), self.elementOrder*5)
      if self.foundation == False:
         text = dwg.text(text=self.text, insert=(self.textLocation[0]*cm,self.textLocation[1]*cm), style='font-size:{0}'.format(0.7/0.0352))
         stroke_width=3
         texts.add(text)
      else:
         stroke_width=0
      
      self.shapeLocation = (self.textLocation[0]-1, self.textLocation[1]-1)
      self.shapeSize=(wordsNum*0.42, 2)
      rect = dwg.rect(insert=(self.shapeLocation[0]*cm,self.shapeLocation[1]*cm), 
                      size=(self.shapeSize[0]*cm, self.shapeSize[1]*cm), rx=10, ry=10, 
                      stroke='blue', stroke_width=stroke_width)
      self.inPoint=((self.shapeLocation[0]+self.shapeSize[0]/2), (self.shapeLocation[1]))
      self.outPointD=((self.shapeLocation[0]+self.shapeSize[0]/2), (self.shapeLocation[1]+self.shapeSize[1]))
      shapes.add(rect)


def writeACommit(dwg, textLocation, text, texts):
   text = dwg.text(text=text, insert=(textLocation[0]*cm, textLocation[1]*cm), style='font-size:{0}'.format(0.7/0.0352))
   texts.add(text)
   pass

class Lines():
   # {'down': [obj], 'left': [obj], 'right':[obj]}
   def __init__(self, outObject):
      self.outObject = outObject

   def drawLines(self, dwg, wideBetweenGroups, shapes, texts):
   # {'left': obj1, 'down':obj2, 'right' obj3}
      vline = dwg.add(dwg.g(id='routeV', stroke='black', ))
      hline = dwg.add(dwg.g(id='routeH', stroke='black'))
      arrow = dwg.add(dwg.g(id='arrow', stroke='black'))
      if self.outObject.relateCollect.get('down'):
         for pDt in self.outObject.relateCollect['down']:
            pD = pDt[0]
            if (self.outObject.groupNumber == pD.groupNumber) and (pD.elementOrder == (self.outObject.elementOrder+1)):
               if (self.outObject.outPointD[0])<=(pD.inPoint[0]):

                  vline.add(dwg.line(start=(self.outObject.outPointD[0]*cm, self.outObject.outPointD[1]*cm), 
                                     end=(self.outObject.inPoint[0]*cm, pD.inPoint[1]*cm)))
                  endPoint=(self.outObject.inPoint[0], pD.inPoint[1])
               else:
                  vline.add(dwg.line(start=(pD.outPointD[0]*cm,self.outObject.outPointD[1]*cm), 
                                     end=(pD.inPoint[0]*cm, pD.inPoint[1]*cm)))
                  endPoint = (pD.inPoint[0], pD.inPoint[1])
               try:
                 textLocation = (endPoint[0], (endPoint[1]+self.outObject.outPointD[1])*0.95/2)
                 writeACommit(dwg=dwg, textLocation=textLocation, texts=texts, text=pDt[1])
               except:
                 pass

            elif (self.outObject.groupNumber <= pD.groupNumber):# This is right path
               if (self.outObject.groupNumber == pD.groupNumber):
                  out2RandomH=(wideBetweenGroups[self.outObject.groupNumber][0]+wideBetweenGroups[self.outObject.groupNumber][1])/2
               else:
                  out2RandomH=(wideBetweenGroups[(pD.groupNumber-1)][0]+wideBetweenGroups[(pD.groupNumber-1)][1])/2
               out1RandomV=self.outObject.outPointD[1]+1.5
               if (self.outObject.elementOrder == pD.elementOrder-1):
                  out3RandomV=out1RandomV
               else:
                  out3RandomV=pD.inPoint[1]-1.5
               vline.add(dwg.line(start=(self.outObject.outPointD[0]*cm, self.outObject.outPointD[1]*cm), 
                                  end=(self.outObject.outPointD[0]*cm, out1RandomV*cm)))
               hline.add(dwg.line(start=(self.outObject.outPointD[0]*cm, out1RandomV*cm), 
                                  end=(out2RandomH*cm, out1RandomV*cm)))
               vline.add(dwg.line(start=(out2RandomH*cm, out1RandomV*cm),
                                  end=(out2RandomH*cm, out3RandomV*cm)))
               hline.add(dwg.line(start=(out2RandomH*cm, out3RandomV*cm), 
                                  end=(pD.inPoint[0]*cm,  out3RandomV*cm)))
               vline.add(dwg.line(start=(pD.inPoint[0]*cm,  out3RandomV*cm), 
                                  end=(pD.inPoint[0]*cm, pD.inPoint[1]*cm)))
               endPoint=(pD.inPoint[0], pD.inPoint[1])
               try:
                  text = pDt[1]
                  writeACommit(dwg=dwg, textLocation=(out2RandomH, out3RandomV), texts=texts, text=pDt[1])
               except:
                  pass
            elif self.outObject.groupNumber > pD.groupNumber:  #This is left path
               out2RandomH=(wideBetweenGroups[(self.outObject.groupNumber-1)][0]+wideBetweenGroups[(self.outObject.groupNumber-1)][1])/2
               out1RandomV=self.outObject.outPointD[1]+1.5
              #  out2RandomH=random.uniform(wideBetweenGroups[(pD['begin'].groupNumber-1)][0]+0.5, wideBetweenGroups[(pD['begin'].groupNumber-1)][1]-0.5)     
               out3RandomV=pD.inPoint[1]-1.5
               vline.add(dwg.line(start=(self.outObject.outPointD[0]*cm, self.outObject.outPointD[1]*cm), 
                                  end=(self.outObject.outPointD[0]*cm, out1RandomV*cm)))
               hline.add(dwg.line(start=(self.outObject.outPointD[0]*cm, out1RandomV*cm), 
                                  end=(out2RandomH*cm, out1RandomV*cm)))         
               vline.add(dwg.line(start=(out2RandomH*cm, out1RandomV*cm),
                                  end=(out2RandomH*cm, out3RandomV*cm)))    
               hline.add(dwg.line(start=(out2RandomH*cm, out3RandomV*cm), 
                               end=(pD.inPoint[0]*cm,  out3RandomV*cm)))      
               vline.add(dwg.line(start=(pD.inPoint[0]*cm,  out3RandomV*cm), 
                                  end=(pD.inPoint[0]*cm, pD.inPoint[1]*cm)))
               endPoint=(pD.inPoint[0], pD.inPoint[1])
               try:
                  text = pDt[1]
                  writeACommit(dwg=dwg, textLocation=(pD.inPoint[0], out3RandomV), texts=texts, text=pDt[1])
               except:
                  pass
            arrowList = [(pD.inPoint[0]*37.79, pD.inPoint[1]*37.79),
                         (((endPoint[0]+0.5)*37.79, ((endPoint[1]-0.5)*37.79))),
                         (((endPoint[0]-0.5)*37.79), ((endPoint[1]-0.5)*37.79)),
                         (pD.inPoint[0]*37.79, pD.inPoint[1]*37.79)]
            arrow=dwg.polygon(points=arrowList, stroke='black', stroke_width=1)
            shapes.add(arrow)
      if self.outObject.relateCollect.get('left'):
         for pDt in self.outObject.relateCollect['left']:

            pD = pDt[0]
            out3RandomV=pD.inPoint[1]-1.5
            out2RandomH=(wideBetweenGroups[(self.outObject.groupNumber-1)][0]+wideBetweenGroups[(self.outObject.groupNumber-1)][1])/2
            hline.add(dwg.line(start=(self.outObject.outPointL[0]*cm, self.outObject.outPointL[1]*cm), 
                               end=(out2RandomH*cm, self.outObject.outPointL[1]*cm)))
            vline.add(dwg.line(start=(out2RandomH*cm, self.outObject.outPointL[1]*cm),
                               end=(out2RandomH*cm, out3RandomV*cm)))   
            hline.add(dwg.line(start=(out2RandomH*cm, out3RandomV*cm), 
                               end=(pD.inPoint[0]*cm,  out3RandomV*cm)))
            vline.add(dwg.line(start=(pD.inPoint[0]*cm,  out3RandomV*cm), 
                               end=(pD.inPoint[0]*cm, pD.inPoint[1]*cm)))
            try:
               textLocation = ((out2RandomH, self.outObject.outPointL[1]))
               writeACommit(dwg=dwg, textLocation=textLocation, texts=texts, text=pDt[1])
            except:
               pass
            arrowList = [(pD.inPoint[0]*37.79, pD.inPoint[1]*37.79),
                         (((pD.inPoint[0]+0.5)*37.79, ((pD.inPoint[1]-0.5)*37.79))),
                         (((pD.inPoint[0]-0.5)*37.79), ((pD.inPoint[1]-0.5)*37.79)),
                         (pD.inPoint[0]*37.79, pD.inPoint[1]*37.79)]
            arrow=dwg.polygon(points=arrowList, stroke='black', stroke_width=1)
            shapes.add(arrow)
      if self.outObject.relateCollect.get('right'):
         for pDt in self.outObject.relateCollect['right']:
            pD = pDt[0]
            out3RandomV=pD.inPoint[1]-1.5
            out2RandomH=(wideBetweenGroups[(self.outObject.groupNumber)][0]+wideBetweenGroups[(self.outObject.groupNumber)][1])/2
            hline.add(dwg.line(start=(self.outObject.outPointR[0]*cm, self.outObject.outPointR[1]*cm), 
                               end=(out2RandomH*cm, self.outObject.outPointR[1]*cm)))
            vline.add(dwg.line(start=(out2RandomH*cm, self.outObject.outPointR[1]*cm),
                               end=(out2RandomH*cm, out3RandomV*cm)))   
            hline.add(dwg.line(start=(out2RandomH*cm, out3RandomV*cm), 
                               end=(pD.inPoint[0]*cm,  out3RandomV*cm)))
            vline.add(dwg.line(start=(pD.inPoint[0]*cm,  out3RandomV*cm), 
                               end=(pD.inPoint[0]*cm, pD.inPoint[1]*cm))) 
            try:
               text = pDt[1]
               writeACommit(dwg=dwg, textLocation=self.outObject.outPointR, texts=texts, text=pDt[1])
            except:
               pass
            arrowList = [(pD.inPoint[0]*37.79, pD.inPoint[1]*37.79),
                         (((pD.inPoint[0]+0.5)*37.79, ((pD.inPoint[1]-0.5)*37.79))),
                         (((pD.inPoint[0]-0.5)*37.79), ((pD.inPoint[1]-0.5)*37.79)),
                         (pD.inPoint[0]*37.79, pD.inPoint[1]*37.79)]
            arrow=dwg.polygon(points=arrowList, stroke='black', stroke_width=1)
            shapes.add(arrow)   



def basic_shapes(name):
   relateCollect = []
   objectList = []
   dwg = svgwrite.Drawing(filename=name, debug=True)
  #  drawALine(dwg=dwg)
  #  vlines = dwg.add(dwg.g(id='testID', stroke='black'))
  # #  for y in range(20):
  # #     vlines.add(dwg.line(start=(2*cm, (2+y)*cm), end=(18*cm, (2+y)*cm)))
  #  hlines = dwg.add(dwg.g(id='vlines', stroke='green'))
   
  #  for y in range(40):
  #     hlines.add(dwg.line(start=(0*cm, (y)*cm), end=(40*cm, (y)*cm)))
  #  vlines = dwg.add(dwg.g(id='hline', stroke='blue'))
  #  for x in range(40):
  #     vlines.add(dwg.line(start=((x)*cm, 0*cm), end=((x)*cm, 40*cm)))
   texts = dwg.add(dwg.g(id='text', stroke='black'))
   shapes = dwg.add(dwg.g(id='shapes', fill_opacity=0))
   shapesFilled = dwg.add(dwg.g(id='shapes', fill_opacity=1, stroke='black'))
   rect0 = Rectangal(name='test1', text='Hello World!', groupNumber=1, elementOrder=1, outConnection=[], fundation=True)
   objectList.append(rect0)
   rect0.drawRect(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
   circle1 = Circle(name='test1', text='hello world！', groupNumber=2, elementOrder=1, outConnection=[])
   objectList.append(circle1)
   circle1.drawCircle(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
   circle2 = Circle(name='test1', text='hello world！', groupNumber=2, elementOrder=4, outConnection=[])
   objectList.append(circle2)
   circle2.drawCircle(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
   rect3 = Rectangal(name='test1', text='Hello World!', groupNumber=2, elementOrder=2, outConnection=[])
   objectList.append(rect3)
   rect3.drawRect(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
   rect4 = Rectangal(name='test1', text='Hello World!', groupNumber=1, elementOrder=2, outConnection=[])
   objectList.append(rect4)
   rect4.drawRect(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
   

   rect5 = Rectangal(name='test1', text='Hello World!', groupNumber=1, elementOrder=3, outConnection=[])
   objectList.append(rect5)
   rect5.drawRect(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
   circle1.relateCollect['down'].append((rect3, 'helloworld'))
   rhombus1 = Rhombus(name='test1', text='Hello World!', groupNumber=3, elementOrder=2, outConnection=[])
   objectList.append(rhombus1)
   rhombus1.drawRhom(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
   rect6 = Rectangal(name='test1', text='Hello World!', groupNumber=3, elementOrder=3, outConnection=[])
   objectList.append(rect6)
   rect6.drawRect(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
   rect7 = Rectangal(name='test1', text='Hello World!', groupNumber=4, elementOrder=1, outConnection=[])
   objectList.append(rect7)
   rect7.drawRect(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)

   rhombus1.relateCollect['left'].append((circle2, 'helloworld'))
   lines4 = Lines(outObject=rhombus1)

   lines2 = Lines(outObject=rect4)
   rect3.relateCollect['down'].extend([(rhombus1, 'helloworld'), (rect5, 'helloworld')])
   
   lines3 = Lines(rect3)
   rect4.relateCollect['down'].extend([(circle2, 'helloworld'), (rect5, 'helloworld')])

   group = Group(groupNumber=0, elementOrder=0)
   group.groupWide(objectList=objectList)
   lines1 = Lines(outObject=circle1)
   lines1.drawLines(dwg=dwg, wideBetweenGroups=group.wideBetweenGroups, shapes=shapesFilled, texts=texts)
   lines2.drawLines(dwg=dwg, wideBetweenGroups=group.wideBetweenGroups, shapes=shapesFilled, texts=texts)
   lines3.drawLines(dwg=dwg, wideBetweenGroups=group.wideBetweenGroups, shapes=shapesFilled, texts=texts)
   lines4.drawLines(dwg=dwg, wideBetweenGroups=group.wideBetweenGroups, shapes=shapesFilled, texts=texts)


  #  relateCollect.extend([#{'begin': rect1, 'end': rect6}, 
  #                        {'begin': rect1, 'end': rect5}, 
  #                       #  {'begin': rect2, 'end': rect3}, 
  #                       #  {'begin': rect2, 'end': rect1}, 
  #                        {'begin': rect4, 'end': rect1},
  #                       #  {'begin': rect4, 'end': rect3},
  #                       #  {'begin': rect4, 'end': rect2}
  #  ])

  #  lines3.drawLines(dwg=dwg,wideBetweenGroups=group.wideBetweenGroups, shapes=shapesFilled)
   print(group.wideBetweenGroups)
  #  drawALine(dwg=dwg, wideBetweenGroups=group.wideBetweenGroups, relateCollect=relateCollect)
   dwg.save()


if __name__ == '__main__':
   basic_shapes('basic_shapes.svg')