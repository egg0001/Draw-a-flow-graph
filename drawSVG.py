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
      self.wideBetweenGroups.update({0:(0,1)})
      for gL in groupList:
         maxWide = 0
         for obj in objectList:
            if obj.groupNumber == gL and ((obj.shapeLocation[0]+obj.shapeSize[0]) > maxWide):
              maxWide = obj.shapeLocation[0]+obj.shapeSize[0]
         self.wideBetweenGroups.update({gL:(maxWide,maxWide+4)})
      

class Rectangal(Group):
   def __init__(self, groupNumber, elementOrder, name, text, outConnection):
      Group.__init__(self, groupNumber, elementOrder)
      self.name=name
      self.text=text
      self.shapeSize= ()
      self.textLocation = ()
      self.shapeLocation = ()
      self.inPoint = ()
      self.outPoint = ()
      self.outConnection=outConnection

   def drawRect(self, dwg, texts, shapes, objectList):
      wordsNum = len(self.text.encode('utf-8'))
      objectList.sort(key=lambda x: x.elementOrder)
      objectList.sort(key=lambda x: x.groupNumber)
      index = objectList.index(self)
      if index == 0:
         self.textLocation = (self.groupNumber*3, self.elementOrder*4)
      elif (objectList[index-1].groupNumber == self.groupNumber):
         self.textLocation = (objectList[index-1].textLocation[0], self.elementOrder*4)
      elif objectList[index-1].groupNumber != self.groupNumber:
         longestText = []
         for obj in objectList:
            if obj.groupNumber == (self.groupNumber -1):
              longestText.append((obj.shapeLocation[0]+obj.shapeSize[0]))
         longestText.sort()
         newTextlocationX = longestText[-1]
         self.textLocation = ((newTextlocationX+ 5), self.elementOrder*4)
      text = dwg.text(text=self.text, insert=(self.textLocation[0]*cm,self.textLocation[1]*cm), style='font-size:{0}'.format(0.7/0.0352))
      texts.add(text)
      self.shapeLocation = (self.textLocation[0]-1, self.textLocation[1]-1)
      self.shapeSize=(wordsNum*0.42, 2)
      rect = dwg.rect(insert=(self.shapeLocation[0]*cm,self.shapeLocation[1]*cm), 
                      size=(self.shapeSize[0]*cm, self.shapeSize[1]*cm), rx=10, ry=10, 
                      stroke='blue', stroke_width=3)
      self.inPoint=((self.shapeLocation[0]+self.shapeSize[0]/2), (self.shapeLocation[1]))
      self.outPoint=((self.shapeLocation[0]+self.shapeSize[0]/2), (self.shapeLocation[1]+self.shapeSize[1]))
      shapes.add(rect)


