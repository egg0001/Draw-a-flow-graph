#!/usr/bin/python3

import svgwrite
from . import config

class Group():
   '''This Group class is the parent class for all other shape classes, it contributes two important 
      attributes for the child classes-groupNumber/x and elementOrder/y. It also maintains a list
      containing all the shapes objects for analyzing wide between every group.'''
   objectList = []  # This list contains all the shapes objects. DO NOT REMOVE ANY OBJECT FROM THIS LIST
   def __init__(self, groupNumber, elementOrder):
      self.groupNumber = groupNumber  # groupNumber/x location
      self.elementOrder = elementOrder # elementOrder/y location
      self.wideBetweenGroups={} # The wide information between every group
      Group.objectList.append(self)


   def groupWide(self):
      '''This method would exploit objectList to analyze the wide between groups and generate a dict
         variable to represent the result. To use this method, please use childObject.groupWide()'''
      groupList = []
      for obj in Group.objectList:
         groupList.append(obj.groupNumber)
      groupList = list(set(groupList))
      self.wideBetweenGroups.update({0:(0,2)})
      for gL in groupList:
         maxWide = 0
         for obj in Group.objectList:
            # try:
            if obj.groupNumber == gL and ((obj.shapeLocation[0]+obj.shapeSize[0]) > maxWide):
               maxWide = obj.shapeLocation[0]+obj.shapeSize[0]
            # except:
            #    pass
         self.wideBetweenGroups.update({gL:(maxWide,maxWide+4)})

      return self.wideBetweenGroups

class Circle(Group):
   ''''This Circle class and its objects contain all the necessary attributes to create a circle object
       usually means start and end in the flow graph. It also contains a method to create this circle 
       object to the .svg file. To create a circle object, user should provide a name, the text message
       inside this circle, the groupNumber-x (int) as well as elementOrder-y (int) to mount its location, and 
       the relateCollect dict variable containing all the target objects and commits from a circle object 
       Example: relateCollect = {'down': [(object1, 'commit1'), (object2, 'commit2')]}, if no commit, 
       relateCollect = {'down': [(object1), (object2)]}'''
   def __init__(self, groupNumber, elementOrder, name, text):
      Group.__init__(self, groupNumber, elementOrder)
      self.name=name # str, This is the name of the object
      self.text=text # This is the message containing in the circle
      self.shapeSize= () # This attribute determing the size of the circle
      self.textLocation = () # This attribute determing the location of the text in circle
      self.shapeLocation = ()# This attribute determing the location the circle. It would be 
                             # automatically calculated by textLocation
      self.inPoint = ()      # This attribute indicates where the arrows would arrive to this circle.
                             # Auto calculated
      self.outPointL = None  # Circle would only extend arrows from bottom.
      self.outPointD = ()   # This attribute indicates where the arrows would leave from this circle.
                            # Auto calculated
      self.outPointR = None # Circle would only extend arrows from bottom.
      self.relateCollect = {'down': [], 'left': [], 'right': []}  # This dict contains all the target 
      # shape objects and the commint on the arrows  from a specifide circle object 

   def drawCircle(self, dwg, texts, shapes, objectList=Group.objectList, cm=config.multiConstant):
      '''While exploit this method, the program would draw a circle in the svg file. With the circle object
         itself, it also needs a svgwrite.Drawing object, a objectlist from Group class, a svgwrite's texts
         object (represent a text group in the svg file) and a svgwrite's shape objects (represent a shape 
         group in the svg file)'''
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
      text = dwg.text(text=self.text, insert=(self.textLocation[0]*cm,self.textLocation[1]*cm), style='font-size:{0}'.format((0.7/0.0352)*(cm/37.79)))
      texts.add(text)

      self.shapeLocation = (self.textLocation[0]-0.55, self.textLocation[1])
      self.shapeSize=(wordsNum*0.3, 0.3)
      center=(self.shapeLocation[0]+self.shapeSize[0]/2, self.shapeLocation[1])
      r=self.shapeSize[0]/2
      circle=dwg.circle(center=(center[0]*cm, center[1]*cm), r=r*cm, stroke='blue', stroke_width=3*(cm/37.79))
      self.inPoint=(center[0], center[1]-r)
      self.outPointD=(center[0], center[1]+r)
      shapes.add(circle)
      

