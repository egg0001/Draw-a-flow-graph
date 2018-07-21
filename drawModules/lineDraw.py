import svgwrite
from . import config
import random


random.seed(a=config.randomSeed)
# To produce a analysisable result, providing a random seed is useful.


def randrange_float(start, stop, step):
   '''This function could generate a stepping float to the generation of segments.'''
   return random.randint(0, int((stop - start) / step)) * step + start





class Lines():
   '''This Lines class and its objects contain all the arrows(and its commint) from every shape object. While 
      using any of three shapes objects to construct a Lines objects and exploiting its drawLines method, it
      would analyze the relateCollect attribute in the shape objects and exploit the result to create segments  
      point list preparing to analysis. It also has a writeACommit method to arrange commits on the arrows.'''
   def __init__(self, outObject):
      self.outObject = outObject # This is the shape object
      self.text=''
      self.textLocation = ()
      self.outputLineList = []
      self.lastLineList = []

   def createLinePoints(self, dwg, wideBetweenGroups, shapes, texts, polyLines, cm=config.multiConstant, lineInterval=config.lineinterval,
                 elementInterval=config.elementInterval, groupInterval=config.groupInterval, shapeSize=config.shapeSize):
      '''With a Lines itself, while providing a svgwrite.Drawing object, a svgwrite's texts object (represent a text group in the svg file) 
         and a svgwrite's shape objects (represent a shape group in the svg file) and a wideBetweenGroups variable from shapeObject.groupWide(), 
         it would generate all the segments representing the lines of arrows preparing to further analysis, including the overlapping and line
         crossing. while analysis, it would also create the head of the arrows.'''
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
                  lineList=[(self.outObject.outPointD, (self.outObject.inPoint[0], pD.inPoint[1]))]
                  endPoint=(self.outObject.inPoint[0], pD.inPoint[1])
               else:
                  lineList=[((pD.outPointD[0], self.outObject.outPointD[1]), pD.inPoint)]
                  endPoint = (pD.inPoint[0], pD.inPoint[1])
                  
               try:
                 self.text=pDt[1]
                 self.textLocation = (endPoint[0], (endPoint[1]+self.outObject.outPointD[1])*1.03/2)
            #      writeACommit(dwg=dwg, textLocation=textLocation, texts=texts, text=pDt[1])
               except:
                  self.text=''
                  self.textLocation=()        
               lastLineList.append([lineList[0][0], lineList[0][1]])
               outputLineList.extend(lineList)
            elif (self.outObject.groupNumber <= pD.groupNumber):# This is right path
               if (self.outObject.groupNumber == pD.groupNumber):
                  out2RandomH=randrange_float(wideBetweenGroups[self.outObject.groupNumber][0]+0.3*(groupInterval/5), 
                                              wideBetweenGroups[self.outObject.groupNumber][1]-0.3*(groupInterval/5), 
                                              lineInterval)
               else:
                  out2RandomH=randrange_float(wideBetweenGroups[(pD.groupNumber-1)][0]+0.3*(groupInterval/5), 
                                              wideBetweenGroups[(pD.groupNumber-1)][1]-0.3*(groupInterval/5),
                                              lineInterval)
               out1RandomV=randrange_float(self.outObject.outPointD[1]+0.2*(elementInterval/5), 
                                           self.outObject.outPointD[1]+1*(elementInterval/5), lineInterval)

               out3RandomV=randrange_float(pD.inPoint[1]-1.8*(elementInterval/5), pD.inPoint[1]-0.4*(elementInterval/5), lineInterval)
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
               out2RandomH=randrange_float(wideBetweenGroups[(self.outObject.groupNumber-1)][0]+0.3*(groupInterval/5), 
                                           wideBetweenGroups[(self.outObject.groupNumber-1)][1]-0.3*(groupInterval/5), 
                                           lineInterval)
               out1RandomV=randrange_float(self.outObject.outPointD[1]+0.2*(elementInterval/5), 
                                           self.outObject.outPointD[1]+1*(elementInterval/5), 
                                           lineInterval)
              #  out2RandomH=random.uniform(wideBetweenGroups[(pD['begin'].groupNumber-1)][0]+0.5, wideBetweenGroups[(pD['begin'].groupNumber-1)][1]-0.5)     
               out3RandomV=randrange_float(pD.inPoint[1]-1.8*(elementInterval/5), pD.inPoint[1]-0.4*(elementInterval/5), lineInterval)
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
                         (((endPoint[0]*cm+0.2*cm*shapeSize), ((endPoint[1]*cm-0.2*cm*shapeSize)))),
                         ((endPoint[0]*cm-0.2*cm*shapeSize), ((endPoint[1]*cm-0.2*cm*shapeSize))),
                         (pD.inPoint[0]*cm, pD.inPoint[1]*cm)]
            arrow=dwg.polygon(points=arrowList, stroke='black', stroke_width=1)
            shapes.add(arrow)
      if self.outObject.relateCollect.get('left'):
         for pDt in self.outObject.relateCollect['left']:

            pD = pDt[0]
            out3RandomV=pD.inPoint[1]-0.7*(elementInterval/5)
            out2RandomH=randrange_float(wideBetweenGroups[(self.outObject.groupNumber-1)][0]+0.3*(groupInterval/5), 
                                        wideBetweenGroups[(self.outObject.groupNumber-1)][1]-0.7*(groupInterval/5), 
                                        lineInterval)
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
            out3RandomV=pD.inPoint[1]-0.70*(elementInterval/5)
            out2RandomH=randrange_float(wideBetweenGroups[(self.outObject.groupNumber)][0]+0.7*(groupInterval/5), 
                                        wideBetweenGroups[(self.outObject.groupNumber)][1]-0.3*(groupInterval/5), 
                                        lineInterval)
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
      self.outputLineList = outputLineList
      self.lastLineList =lastLineList
      return  #Line result
   def writeACommit(self, dwg, texts, cm=config.multiConstant, fontSize=config.commitSize):
      '''the drawLines method in Lines class would exploit this function to write commits on the arrows. It should only be used 
         after the segment analysis completed.'''
      text = dwg.text(text=self.text, insert=(self.textLocation[0]*cm, self.textLocation[1]*cm), style='font-size:{0}'.format(fontSize*(cm/37.79)))
      texts.add(text)


                         

