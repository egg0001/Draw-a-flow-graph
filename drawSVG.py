#!/usr/bin/python3

import svgwrite
from drawModules.shapeDraw import Group, Circle, Rectangal, Rhombus
from drawModules.lineDraw import Lines
from drawModules import config 


def basic_shapes(name, cm=config.multiConstant):

   dwg = svgwrite.Drawing(filename=name, debug=True)
  #  drawALine(dwg=dwg)
  #  vlines = dwg.add(dwg.g(id='testID', stroke='black'))
  # # #  for y in range(20):
  # # #     vlines.add(dwg.line(start=(2*cm, (2+y)*cm), end=(18*cm, (2+y)*cm)))
  #  hlines = dwg.add(dwg.g(id='vlines', stroke='green'))
   
  #  for y in range(40):
  #     hlines.add(dwg.line(start=(0*cm, (y)*cm), end=(40*cm, (y)*cm)))
  #  vlines = dwg.add(dwg.g(id='hline', stroke='blue'))
  #  for x in range(40):
  #     vlines.add(dwg.line(start=((x)*cm, 0*cm), end=((x)*cm, 40*cm)))
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
   circle1.relateCollect['down'].append((rect3, 'helloworld'))
   rhombus1 = Rhombus(name='test1', text='Hello World!', groupNumber=3, elementOrder=2)

   rhombus1.drawRhom(dwg=dwg,texts=texts,shapes=shapes)
   rect6 = Rectangal(name='test1', text='Hello World!', groupNumber=3, elementOrder=3)

   rect6.drawRect(dwg=dwg,texts=texts,shapes=shapes)
   rect7 = Rectangal(name='test1', text='Hello World!', groupNumber=4, elementOrder=1)

   rect7.drawRect(dwg=dwg,texts=texts,shapes=shapes)
   rhombus1.relateCollect['left'].append((circle2, 'helloworld'))
   lines4 = Lines(outObject=rhombus1)
   lines2 = Lines(outObject=rect4)
   rect3.relateCollect['down'].extend([(rhombus1, 'helloworld')])
   lines3 = Lines(rect3)
   rect4.relateCollect['down'].extend([(circle2, 'helloworld'), (rect5, 'helloworld')])
   lines1 = Lines(outObject=circle1)
   lines1.drawLines(dwg=dwg, wideBetweenGroups=circle1.groupWide(), shapes=shapesFilled, texts=texts, polyLines=polyLines)
  #  lines2.drawLines(dwg=dwg, wideBetweenGroups=Group.groupWide(rect4), shapes=shapesFilled, texts=texts, polyLines=polyLines)
   lines3.drawLines(dwg=dwg, wideBetweenGroups=Group.groupWide(rect3), shapes=shapesFilled, texts=texts, polyLines=polyLines)
   lines4.drawLines(dwg=dwg, wideBetweenGroups=Group.groupWide(rhombus1), shapes=shapesFilled, texts=texts, polyLines=polyLines)
   dwg.save()


if __name__ == '__main__':
   basic_shapes('basic_shapes.svg')