class Rhombus(Group):
   ''''This Rhombus class and its objects contain all the necessary attributes to create a rhombus object
       usually means determination in the flow graph. It also contains a method to create this rhombus 
       object to the .svg file. To create a rhombus object, user should provide a name, the text message
       inside this rhombus, the groupNumber, x position (int), as well as elementOrder, y position (int), to mount its location, 
       and the relateCollect dict variable containing all the target objects and commits from this rhombus object 
       Example: relateCollect = {'down': [(object1, 'commit1'), (object2, 'commit2')], 'left': 
       [(object3, 'commit3'), (object4, 'commit4')]}, if no commit, relateCollect = {'down': [(object1), (object2)]}'''
   def __init__(self, groupNumber, elementOrder, name, text):
      Group.__init__(self, groupNumber, elementOrder)
      self.name=name # str, This is the name of the object
      self.text=text # This is the message containing in the rhombus
      self.shapeSize= () # This attribute determing the size of the rhombus
      self.textLocation = () # This attribute determing the location of the text in rhombus
      self.shapeLocation = ()# This attribute determing the location the rhombus. It would be 
                             # automatically calculated by textLocation
      self.inPoint = ()      # This attribute indicates where the arrows would arrive in this rhombus.
                             # Auto calculated
      self.outPointL = ()   # This attribute indicates where the arrows would leave from this rhombus on left side.
                            # Auto calculated
      self.outPointD = ()   # This attribute indicates where the arrows would leave from this rhombus.
                            # Auto calculated
      self.outPointR = () # This attribute indicates where the arrows would leave from this rhombus on right side.
                           # Auto calculated
      self.relateCollect = {'down': [], 'left': [], 'right': []}  # This dict contains all the target 
      # shape objects and the commint on the arrows  from a specifide rhombus object 
   
   def drawRhom(self, dwg, texts, shapes, objectList=Group.objectList, cm=config.multiConstant):
      '''While exploit this method, the program would draw a rhombus in the svg file. With the rhombus object
         itself, it also needs a svgwrite.Drawing object, a objectlist from Group class, a svgwrite's texts
         object (represent a text group in the svg file) and a svgwrite's shape objects (represent a shape 
         group in the svg file)'''
      wordsNum = len(self.text.encode('utf-8'))
      objectList.sort(key=lambda x: x.elementOrder)
      objectList.sort(key=lambda x: x.groupNumber)
      index = objectList.index(self)
      if index == 0:
         self.textLocation = (self.groupNumber*3, self.elementOrder*5)   # Seems could be used to sed a size style 
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
      text = dwg.text(text=self.text, insert=(self.textLocation[0]*cm,self.textLocation[1]*cm), style='font-size:{0}'.format((0.7/0.0352)*(cm/37.79)))
      texts.add(text)
      # text = dwg.text(text=self.text, insert=(self.textLocation[0]*cm,self.textLocation[1]*cm), style='font-size:{0}'.format(0.7/0.0352*(cm/37.79)))
      self.shapeLocation = (self.textLocation[0]-1, self.textLocation[1]-0.2)
      self.shapeSize=(wordsNum*0.42, 1.2)
      rhomList=[(self.shapeLocation[0]*cm, self.shapeLocation[1]*cm),
                ((self.shapeLocation[0]+self.shapeSize[0]/2)*cm, (self.shapeLocation[1]-self.shapeSize[1])*cm),
                ((self.shapeLocation[0]+self.shapeSize[0])*cm, self.shapeLocation[1]*cm),
                ((self.shapeLocation[0]+self.shapeSize[0]/2)*cm, (self.shapeLocation[1]+self.shapeSize[1])*cm),
                (self.shapeLocation[0]*cm, self.shapeLocation[1]*cm)]

      rhom=dwg.polygon(points=rhomList, stroke='blue', stroke_width=3*(cm/37.79))
      self.inPoint=(self.shapeLocation[0]+self.shapeSize[0]/2, self.shapeLocation[1]-self.shapeSize[1])
      self.outPointR=(self.shapeLocation[0]+self.shapeSize[0], self.shapeLocation[1])
      self.outPointL=self.shapeLocation   
      self.outPointD=(self.shapeLocation[0]+self.shapeSize[0]/2, self.shapeLocation[1]+self.shapeSize[1])
      shapes.add(rhom)

class Rectangal(Group):
   ''''This Rectangal class and its objects contain all the necessary attributes to create a rectangal object
       usually means progress in the flow graph. It also contains a method to create this rectangal 
       object to the .svg file. To create a rectangal object, user should provide a name, the text message
       inside this rectangal, the groupNumber, x position (int), as well as elementOrder, y position (int), to mount its location, 
       and the relateCollect dict variable containing all the target objects and commits from this rectangal object 
       Example: relateCollect = {'down': [(object1, 'commit1'), (object2, 'commit2')]]}, , if no commit, 
       relateCollect = {'down': [(object1), (object2)]}.
       To maintain all the object's locations, user should create a fundation Rectangal object at groupNumber=1
       , elementOrder=1 and set the fundation=True'''
   def __init__(self, groupNumber, elementOrder, name, text='Hello World!', fundation=False):
      Group.__init__(self, groupNumber, elementOrder)
      self.name=name # str, This is the name of the object
      self.text=text # This is the message containing in the rectangal
      self.shapeSize= () # This attribute determing the size of the rectangal
      self.textLocation = () # This attribute determing the location of the text in rectangal
      self.shapeLocation = ()# This attribute determing the location the rectangal. It would be 
                             # automatically calculated by textLocation
      self.inPoint = ()      # This attribute indicates where the arrows would arrive to this rectangal.
                             # Auto calculated
      self.outPointL = None  # Rectangal would only extend arrows from bottom.
      self.outPointD = ()   # This attribute indicates where the arrows would leave from this rectangal.
                            # Auto calculated
      self.outPointR = None # rectangal would only extend arrows from bottom.
      self.relateCollect = {'down': [], 'left': [], 'right': []}  # This dict contains all the target 
      # shape objects and the commint on the arrows  from a specifide rectangal object 
      self.foundation = fundation # If true, the object would be transparent.
   
   def drawRect(self, dwg, texts, shapes, objectList=Group.objectList, cm=config.multiConstant):
      '''While exploit this method, the program would draw a rectangal in the svg file. With the rectangal object
         itself, it also needs a svgwrite.Drawing object, a objectlist from Group class, a svgwrite's texts
         object (represent a text group in the svg file) and a svgwrite's shape objects (represent a shape 
         group in the svg file)'''
      wordsNum = len(self.text.encode('utf-8'))
      objectList.sort(key=lambda x: x.elementOrder)
      objectList.sort(key=lambda x: x.groupNumber)
      index = objectList.index(self)
      if index == 0:
         self.textLocation = (self.groupNumber*3, self.elementOrder*5)   # Seems could be used to set a size style 
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
         text = dwg.text(text=self.text, insert=(self.textLocation[0]*cm,self.textLocation[1]*cm), style='font-size:{0}'.format((0.7/0.0352)*(cm/37.79)))
         stroke_width=3*(cm/37.79)
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