class lineEvaluation():
   '''While the segment list from all the Lines objects is provided to create a lineEvaluation object, this object's evaluateOverlap
      method would analysis all the segments and find out whether these segments exist issues, including the overlapping and line 
      crossing. If it does not detect any issue, the reallyDrawLine method would draw the segment on the svg object.'''
   def __init__(self, pointList, lastLineList):
      self.pointList=pointList
      self.lastLineList = lastLineList
      self.overlapList =[]
      self.overlapPoint = []
      self.vertical = []
      self.horizontal = []
      self.overlapX = False
      self.overlapY = False

   def evaluateOverlap(self, lineinterval=config.lineinterval):
      '''This method would analysis most of the issues before drawing. After the analysis, this method would alter the bool values of
         overlapX and overlapY attributes of the lineEvaluation to represent whether this segments encounter any overlapping issue. If
         one of this attributes is True, the lines objects should be discard and re-create since the Line object would exploit random 
         to create those new segments. Moreover, it would also add a overlapPoint attribute after analysis to deal with line corssing
         issue
      '''
      lC = lineinterval/0.2
#       print (self.lastLineList)
      self.lastLineList.sort()
      print (self.lastLineList)
      vertical = []
      horizontal = []
      overlapList = [] # overlapList = [[(p1),(p2)], [(p3), (p4)].....]
      overpalLineList=[]
      for pL in self.pointList:
         pL = list(pL)
         pL.sort()
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
                                          (segmentList[nextSegmentIndex][0]-0.1*lC, segmentList[nextSegmentIndex][1])])
               elif segmentList.index(segment) < (len(segmentList)-2):
                  nextSegmentIndex = segmentList.index(segment) +1
                  self.horizontal.append([(segment[0]+0.1*lC, segment[1]), 
                                          (segmentList[nextSegmentIndex][0]-0.1*lC, segmentList[nextSegmentIndex][1])])
               elif segmentList.index(segment) == (len(segmentList)-2):

                  nextSegmentIndex = segmentList.index(segment) +1

                  self.horizontal.append([(segment[0]+0.1*lC, segment[1]), 
                                           (segmentList[nextSegmentIndex][0], segmentList[nextSegmentIndex][1])])
               else:
                  pass
            overpalLineList.append(h)
      lastPoint = []
      for lastLine in self.lastLineList:
         lastLine.sort()
         lastPoint.append(lastLine[1][1])