def drawALine(dwg, wideBetweenGroups, relateCollect=[]):
   vline = dwg.add(dwg.g(id='routeV', stroke='black', ))
   hline = dwg.add(dwg.g(id='routeH', stroke='black'))
   for pD in relateCollect:
      if (pD['begin'].groupNumber == pD['end'].groupNumber) and (pD['end'].elementOrder == (pD['begin'].elementOrder+1)):
         if (pD['begin'].outPoint[0])<=(pD['begin'].inPoint[0]):
            vline.add(dwg.line(start=(pD['begin'].outPoint[0]*cm, pD['begin'].outPoint[1]*cm), 
                               end=(pD['begin'].inPoint[0]*cm, pD['end'].inPoint[1]*cm)))
         else:
            vline.add(dwg.line(start=(pD['end'].outPoint[0]*cm, pD['begin'].outPoint[1]*cm), 
                               end=(pD['end'].outPoint[0]*cm, pD['end'].outPoint[1]*cm)))
      elif (pD['begin'].groupNumber < pD['end'].groupNumber) and (pD['begin'].elementOrder <= pD['end'].elementOrder+1):  # This is right path
         if (pD['begin'].groupNumber == pD['end'].groupNumber):
            out2RandomH=random.uniform(wideBetweenGroups[pD['begin'].groupNumber][0]+0.5, wideBetweenGroups[pD['begin'].groupNumber][1]-0.5)
         else:
            out2RandomH=random.uniform(wideBetweenGroups[(pD['end'].groupNumber-1)][0]+0.5, wideBetweenGroups[(pD['end'].groupNumber-1)][1]-0.5)  
         out1RandomV=pD['begin'].outPoint[1]+random.uniform(0.3,1.8)
         out3RandomV=pD['end'].inPoint[1]-random.uniform(0.3,1.8)
         vline.add(dwg.line(start=(pD['begin'].outPoint[0]*cm, pD['begin'].outPoint[1]*cm), 
                            end=(pD['begin'].inPoint[0]*cm, out1RandomV*cm)))
         hline.add(dwg.line(start=(pD['begin'].inPoint[0]*cm, out1RandomV*cm), 
                            end=(out2RandomH*cm, out1RandomV*cm)))
         vline.add(dwg.line(start=(out2RandomH*cm, out1RandomV*cm),
                            end=(out2RandomH*cm, out3RandomV*cm)))
         hline.add(dwg.line(start=(out2RandomH*cm, out3RandomV*cm), 
                            end=(pD['end'].inPoint[0]*cm,  out3RandomV*cm)))
         vline.add(dwg.line(start=(pD['end'].inPoint[0]*cm,  out3RandomV*cm), 
                            end=(pD['end'].inPoint[0]*cm, pD['end'].inPoint[1]*cm)))
      elif (pD['begin'].groupNumber >= pD['end'].groupNumber) and (pD['begin'].elementOrder >= pD['end'].elementOrder):  #This is left path
         if (pD['begin'].groupNumber == pD['end'].groupNumber):
             out2RandomH=random.uniform(wideBetweenGroups[(pD['end'].groupNumber-1)][0]+0.5, wideBetweenGroups[pD['end'].groupNumber-1][1]-0.5)
         else:
            out2RandomH=random.uniform(wideBetweenGroups[(pD['begin'].groupNumber-1)][0]+0.5, wideBetweenGroups[(pD['begin'].groupNumber-1)][1]-0.5)
         out1RandomV=pD['begin'].outPoint[1]+random.uniform(0.3,1.8)
         out2RandomH=random.uniform(wideBetweenGroups[(pD['begin'].groupNumber-1)][0]+0.5, wideBetweenGroups[(pD['begin'].groupNumber-1)][1]-0.5)     
         out3RandomV=pD['end'].inPoint[1]-random.uniform(0.3,1.8)
         vline.add(dwg.line(start=(pD['begin'].outPoint[0]*cm, pD['begin'].outPoint[1]*cm), 
                            end=(pD['begin'].inPoint[0]*cm, out1RandomV*cm)))
         hline.add(dwg.line(start=(pD['begin'].inPoint[0]*cm, out1RandomV*cm), 
                            end=(out2RandomH*cm, out1RandomV*cm)))         
         vline.add(dwg.line(start=(out2RandomH*cm, out1RandomV*cm),
                            end=(out2RandomH*cm, out3RandomV*cm)))    
         hline.add(dwg.line(start=(out2RandomH*cm, out3RandomV*cm), 
                            end=(pD['end'].inPoint[0]*cm,  out3RandomV*cm)))      
         vline.add(dwg.line(start=(pD['end'].inPoint[0]*cm,  out3RandomV*cm), 
                            end=(pD['end'].inPoint[0]*cm, pD['end'].inPoint[1]*cm)))



def basic_shapes(name):
   relateCollect = []
   objectList = []
   dwg = svgwrite.Drawing(filename=name, debug=True)
#    drawALine(dwg=dwg)
#    vlines = dwg.add(dwg.g(id='testID', stroke='black'))
#    for y in range(20):
#       vlines.add(dwg.line(start=(2*cm, (2+y)*cm), end=(18*cm, (2+y)*cm)))
#    hlines = dwg.add(dwg.g(id='vlines', stroke='green'))
   
#    for y in range(20):
#       hlines.add(dwg.line(start=(0*cm, (y)*cm), end=(20*cm, (y)*cm)))
#    vlines = dwg.add(dwg.g(id='hline', stroke='blue'))
#    for x in range(20):
#       vlines.add(dwg.line(start=((x)*cm, 0*cm), end=((x)*cm, 20*cm)))
   texts = dwg.add(dwg.g(id='text', stroke='black'))
   shapes = dwg.add(dwg.g(id='shapes', fill_opacity=0))

   rect1 = Rectangal(name='test1', text='你好！', groupNumber=1, elementOrder=1, outConnection=[])
   objectList.append(rect1)
   rect1.drawRect(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
   rect2 = Rectangal(name='test1', text='Hello World!', groupNumber=1, elementOrder=2, outConnection=[])
   objectList.append(rect2)
   rect2.drawRect(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
   rect3 = Rectangal(name='test1', text='Hello World!', groupNumber=2, elementOrder=1, outConnection=[])
   objectList.append(rect3)
   rect3.drawRect(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
   rect4 = Rectangal(name='test1', text='Hello World!', groupNumber=2, elementOrder=2, outConnection=[])
   objectList.append(rect4)
   rect4.drawRect(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
#    rect4 = Rectangal(name='test1', text='Hello World!', groupNumber=2, elementOrder=2, outConnection=[])
#    objectList.append(rect4)
#    rect4.drawRect(dwg=dwg,texts=texts,shapes=shapes, objectList=objectList)
   relateCollect.extend([{'begin': rect1, 'end': rect3}, 
                         {'begin': rect1, 'end': rect2}, 
                         {'begin': rect2, 'end': rect3}, 
                         {'begin': rect2, 'end': rect1}, 
                         {'begin': rect4, 'end': rect1},
                         {'begin': rect4, 'end': rect3}])
   group = Group(groupNumber=0, elementOrder=0)
   group.groupWide(objectList=objectList)
   print(group.wideBetweenGroups)
   drawALine(dwg=dwg, wideBetweenGroups=group.wideBetweenGroups, relateCollect=relateCollect)
   dwg.save()


if __name__ == '__main__':
   basic_shapes('basic_shapes.svg')