import svgwrite
from . import config


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

   def drawLines(self, dwg, wideBetweenGroups, shapes, texts, polyLines, cm=config.multiConstant):
      '''With a Lines itself, while providing a svgwrite.Drawing object, a objectlist from Group class, a 
         svgwrite's texts object (represent a text group in the svg file) and a svgwrite's shape objects 
         (represent a shape group in the svg file) and a wideBetweenGroups variable from shapeObject.groupWide(), 
         it would draw all the arrow from the providing shape object.'''
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
                 textLocation = (endPoint[0], (endPoint[1]+self.outObject.outPointD[1])*1.03/2)
                 writeACommit(dwg=dwg, textLocation=textLocation, texts=texts, text=pDt[1])
               except:
                 pass

            elif (self.outObject.groupNumber <= pD.groupNumber):# This is right path
               if (self.outObject.groupNumber == pD.groupNumber):
                  out2RandomH=(wideBetweenGroups[self.outObject.groupNumber][0]+wideBetweenGroups[self.outObject.groupNumber][1])/2
               else:
                  out2RandomH=(wideBetweenGroups[(pD.groupNumber-1)][0]+wideBetweenGroups[(pD.groupNumber-1)][1])*1.05/2
               out1RandomV=self.outObject.outPointD[1]+0.8
               if (self.outObject.elementOrder == pD.elementOrder-1):
                  out3RandomV=out1RandomV
               else:
                  out3RandomV=pD.inPoint[1]-0.8
               linesList = [(self.outObject.outPointD[0]*cm, self.outObject.outPointD[1]*cm), 
                            (self.outObject.outPointD[0]*cm, out1RandomV*cm),
                            (out2RandomH*cm, out1RandomV*cm),
                            (out2RandomH*cm, out3RandomV*cm),
                            (pD.inPoint[0]*cm,  out3RandomV*cm),
                            (pD.inPoint[0]*cm, pD.inPoint[1]*cm)]
               polyLines.add(dwg.polyline(points=linesList))
               endPoint=(pD.inPoint[0], pD.inPoint[1])
               try:
                  writeACommit(dwg=dwg, textLocation=(out2RandomH, out3RandomV), texts=texts, text=pDt[1])
               except:
                  pass
            elif self.outObject.groupNumber > pD.groupNumber:  #This is left path
               out2RandomH=(wideBetweenGroups[(self.outObject.groupNumber-1)][0]+wideBetweenGroups[(self.outObject.groupNumber-1)][1])*0.98/2
               out1RandomV=self.outObject.outPointD[1]+0.6
              #  out2RandomH=random.uniform(wideBetweenGroups[(pD['begin'].groupNumber-1)][0]+0.5, wideBetweenGroups[(pD['begin'].groupNumber-1)][1]-0.5)     
               out3RandomV=pD.inPoint[1]-0.6
               linesList=[(self.outObject.outPointD[0]*cm, self.outObject.outPointD[1]*cm),
                          (self.outObject.outPointD[0]*cm, out1RandomV*cm),
                          (out2RandomH*cm, out1RandomV*cm),
                          (out2RandomH*cm, out3RandomV*cm),
                          (pD.inPoint[0]*cm,  out3RandomV*cm),
                          (pD.inPoint[0]*cm, pD.inPoint[1]*cm)]
               polyLines.add(dwg.polyline(points=linesList))
               endPoint=(pD.inPoint[0], pD.inPoint[1])
               try:
                  writeACommit(dwg=dwg, textLocation=(pD.inPoint[0], out3RandomV), texts=texts, text=pDt[1])
               except:
                  pass
            arrowList = [(pD.inPoint[0]*cm, pD.inPoint[1]*cm),
                         (((endPoint[0]+0.5)*cm, ((endPoint[1]-0.5)*cm))),
                         (((endPoint[0]-0.5)*cm), ((endPoint[1]-0.5)*cm)),
                         (pD.inPoint[0]*cm, pD.inPoint[1]*cm)]
            arrow=dwg.polygon(points=arrowList, stroke='black', stroke_width=1)
            shapes.add(arrow)
      if self.outObject.relateCollect.get('left'):
         for pDt in self.outObject.relateCollect['left']:

            pD = pDt[0]
            out3RandomV=pD.inPoint[1]-0.7
            out2RandomH=(wideBetweenGroups[(self.outObject.groupNumber-1)][0]+wideBetweenGroups[(self.outObject.groupNumber-1)][1])*0.95/2
            lineList=[(self.outObject.outPointL[0]*cm, self.outObject.outPointL[1]*cm),
                       (out2RandomH*cm, self.outObject.outPointL[1]*cm),
                       (out2RandomH*cm, out3RandomV*cm),
                       (pD.inPoint[0]*cm,  out3RandomV*cm),
                       (pD.inPoint[0]*cm, pD.inPoint[1]*cm)]
            polyLines.add(dwg.polyline(points=lineList))
            try:
               textLocation = ((out2RandomH, self.outObject.outPointL[1]))
               writeACommit(dwg=dwg, textLocation=textLocation, texts=texts, text=pDt[1])
            except:
               pass
            arrowList = [(pD.inPoint[0]*cm, pD.inPoint[1]*cm),
                         ((pD.inPoint[0]+0.5)*cm, ((pD.inPoint[1]-0.5)*cm)),
                         (((pD.inPoint[0]-0.5)*cm), ((pD.inPoint[1]-0.5)*cm)),
                         (pD.inPoint[0]*cm, pD.inPoint[1]*cm)]
            arrow=dwg.polygon(points=arrowList, stroke='black', stroke_width=1)
            shapes.add(arrow)
      if self.outObject.relateCollect.get('right'):
         for pDt in self.outObject.relateCollect['right']:
            pD = pDt[0]
            out3RandomV=pD.inPoint[1]-0.7
            out2RandomH=(wideBetweenGroups[(self.outObject.groupNumber)][0]+wideBetweenGroups[(self.outObject.groupNumber)][1])*0.9/2
            lineList=[(self.outObject.outPointR[0]*cm, self.outObject.outPointR[1]*cm),
                      (out2RandomH*cm, self.outObject.outPointR[1]*cm),
                      (out2RandomH*cm, out3RandomV*cm),
                      (pD.inPoint[0]*cm,  out3RandomV*cm),
                      (pD.inPoint[0]*cm, pD.inPoint[1]*cm)]
            polyLines.add(dwg.polyline(points=lineList))
            try:
               text = pDt[1]
               writeACommit(dwg=dwg, textLocation=self.outObject.outPointR, texts=texts, text=pDt[1])
            except:
               pass
            arrowList = [(pD.inPoint[0]*cm, pD.inPoint[1]*cm),
                         (((pD.inPoint[0]+0.5)*cm, ((pD.inPoint[1]-0.5)*cm))),
                         (((pD.inPoint[0]-0.5)*cm), ((pD.inPoint[1]-0.5)*cm)),
                         (pD.inPoint[0]*cm, pD.inPoint[1]*cm)]
            arrow=dwg.polygon(points=arrowList, stroke='black', stroke_width=1)
            shapes.add(arrow)   