#       print(lastPoint)
      for currentLine in vertical:
         currentLine.sort()
        #  print (currentLine[1][1])
         if currentLine[1][1] not in lastPoint:
        #     print (currentLine[1][1])
            for others in vertical:
               currentLine.sort()
               others.sort()
               if currentLine==others:
                  continue
               if ((abs(others[0][0]-currentLine[0][0])<0.1) and ((currentLine[1][1]>=others[0][1] and currentLine[0][1]<=others[0][1])
                  or (currentLine[1][1]<=others[1][1] and currentLine[1][1]>others[0][1]) or (currentLine[1][1]>=others[1][1] and
                  currentLine[0][1]<=others[0][1]) or(currentLine[1][1]<=others[1][1] and currentLine[1][1]>=others[0][1]) 
                  or(currentLine[1][1]>=others[1][1] and currentLine[0][1]<=others[0][1]) or() )):
                  self.overlapX = True
                  print(currentLine)
                  print (others)
                  break
            if self.overlapX == True:
               break
         else:
            pass
      for h in horizontal:
         currentLine = h
         for others in horizontal:
            currentLine.sort()
            others.sort()
            if currentLine==others:
               continue
            if ((abs(others[0][1]-currentLine[0][1])<0.1) and ((currentLine[1][0]>=others[1][0] and currentLine[0][0]<=others[0][0]) or 
                (currentLine[1][0]>=others[0][0] and currentLine[0][0]<=others[1][0]) or 
                (currentLine[0][0]==others[0][0] or currentLine[1][0]==others[1][0]) or (currentLine[1][0]<=others[1][0] and 
                currentLine[0][0]>=others[0][0]) or (currentLine[1][0]>=others[1][0] and currentLine[0][0]<=others[0][0]))):
               self.overlapY = True
               break
      for pL in self.pointList:
         if pL[0][0] == pL[1][0]:
            self.vertical.append(pL)
         elif pL[0][1] == pL[1][1] and (pL not in overpalLineList):
            self.horizontal.append(pL)

   def reallyDrawLine(self, dwg, vlines, hlines, cm=config.multiConstant, lineInterval=config.lineinterval):
      '''If overlapX and overlapY attributes are both False after analysis, this method, with a Drawing object, vline
         and hlines object for the groupping, would really draw all the segments on the svg object.'''
      lC = lineInterval/0.2
      for pL in self.vertical:
         vlines.add(dwg.line(start=(pL[0][0]*cm, pL[0][1]*cm), 
                             end=(pL[1][0]*cm, pL[1][1]*cm)))

      for pL in self.horizontal:
         hlines.add(dwg.line(start=(pL[0][0]*cm, pL[0][1]*cm), 
                             end=(pL[1][0]*cm, pL[1][1]*cm)))  

      
      for points in self.overlapPoint:
         vlines.add(dwg.line(start=((points[0]-0.1*lC)*cm, points[1]*cm), 
                             end=((points[0]-0.1*lC)*cm, (points[1]-0.1*lC)*cm)))
         hlines.add(dwg.line(start=((points[0]-0.1*lC)*cm, (points[1]-0.1*lC)*cm),
                             end=((points[0]+0.1*lC)*cm, (points[1]-0.1*lC)*cm)))
         vlines.add(dwg.line(start=((points[0]+0.1*lC)*cm, (points[1]-0.1*lC)*cm), 
                             end=((points[0]+0.1*lC)*cm, (points[1])*cm))) 