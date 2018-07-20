import svgwrite
from . import config
import random



def randrange_float(start, stop, step):
    return random.randint(0, int((stop - start) / step)) * step + start


def writeACommit(dwg, textLocation, text, texts, cm=config.multiConstant):
   '''the drawLines method in Lines class would exploit this function to write commits on the arrows.'''
   text = dwg.text(text=text, insert=(textLocation[0]*cm, textLocation[1]*cm), style='font-size:{0}'.format((0.7/0.0352)*(cm/37.79)))
   texts.add(text)
   pass

class Lines():
   '''This Lines class and its objects contain all the arrows(and its commint) from every shape object. While 
      using any of three shapes objects to construct a Lines objects and exploiting its drawLines method, it
      would analyze the relateCollect attribute in the shape objects and exploit the result to drawlines.'''
   def __init__(self, outObject):
      self.outObject = outObject # This is the shape object
      self.text=''
      self.textLocation = ()

   def drawLines(self, dwg, wideBetweenGroups, shapes, texts, polyLines, cm=config.multiConstant):
      '''With a Lines itself, while providing a svgwrite.Drawing object, a objectlist from Group class, a 
         svgwrite's texts object (represent a text group in the svg file) and a svgwrite's shape objects 
         (represent a shape group in the svg file) and a wideBetweenGroups variable from shapeObject.groupWide(), 
         it would draw all the arrow from the providing shape object.'''
      vline = dwg.add(dwg.g(id='routeV', stroke='black', ))
      hline = dwg.add(dwg.g(id='routeH', stroke='black'))
      arrow = dwg.add(dwg.g(id='arrow', stroke='black'))
      outputLineList = []
      lastLineList = []
      if self.outObject.relateCollect.get('down'):
         for pDt in self.outObject.relateCollect['down']:
            pD = pDt[0]
            if (self.outObject.groupNumber == pD.groupNumber) and (pD.elementOrder == (self.outObject.elementOrder+1)):
               if (self.outObject.outPointD[0])<=(pD.inPoint[0]):

                  # vline.add(dwg.line(start=(self.outObject.outPointD[0]*cm, self.outObject.outPointD[1]*cm), 
                  #                    end=(self.outObject.inPoint[0]*cm, pD.inPoint[1]*cm)))
                  lineList=[(self.outObject.outPointD, (self.outObject.inPoint[0], pD.inPoint[1]))]
                  endPoint=(self.outObject.inPoint[0], pD.inPoint[1])

               else:
                  # vline.add(dwg.line(start=(pD.outPointD[0]*cm,self.outObject.outPointD[1]*cm), 
                  #                    end=(pD.inPoint[0]*cm, pD.inPoint[1]*cm)))
                  lineList=[((pD.outPointD[0], self.outObject.outPointD[1]), pD.inPoint)]
                  endPoint = (pD.inPoint[0], pD.inPoint[1])
                  
               try:
                 self.text=pDt[1]
                 self.textLocation = (endPoint[0], (endPoint[1]+self.outObject.outPointD[1])*1.03/2)
            #      writeACommit(dwg=dwg, textLocation=textLocation, texts=texts, text=pDt[1])
               except:
                  self.text=''
                  self.textLocation=()                
               lastLineList.append([lineList[0], lineList[1]])
               outputLineList.extend(lineList)
            elif (self.outObject.groupNumber <= pD.groupNumber):# This is right path
               if (self.outObject.groupNumber == pD.groupNumber):
                  out2RandomH=randrange_float(wideBetweenGroups[self.outObject.groupNumber][0]+0.3, 
                                              wideBetweenGroups[self.outObject.groupNumber][1]-0.3, 
                                              0.2)
               else:
                  out2RandomH=randrange_float(wideBetweenGroups[(pD.groupNumber-1)][0]+0.3, 
                                              wideBetweenGroups[(pD.groupNumber-1)][1]-0.3,
                                              0.2)
               out1RandomV=randrange_float(self.outObject.outPointD[1]+0.2, self.outObject.outPointD[1]+1, 0.2)
   
  
               out3RandomV=randrange_float(pD.inPoint[1]-1.8, pD.inPoint[1]-0.8, 0.2)
               linesList = [[(self.outObject.outPointD[0], self.outObject.outPointD[1]), 
                            (self.outObject.outPointD[0], out1RandomV)],

                            [(self.outObject.outPointD[0], out1RandomV),
                            (out2RandomH, out1RandomV)],

                            [(out2RandomH, out1RandomV),
                            (out2RandomH, out3RandomV)],

                            [(out2RandomH, out3RandomV),
                            (pD.inPoint[0],  out3RandomV)],

                             [(pD.inPoint[0],  out3RandomV),
                            (pD.inPoint[0], pD.inPoint[1])]]
               outputLineList.extend(linesList)
               lastLineList.append([(pD.inPoint[0],  out3RandomV),(pD.inPoint[0], pD.inPoint[1])])
            #    polyLines.add(dwg.polyline(points=linesList))
               endPoint=(pD.inPoint[0], pD.inPoint[1])
               try:
                  self.text=pDt[1]
                  self.textLocation=(out2RandomH, out3RandomV)
                  # writeACommit(dwg=dwg, textLocation=(out2RandomH, out3RandomV), texts=texts, text=pDt[1])
               except:
                  self.text=''
                  self.textLocation=()
            elif self.outObject.groupNumber > pD.groupNumber:  #This is left path
               print ('left path')
               out2RandomH=randrange_float(wideBetweenGroups[(self.outObject.groupNumber-1)][0], wideBetweenGroups[(self.outObject.groupNumber-1)][1], 0.2)
               out1RandomV=randrange_float(self.outObject.outPointD[1], self.outObject.outPointD[1]+1, 0.2)
              #  out2RandomH=random.uniform(wideBetweenGroups[(pD['begin'].groupNumber-1)][0]+0.5, wideBetweenGroups[(pD['begin'].groupNumber-1)][1]-0.5)     
               out3RandomV=randrange_float(pD.inPoint[1]-1.8, pD.inPoint[1]-0.8, 0.2)
               linesList = [[(self.outObject.outPointD[0], self.outObject.outPointD[1]), 
                            (self.outObject.outPointD[0], out1RandomV)],

                            [(self.outObject.outPointD[0], out1RandomV),
                            (out2RandomH, out1RandomV)],

                            [(out2RandomH, out1RandomV),
                            (out2RandomH, out3RandomV)],

                            [(out2RandomH, out3RandomV),
                            (pD.inPoint[0],  out3RandomV)],
                            
                             [(pD.inPoint[0],  out3RandomV),
                            (pD.inPoint[0], pD.inPoint[1])]]
               outputLineList.extend(linesList)
               lastLineList.append([(pD.inPoint[0],  out3RandomV),(pD.inPoint[0], pD.inPoint[1])])
            #    polyLines.add(dwg.polyline(points=linesList))
               endPoint=(pD.inPoint[0], pD.inPoint[1])
               try:
                  self.text=pDt[1]
                  self.textLocation = (pD.inPoint[0], out3RandomV)
                  # writeACommit(dwg=dwg, textLocation=(pD.inPoint[0], out3RandomV), texts=texts, text=pDt[1])
               except:
                  self.text=''
                  self.textLocation = ()
            arrowList = [(pD.inPoint[0]*cm, pD.inPoint[1]*cm),
                         (((endPoint[0]*cm+0.2*cm), ((endPoint[1]*cm-0.2*cm)))),
                         (((endPoint[0]*cm-0.2*cm)), ((endPoint[1]*cm-0.2*cm))),
                         (pD.inPoint[0]*cm, pD.inPoint[1]*cm)]
            arrow=dwg.polygon(points=arrowList, stroke='black', stroke_width=1)
            shapes.add(arrow)
      if self.outObject.relateCollect.get('left'):
         for pDt in self.outObject.relateCollect['left']:

            pD = pDt[0]
            out3RandomV=pD.inPoint[1]-0.7
            out2RandomH=randrange_float(wideBetweenGroups[(self.outObject.groupNumber-1)][0]+0.3, 
                                        wideBetweenGroups[(self.outObject.groupNumber-1)][1]-0.7, 
                                        0.2)
            lineList=[[(self.outObject.outPointL[0], self.outObject.outPointL[1]),
                       (out2RandomH, self.outObject.outPointL[1])],

                       [(out2RandomH, self.outObject.outPointL[1]),
                       (out2RandomH, out3RandomV),],

                       [(out2RandomH, out3RandomV),
                       (pD.inPoint[0],  out3RandomV),],

                       [(pD.inPoint[0],  out3RandomV),
                       (pD.inPoint[0], pD.inPoint[1])]]
            outputLineList.extend(lineList)
            lastLineList.append([(pD.inPoint[0],  out3RandomV),(pD.inPoint[0], pD.inPoint[1])])
            # polyLines.add(dwg.polyline(points=lineList))
            try:
               self.text=text=pDt[1]
               self.textLocation = ((out2RandomH, self.outObject.outPointL[1]))
            #    writeACommit(dwg=dwg, textLocation=textLocation, texts=texts, text=pDt[1])
            except:
               self.text=''
               self.textLocation=()
            arrowList = [(pD.inPoint[0]*cm, pD.inPoint[1]*cm),
                         ((pD.inPoint[0]*cm+0.2*cm), ((pD.inPoint[1]*cm-0.2*cm))),
                         (((pD.inPoint[0]*cm-0.2*cm)), ((pD.inPoint[1]*cm-0.2*cm))),
                         (pD.inPoint[0]*cm, pD.inPoint[1]*cm)]
            arrow=dwg.polygon(points=arrowList, stroke='black', stroke_width=1)
            shapes.add(arrow)
      if self.outObject.relateCollect.get('right'):
         for pDt in self.outObject.relateCollect['right']:
            pD = pDt[0]
            out3RandomV=pD.inPoint[1]-0.7
            out2RandomH=randrange_float(wideBetweenGroups[(self.outObject.groupNumber)][0]+0.7, 
                                        wideBetweenGroups[(self.outObject.groupNumber)][1]-0.3, 
                                        0.2)
            lineList=[[(self.outObject.outPointR[0], self.outObject.outPointR[1]),
                       (out2RandomH, self.outObject.outPointR[1])],

                       [(out2RandomH, self.outObject.outPointR[1]),
                       (out2RandomH, out3RandomV),],

                       [(out2RandomH, out3RandomV),
                       (pD.inPoint[0],  out3RandomV),],

                       [(pD.inPoint[0],  out3RandomV),
                       (pD.inPoint[0], pD.inPoint[1])]]
            outputLineList.extend(lineList)
            lastLineList.append([(pD.inPoint[0],  out3RandomV),(pD.inPoint[0], pD.inPoint[1])])
            # polyLines.add(dwg.polyline(points=lineList))
            try:
               self.text = pDt[1]
               self.textLocation=self.outObject.outPointR
            #    writeACommit(dwg=dwg, textLocation=self.outObject.outPointR, texts=texts, text=pDt[1])
            except:
               self.text=''
               self.textLocation=()      
            arrowList = [(pD.inPoint[0]*cm, pD.inPoint[1]*cm),
                         (((pD.inPoint[0]*cm+0.2*cm), ((pD.inPoint[1]*cm-0.2*cm)))),
                         ((pD.inPoint[0]*cm-0.2*cm), ((pD.inPoint[1]*cm-0.2*cm))),
                         (pD.inPoint[0]*cm, pD.inPoint[1]*cm)]
            arrow=dwg.polygon(points=arrowList, stroke='black', stroke_width=1)
            shapes.add(arrow)   
      return {'outputLineList': outputLineList, 'lastLineList': lastLineList}  #Line result


