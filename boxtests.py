#!/usr/bin/python2

import unittest
import core
import patterns
import main
import math

from ptests import *


class TestDbCylinderPattern(unittest.TestCase,PatternTests):

	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.DbCylinderPattern
	
	def test_accepts_cylinder(self):
		input = [
			".--.\n",
			"'--'\n",
			"|  |\n",
			"'--'\n",
			"    " ]
		p = self.pclass()
		for j,line in enumerate(input):
			for i,char in enumerate(line):
				p.test(main.CurrentChar(j,i,char,core.M_NONE))
		try:
			p.test(main.CurrentChar(len(input),0," ",core.M_NONE))
		except StopIteration: pass
		
	def test_expects_top_start_period(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,"p",core.M_NONE))
			
	def test_expects_top_start_period_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,".",core.M_OCCUPIED))
			
	def test_expects_top_line(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,0,".",core.M_NONE))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,1,".",core.M_NONE))
			
	def test_expects_top_line_unoccupied(self):
		p = self.pclass()
		p.test(main.CurrentChar(0,0,".",core.M_NONE))
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,0,"-",core.M_OCCUPIED))
			
	def test_expects_top_end_period(self):
		p = self.pclass()
		feed_input(p,0,0,".-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_NONE))
			
	def test_expects_top_end_period_unoccupie(self):
		p = self.pclass()
		feed_input(p,0,0,".-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,".",core.M_OCCUPIED))
		
	def test_allows_long_top_line(self):
		p = self.pclass()
		feed_input(p,0,1,".---.")

	def test_allows_rest_of_top_line(self):
		p = self.pclass()
		feed_input(p,0,1,".-.")
		p.test(main.CurrentChar(0,2,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,3,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,4,"\n",core.M_OCCUPIED))
		
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,".-.\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))		
	
	def test_expects_top_start_apos(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,0,"|",core.M_NONE))
			
	def test_expects_top_start_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,0,"'",core.M_OCCUPIED))
	
	def test_expects_top_underline(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,1,"'",core.M_NONE))
	
	def test_expects_top_underline_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,1,"-",core.M_OCCUPIED))
	
	def test_rejects_top_underline_too_short(self):
		p = self.pclass()
		feed_input(p,0,0,".--.\n")
		feed_input(p,1,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"'",core.M_NONE))
			
	def test_rejects_top_underline_too_lone(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"-",core.M_NONE))
	
	def test_expects_top_end_apos(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"a",core.M_NONE))
			
	def test_expects_top_end_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"'",core.M_OCCUPIED))
	
	def test_allows_rest_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'")
		p.test(main.CurrentChar(1,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,5,"\n",core.M_OCCUPIED))
	
	def test_allows_start_of_third_line(self):
		p = self.pclass()
		feed_input(p,0,2,".-.\n")
		feed_input(p,1,0,"  '-'\n")
		p.test(main.CurrentChar(2,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,1,"x",core.M_OCCUPIED))
	
	def test_expects_mid_start_pipe(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,0,"'",core.M_NONE))
						
	def test_expects_mid_start_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,0,"|",core.M_OCCUPIED))
			
	def test_allows_mid_space(self):
		p = self.pclass()
		feed_input(p,0,0,".--.\n")
		feed_input(p,1,0,"'--'\n")
		feed_input(p,2,0,"|")
		p.test(main.CurrentChar(2,1,"p",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,2,"q",core.M_OCCUPIED))

	def test_rejects_short_mid_space_line(self):
		p = self.pclass()
		feed_input(p,0,0,".--.\n")
		feed_input(p,1,0,"'--'\n")
		feed_input(p,2,0,"| \n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,0," ",core.M_NONE))
	
	def test_expects_mid_end_pipe(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"p",core.M_NONE))
			
	def test_expects_mid_end_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"|",core.M_OCCUPIED))
			
	def test_allows_end_of_third_line(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |")
		p.test(main.CurrentChar(2,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,4,"z",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,5,"\n",core.M_OCCUPIED))	
	
	def test_allows_start_of_last_line(self):
		p = self.pclass()
		feed_input(p,0,2,  ".-.\n")
		feed_input(p,1,0,"  '-'\n")
		feed_input(p,2,0,"  | |\n")
		p.test(main.CurrentChar(3,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(3,1,"x",core.M_OCCUPIED))
		
	def test_expects_bottom_start_apos(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,0,"z",core.M_NONE))
		
	def test_expects_bottom_start_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,0,"'",core.M_OCCUPIED))
			
	def test_expects_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"'")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,1,"'",core.M_NONE))
			
	def test_expects_bottom_line_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"'")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,1,"-",core.M_OCCUPIED))
	
	def test_rejects_bottom_line_too_short(self):
		p = self.pclass()
		feed_input(p,0,0,".--.\n")
		feed_input(p,1,0,"'--'\n")
		feed_input(p,2,0,"|  |\n")
		feed_input(p,3,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,2,"'",core.M_NONE))
	
	def test_rejects_bottom_line_too_long(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,2,"-",core.M_NONE))
			
	def test_expects_bottom_end_apos(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,2,"z",core.M_NONE))
			
	def test_expects_bottom_end_apos_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"'-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(3,2,"'",core.M_OCCUPIED))
			
	def test_allows_rest_of_last_line(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"'-'ab\n")
		
	def test_accepts_partial_line_after(self):
		p = self.pclass()
		feed_input(p,0,0,".--.\n")
		feed_input(p,1,0,"'--'\n")
		feed_input(p,2,0,"|  |\n")
		feed_input(p,3,0,"'--'\n")
		feed_input(p,4,0,"ab\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(5,0,"c",core.M_NONE))
			
	def test_accepts_no_line_after(self):
		p = self.pclass()
		feed_input(p,0,0,".--.\n")
		feed_input(p,1,0,"'--'\n")
		feed_input(p,2,0,"|  |\n")
		feed_input(p,3,0,"'--'\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_multiple_mid_lines(self):
		p = self.pclass()
		feed_input(p,0,0,".-.\n")
		feed_input(p,1,0,"'-'\n")
		feed_input(p,2,0,"| |\n")
		feed_input(p,3,0,"| |\n")
		feed_input(p,4,0,"| |\n")
		
	def test_sets_correct_meta_flags(self):
		input = ((2,  ".---.  \n",),
		         (0,"  '---'  \n",),
		         (0,"  |   |  \n",),
		         (0,"  '---'  \n",),
		         (0,"       "    ,))
		c = core.M_OCCUPIED | core.M_BOX_START_S | core.M_BOX_START_E
		t = core.M_OCCUPIED | core.M_BOX_START_S
		l = core.M_OCCUPIED | core.M_BOX_START_E
		n = core.M_NONE
		o = core.M_OCCUPIED
		r = core.M_BOX_AFTER_E
		b = core.M_BOX_AFTER_S
		meta =  ((    c,t,t,t,t,r,n,n,),
				 (n,n,l,o,o,o,o,r,n,n,),
				 (n,n,l,n,n,n,o,r,n,n,),
				 (n,n,l,o,o,o,o,r,n,n,),
				 (n,n,b,b,b,b,b       ))
		p = self.pclass()
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE))
				self.assertEquals(meta[j][i],m)

	def do_render(self,x,y,w,h):
		p = self.pclass()
		feed_input(p,y,x,                "." + "-"*w + ".\n")
		feed_input(p,y+1,0,      " "*x + "'" + "-"*w + "'\n")
		for i in range(h):
			feed_input(p,y+2+i,0," "*x + "|" + " "*w + "|\n")
		feed_input(p,y+2+h,0,    " "*x + "'" + "-"*w + "'\n")
		feed_input(p,y+2+h+1,0,  " "*x + " " + " "*w + " "  )
		try:
			p.test(main.CurrentChar(y+2+h+1,x+1+w+1,"\n",core.M_NONE))
		except StopIteration: pass
		return p.render()
			
	def test_render_returns_correct_shapes(self):
		result = self.do_render(2,2,3,1)
		self.assertEquals(4,len(result))
		self.assertEquals(1,len(filter(lambda x: isinstance(x,core.Ellipse), result)))
		self.assertEquals(1,len(filter(lambda x: isinstance(x,core.Arc), result)))
		self.assertEquals(2,len(filter(lambda x: isinstance(x,core.Line), result)))
			
	def test_render_line_coordinates(self):
		lines = filter(lambda x: isinstance(x,core.Line), self.do_render(2,2,3,1))
		linea = find_with(self,lines,"a",(2.5,3))
		self.assertEquals((2.5,5),linea.b)
		lineb = find_with(self,lines,"a",(6.5,3))
		self.assertEquals((6.5,5),lineb.b)
		
	def test_render_line_coordinates_wider(self):
		lines = filter(lambda x: isinstance(x,core.Line), self.do_render(5,1,5,1))
		linea = find_with(self,lines,"a",(5.5,2))
		self.assertEquals((5.5,4),linea.b)
		lineb = find_with(self,lines,"a",(11.5,2))
		self.assertEquals((11.5,4),lineb.b)
		
	def test_render_line_coordinates_taller(self):
		lines = filter(lambda x: isinstance(x,core.Line), self.do_render(3,2,3,3))
		linea = find_with(self,lines,"a",(3.5,3))
		self.assertEquals((3.5,7), linea.b)
		lineb = find_with(self,lines,"a",(7.5,3))
		self.assertEquals((7.5,7), lineb.b)
		
	def test_render_ellipse_coordinates(self):
		ellipse = filter(lambda x: isinstance(x,core.Ellipse), self.do_render(2,2,3,1))[0]
		self.assertEquals((2.5,2.5),ellipse.a)
		self.assertEquals((6.5,3.5),ellipse.b)
		
	def test_render_ellipse_coordinates_wider(self):
		ellipse = filter(lambda x: isinstance(x,core.Ellipse), self.do_render(3,2,4,1))[0]
		self.assertEquals((3.5,2.5),ellipse.a)
		self.assertEquals((8.5,3.5),ellipse.b)

	def test_render_ellipse_coordinates_taller(self):
		ellipse = filter(lambda x: isinstance(x,core.Ellipse), self.do_render(4,1,3,3))[0]
		self.assertEquals((4.5,1.5),ellipse.a)
		self.assertEquals((8.5,2.5),ellipse.b)
		
	def test_render_arc_coordinates(self):
		arc = filter(lambda x: isinstance(x,core.Arc), self.do_render(2,2,3,1))[0]
		self.assertEquals((2.5,4.5),arc.a)
		self.assertEquals((6.5,5.5),arc.b)
		self.assertEquals(0,arc.start)
		self.assertEquals(math.pi,arc.end)
		
	def test_render_arc_coordinates_wider(self):
		arc = filter(lambda x: isinstance(x,core.Arc), self.do_render(3,1,4,1))[0]
		self.assertEquals((3.5,3.5),arc.a)
		self.assertEquals((8.5,4.5),arc.b)
		self.assertEquals(0,arc.start)
		self.assertEquals(math.pi,arc.end)
	
	def test_render_arc_coordinates_taller(self):
		arc = filter(lambda x: isinstance(x,core.Arc), self.do_render(2,2,3,4))[0]
		self.assertEquals((2.5,7.5),arc.a)
		self.assertEquals((6.5,8.5),arc.b)
		self.assertEquals(0,arc.start)
		self.assertEquals(math.pi,arc.end)
	
	def test_render_z(self):
		result = self.do_render(2,2,3,4)
		for r in result:
			self.assertEquals(0,r.z)
				
	def test_render_stroke_colour(self):
		result = self.do_render(2,2,3,4)
		for r in result:
			self.assertEquals(core.C_FOREGROUND,r.stroke)
			
	def test_render_stroke_width(self):
		result = self.do_render(2,2,3,4)
		for r in result:
			self.assertEquals(1,r.w)

	def test_render_stroke_style(self):
		result = self.do_render(2,2,3,4)
		for r in result:
			self.assertEquals(core.STROKE_SOLID,r.stype)
			
	def test_render_fill_colour(self):
		result = filter(lambda x: not isinstance(x,core.Line), self.do_render(2,2,3,4))
		for r in result:
			self.assertEquals(None,r.fill)



class TestRectangularBoxPattern(unittest.TestCase,PatternTests):

	def __init__(self,*args,**kargs):
		unittest.TestCase.__init__(self,*args,**kargs)
		self.pclass = patterns.RectangularBoxPattern	
	
	def test_accepts_box(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-----+ \n")
		feed_input(p,1,0,"  |     | \n")
		feed_input(p,2,0,"  |     | \n")
		feed_input(p,3,0,"  +-----+ \n")
		feed_input(p,4,0,"         ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,9," ",core.M_NONE))
			
	def test_expects_top_left_plus(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"?",core.M_NONE))
			
	def test_expects_top_left_plus_unoccupied(self):
		p = self.pclass()
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,2,"+",core.M_OCCUPIED))
			
	def test_expects_top_hyphen(self):
		p = self.pclass()
		feed_input(p,0,2,"+")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"+",core.M_NONE))
			
	def test_expects_top_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,"+")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,3,"-",core.M_OCCUPIED))
			
	def test_allows_single_char_width(self):
		p = self.pclass()
		feed_input(p,0,2,"+-+")
			
	def test_expects_top_right_plus(self):
		p = self.pclass()
		feed_input(p,0,2,"+-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"?",core.M_NONE))
			
	def test_expects_top_right_plus_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,"+-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4,"+",core.M_OCCUPIED))
			
	def test_allows_long_width(self):
		p = self.pclass()
		feed_input(p,0,2,"+-------------+")
	
	def test_allows_rest_of_first_line(self):
		p = self.pclass()
		feed_input(p,0,2,"+---+")
		p.test(main.CurrentChar(0,7,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,8,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(0,9,"\n",core.M_OCCUPIED))
	
	def test_allows_start_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,"+---+\n")
		p.test(main.CurrentChar(1,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,1,"b",core.M_OCCUPIED))
		
	def test_expects_left_pipe(self):
		p = self.pclass()
		feed_input(p,0,2,"+---+\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"+",core.M_NONE))
			
	def test_expects_left_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,"+---+\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"|",core.M_OCCUPIED))
	
	def test_allows_box_contents(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |")
		p.test(main.CurrentChar(1,3,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,4,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,5,"c",core.M_OCCUPIED))
		
	def test_rejects_short_content_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,5,"\n",core.M_NONE))
		
	def test_expects_right_pipe(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,6,"a",core.M_NONE))
			
	def test_expects_right_pipe_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,6,"|",core.M_OCCUPIED))
			
	def test_allows_rest_of_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |")
		p.test(main.CurrentChar(1,7,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,8,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(1,9,"\n",core.M_OCCUPIED))
	
	def test_allows_start_of_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		p.test(main.CurrentChar(2,0,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,1,"b",core.M_OCCUPIED))
		
	def test_allows_single_char_height(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +")
		
	def test_expects_bottom_left_plus(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"?",core.M_NONE))
	
	def test_expects_bottom_left_plus_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"+",core.M_OCCUPIED))
			
	def test_allows_long_height(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  |   |\n")
		feed_input(p,3,0,"  |   |\n")
		feed_input(p,4,0,"  +")
		
	def test_expects_bottom_hyphen(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,3,"+",core.M_NONE))
	
	def test_expects_bottom_hyphen_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,3,"-",core.M_OCCUPIED))
			
	def test_expects_bottom_right_plus(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +---")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"-",core.M_NONE))
			
	def test_expects_bottom_right_plus_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +---")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"+",core.M_OCCUPIED))
			
	def test_allows_rest_of_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +---+")
		p.test(main.CurrentChar(2,7,"a",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,8,"b",core.M_OCCUPIED))
		p.test(main.CurrentChar(2,9,"\n",core.M_OCCUPIED))
		
	def test_allows_final_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +---+\n")
		for i in range(7):
			p.test(main.CurrentChar(3,i,"z",core.M_OCCUPIED))
			
	def test_allows_no_final_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +---+\n")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,0,core.END_OF_INPUT,core.M_NONE))
			
	def test_allows_short_final_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+---+\n")
		feed_input(p,1,0,"  |   |\n")
		feed_input(p,2,0,"  +---+\n")
		feed_input(p,3,0,"    ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(3,4,"\n",core.M_NONE))
	
	def test_allows_h_separator(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |----|\n")
			
	def test_expects_continuation_of_h_separator(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4," ",core.M_NONE))
			
	def test_expects_continuation_of_h_separator_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"-",core.M_OCCUPIED))
			
	def test_allows_non_separator_h_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  | ---|\n")
		
	def test_allows_h_non_separator_start_if_occupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |")
		p.test(main.CurrentChar(2,3,"-",core.M_OCCUPIED))
		feed_input(p,2,4,"---|\n")
	
	def test_doesnt_assume_h_separator_if_first_row(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |--- |\n")
		
	def test_doesnt_assume_h_separator_if_section_too_small(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |----|\n")
		feed_input(p,3,0,"  |--  |\n")
		
	def test_allows_multiple_h_separators(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |----|\n")
		feed_input(p,3,0,"  |    |\n")
		feed_input(p,4,0,"  |----|\n")
	
	def test_allows_v_separator(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |  | |\n")
		feed_input(p,3,0,"  +----+\n")
		
	def test_expects_continuation_of_v_separator(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5," ",core.M_NONE))
			
	def test_expects_continuation_of_v_separator_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"|",core.M_OCCUPIED))
	
	def test_allows_non_separator_v_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |    |\n")
		feed_input(p,2,0,"  |  | |\n")
		feed_input(p,3,0,"  |  | |\n")
		feed_input(p,4,0,"  +----+\n")
	
	def test_allows_v_non_separator_start_if_occupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  ")
		p.test(main.CurrentChar(1,5,"|",core.M_OCCUPIED))
		feed_input(p,1,6," |\n")
	
	def test_allows_multiple_v_separators(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-----+\n")
		feed_input(p,1,0,"  | | | |\n")
		feed_input(p,2,0,"  | | | |\n")
		feed_input(p,3,0,"  +-----+\n")
	
	def test_doesnt_assume_v_separator_if_first_col(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  ||   |\n")
		feed_input(p,2,0,"  ||   |\n")
		feed_input(p,3,0,"  |    |\n")
		
	def test_doesnt_assume_v_separator_if_section_too_small(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-----+\n")
		feed_input(p,1,0,"  |  || |\n")
		feed_input(p,2,0,"  |  || |\n")
		feed_input(p,3,0,"  |  |  |\n")
	
	def test_allows_crossing_separators(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |----|\n")
		feed_input(p,3,0,"  |  | |\n")
		feed_input(p,4,0,"  +----+\n")
		
	def test_expects_line_at_separator_intersection(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |--")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"+",core.M_NONE))
			
	def test_expects_line_at_separator_intersection_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |--")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,5,"-",core.M_OCCUPIED))

	def test_allows_vertical_line_at_separator_intersection(self):
		p = self.pclass()
		feed_input(p,0,2,  "+----+\n")
		feed_input(p,1,0,"  |  | |\n")
		feed_input(p,2,0,"  |--|-|\n")

	def test_allows_single_character_sections(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-----+\n")
		feed_input(p,1,0,"  | | | |\n")
		feed_input(p,2,0,"  |-----|\n")
		feed_input(p,3,0,"  | | | |\n")
		feed_input(p,4,0,"  |-----|\n")
		feed_input(p,5,0,"  | | | |\n")
		feed_input(p,6,0,"  +-----+\n")

	def test_allows_dashed_box(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - - - +\n")
		feed_input(p,1,0,"  ;        ;\n")
		feed_input(p,2,0,"  ;        ;\n")
		feed_input(p,3,0,"  +- - - - +\n")
		feed_input(p,4,0,"            ")
		with self.assertRaises(StopIteration):
			p.test(main.CurrentChar(4,12," ",core.M_NONE))
	
	def test_expects_top_dash_continuation(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,6,"-",core.M_NONE))
			
	def test_expects_top_dash_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,4," ",core.M_OCCUPIED))
	
	def test_top_expects_complete_dashes(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(0,6,"+",core.M_NONE))
	
	def test_expects_dashed_left_side(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,"|",core.M_NONE))
	
	def test_expects_dashed_left_side_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,   "+- - +\n")
		feed_input(p,1,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,2,";",core.M_OCCUPIED))
	
	def test_expects_dashed_right_side(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,7,"|",core.M_NONE))
			
	def test_expects_dashed_right_side_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(1,7,";",core.M_OCCUPIED))
			
	def test_expects_dashed_left_side_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,"|",core.M_NONE))
			
	def test_expects_dashed_left_side_second_line_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,2,";",core.M_OCCUPIED))
			
	def test_expects_dashed_right_side_second_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  ;    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,7,"|",core.M_NONE))
		
	def test_expects_dashed_right_side_second_line_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  ;    ")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,7,";",core.M_OCCUPIED))
			
	def test_expects_dashed_bottom_line(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  +-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4,"-",core.M_NONE))
	
	def test_expects_dashed_bottom_line_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - +\n")
		feed_input(p,1,0,"  ;    ;\n")
		feed_input(p,2,0,"  +-")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,4," ",core.M_OCCUPIED))
	
	def test_expects_dashed_bottom_line_continuation(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - - - +\n")
		feed_input(p,1,0,"  ;        ;\n")
		feed_input(p,2,0,"  +- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6,"-",core.M_NONE))
			
	def test_expects_dashed_bottom_line_continuation_unoccupied(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - - - +\n")
		feed_input(p,1,0,"  ;        ;\n")
		feed_input(p,2,0,"  +- -")
		with self.assertRaises(core.PatternRejected):
			p.test(main.CurrentChar(2,6," ",core.M_OCCUPIED))
	
	def test_dashed_box_allows_separators(self):
		p = self.pclass()
		feed_input(p,0,2,  "+- - - - - - +\n")
		feed_input(p,1,0,"  ;   |    |   ;\n")
		feed_input(p,2,0,"  ;--------|---;\n")
		feed_input(p,3,0,"  ;   |    |   ;\n")
		feed_input(p,4,0,"  +- - - - - - +\n")
	
	def test_sets_correct_meta_flags(self):
		p = self.pclass()
		input = ((2,  "+---+  \n",),
				 (0,"  |+|||  \n",),
				 (0,"  |---|  \n",),
				 (0,"  |-| |  \n",),
				 (0,"  +---+  \n",),
				 (0,"       ",    ),)
		c = core.M_BOX_START_S | core.M_BOX_START_E | core.M_OCCUPIED
		t = core.M_BOX_START_S | core.M_OCCUPIED
		l = core.M_BOX_START_E | core.M_OCCUPIED
		o = core.M_OCCUPIED
		n = core.M_NONE
		r = core.M_BOX_AFTER_E
		b = core.M_BOX_AFTER_S
		outmeta = ((    c,t,t,t,t,r,n,n,),
				   (n,n,l,n,o,n,o,r,n,n,),
				   (n,n,l,o,o,o,o,r,n,n,),
				   (n,n,l,n,o,n,o,r,n,n,),
				   (n,n,l,o,o,o,o,r,n,n,),
				   (n,n,b,b,b,b,b,      ),)
		for j,(startcol,line) in enumerate(input):
			for i,char in enumerate(line):
				m = outmeta[j][i]
				self.assertEquals(m, p.test(main.CurrentChar(j,startcol+i,char,core.M_NONE)))
		 
	def do_render(self,x,y,w,h,hs=[],vs=[],dash=False):
		p = self.pclass()
		feed_input(p,y,x,"+" + (("- "*(w//2)) if dash else ("-"*w)) + "+\n")
		for i in range(h):
			feed_input(p,y+1+i,0," "*x + (";" if dash else "|"))
			for n in range(w):
				chr = { 
					(True,True): "-",
				  	(True,False): "-",
				  	(False,True): "|",
				  	(False,False): " " 
				}[(i in hs,n in vs)]
				feed_input(p,y+1+i,x+1+n, chr)
			feed_input(p,y+1+i,x+1+w, (";" if dash else "|")+"\n")
		feed_input(p,y+1+h+0,0," "*x + "+" + (("- "*(w//2)) if dash else ("-"*w)) + "+\n")
		feed_input(p,y+1+h+1,0," "*x + " " + " "*w + " ")
		try:
			p.test(main.CurrentChar(y+h+2,x+w+2," ",core.M_NONE))
		except StopIteration: pass
		return p.render()
			
	def test_render_returns_correct_shapes(self):
		r = self.do_render(2,3,5,6)
		self.assertEquals(1, len(r))
		self.assertTrue( isinstance(r[0],core.Rectangle) )
		
	def test_render_coordinates(self):
		r = self.do_render(2,3,5,6)[0]
		self.assertEquals((2.5,3.5),r.a)
		self.assertEquals((8.5,10.5),r.b)
		
	def test_render_coordinates_width(self):
		r = self.do_render(2,3,7,6)[0]
		self.assertEquals((2.5,3.5),r.a)
		self.assertEquals((10.5,10.5),r.b)
		
	def test_render_coordinates_height(self):
		r = self.do_render(2,3,5,8)[0]
		self.assertEquals((2.5,3.5),r.a)
		self.assertEquals((8.5,12.5),r.b)
		
	def test_render_coordinates_position(self):
		r = self.do_render(7,5,5,6)[0]
		self.assertEquals((7.5,5.5),r.a)
		self.assertEquals((13.5,12.5),r.b)
	
	def test_render_z(self):
		r = self.do_render(2,3,5,6)[0]
		self.assertEquals(0,r.z)
		
	def test_render_stroke_colour(self):
		r = self.do_render(2,3,5,6)[0]
		self.assertEquals(core.C_FOREGROUND,r.stroke)
		
	def test_render_stroke_width(self):
		r = self.do_render(2,3,5,6)[0]
		self.assertEquals(1,r.w)
		
	def test_render_stroke_style_solid(self):
		r = self.do_render(2,3,6,6,dash=False)[0]
		self.assertEquals(core.STROKE_SOLID,r.stype)
		
	def test_render_stroke_style_dashed(self):
		r = self.do_render(2,3,6,6,dash=True)[0]
		self.assertEquals(core.STROKE_DASHED,r.stype)
		
	def test_render_fill_colour(self):
		r = self.do_render(2,3,5,6)[0]
		self.assertEquals(None,r.fill)
		
	def test_render_h_sections_returns_background_shapes(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		self.assertEquals(4,len(find_type(self,r,core.Rectangle)))
			
	def test_render_h_sections_coordinates(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(b1.a,(3.5,2.5))
		b2 = find_with(self,r,"b",(12.5,7.5))
		self.assertEquals(b2.a,(8.5,2.5))
		b3 = find_with(self,r,"a",(12.5,2.5))
		self.assertEquals(b3.b,(16.5,7.5))
		
	def test_render_h_sections_stroke_colour(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(None,b1.stroke)
		b2 = find_with(self,r,"b",(12.5,7.5))
		self.assertEquals(None,b2.stroke)
		b3 = find_with(self,r,"a",(12.5,2.5))
		self.assertEquals(None,b3.stroke)
		
	def test_render_h_sections_fill_colour(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b1.fill)
		b2 = find_with(self,r,"b",(12.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b2.fill)
		b3 = find_with(self,r,"a",(12.5,2.5))
		self.assertEquals(core.C_FOREGROUND,b3.fill)
		
	def test_render_h_sections_fill_alpha(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(0.25,b1.falpha)
		b2 = find_with(self,r,"b",(12.5,7.5))
		self.assertEquals(0.0,b2.falpha)
		b3 = find_with(self,r,"a",(12.5,2.5))
		self.assertEquals(0.25,b3.falpha)
		
	def test_render_h_sections_z(self):
		r = self.do_render(3,2,12,4,[],[4,8])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(-0.5,b1.z)
		b2 = find_with(self,r,"b",(12.5,7.5))
		self.assertEquals(-0.5,b2.z)
		b3 = find_with(self,r,"a",(12.5,2.5))
		self.assertEquals(-0.5,b3.z)
	
	def test_render_v_sections_returns_correct_shapes(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		self.assertEquals(4,len(find_type(self,r,core.Rectangle)))
		
	def test_render_v_sections_coordinates(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(b1.a,(3.5,2.5))
		b2 = find_with(self,r,"b",(8.5,11.5))
		self.assertEquals(b2.a,(3.5,7.5))
		b3 = find_with(self,r,"a",(3.5,11.5))
		self.assertEquals(b3.b,(8.5,15.5))
		
	def test_render_v_sections_stroke_colour(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(b1.stroke,None)
		b2 = find_with(self,r,"b",(8.5,11.5))
		self.assertEquals(b2.stroke,None)
		b3 = find_with(self,r,"a",(3.5,11.5))
		self.assertEquals(b3.stroke,None)
		
	def test_render_v_sections_fill_colour(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(b1.fill,core.C_FOREGROUND)
		b2 = find_with(self,r,"b",(8.5,11.5))
		self.assertEquals(b2.fill,core.C_FOREGROUND)
		b3 = find_with(self,r,"a",(3.5,11.5))
		self.assertEquals(b3.fill,core.C_FOREGROUND)
			
	def test_render_v_sections_fill_alpha(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(b1.falpha,0.25)
		b2 = find_with(self,r,"b",(8.5,11.5))
		self.assertEquals(b2.falpha,0.0)
		b3 = find_with(self,r,"a",(3.5,11.5))
		self.assertEquals(b3.falpha,0.25)
		
	def test_render_v_sections_z(self):
		r = self.do_render(3,2,4,12,[4,8],[])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(-0.5,b1.z)
		b2 = find_with(self,r,"b",(8.5,11.5))
		self.assertEquals(-0.5,b2.z)
		b3 = find_with(self,r,"a",(3.5,11.5))
		self.assertEquals(-0.5,b3.z)
			
	def test_render_hv_sections_returns_correct_shapes(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		self.assertEquals(10,len(find_type(self,r,core.Rectangle)))
		
	def test_render_hv_sections_coordinates(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(b1.a,(3.5,2.5))
		b2 = find_with(self,r,"b",(8.5,11.5))
		self.assertEquals(b2.a,(3.5,7.5))
		b3 = find_with(self,r,"a",(3.5,11.5))
		self.assertEquals(b3.b,(8.5,16.5))
		b4 = find_with(self,r,"b",(12.5,7.5))
		self.assertEquals(b4.a,(8.5,2.5))
		b5 = find_with(self,r,"b",(12.5,11.5))
		self.assertEquals(b5.a,(8.5,7.5))
		b6 = find_with(self,r,"a",(8.5,11.5))
		self.assertEquals(b6.b,(12.5,16.5))		
		b7 = find_with(self,r,"b",(16.5,7.5))
		self.assertEquals(b7.a,(12.5,2.5))
		b8 = find_with(self,r,"b",(16.5,11.5))
		self.assertEquals(b8.a,(12.5,7.5))
		b9 = find_with(self,r,"a",(12.5,11.5))
		self.assertEquals(b9.b,(16.5,16.5))
			
	def test_render_hv_sections_stroke_colour(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(None,b1.stroke)
		b2 = find_with(self,r,"b",(8.5,11.5))
		self.assertEquals(None,b2.stroke)
		b3 = find_with(self,r,"a",(3.5,11.5))
		self.assertEquals(None,b3.stroke)
		b4 = find_with(self,r,"b",(12.5,7.5))
		self.assertEquals(None,b4.stroke)
		b5 = find_with(self,r,"b",(12.5,11.5))
		self.assertEquals(None,b5.stroke)
		b6 = find_with(self,r,"a",(8.5,11.5))
		self.assertEquals(None,b6.stroke)		
		b7 = find_with(self,r,"b",(16.5,7.5))
		self.assertEquals(None,b7.stroke)
		b8 = find_with(self,r,"b",(16.5,11.5))
		self.assertEquals(None,b8.stroke)
		b9 = find_with(self,r,"a",(12.5,11.5))
		self.assertEquals(None,b9.stroke)
			
	def test_render_hv_sections_fill_colour(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b1.fill)
		b2 = find_with(self,r,"b",(8.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b2.fill)
		b3 = find_with(self,r,"a",(3.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b3.fill)
		b4 = find_with(self,r,"b",(12.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b4.fill)
		b5 = find_with(self,r,"b",(12.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b5.fill)
		b6 = find_with(self,r,"a",(8.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b6.fill)		
		b7 = find_with(self,r,"b",(16.5,7.5))
		self.assertEquals(core.C_FOREGROUND,b7.fill)
		b8 = find_with(self,r,"b",(16.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b8.fill)
		b9 = find_with(self,r,"a",(12.5,11.5))
		self.assertEquals(core.C_FOREGROUND,b9.fill)
			
	def test_render_hv_sections_fill_alpha(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(0.25,b1.falpha)
		b2 = find_with(self,r,"b",(8.5,11.5))
		self.assertEquals(0.125,b2.falpha)
		b3 = find_with(self,r,"a",(3.5,11.5))
		self.assertEquals(0.25,b3.falpha)
		b4 = find_with(self,r,"b",(12.5,7.5))
		self.assertEquals(0.125,b4.falpha)
		b5 = find_with(self,r,"b",(12.5,11.5))
		self.assertEquals(0.0,b5.falpha)
		b6 = find_with(self,r,"a",(8.5,11.5))
		self.assertEquals(0.125,b6.falpha)		
		b7 = find_with(self,r,"b",(16.5,7.5))
		self.assertEquals(0.25,b7.falpha)
		b8 = find_with(self,r,"b",(16.5,11.5))
		self.assertEquals(0.125,b8.falpha)
		b9 = find_with(self,r,"a",(12.5,11.5))
		self.assertEquals(0.25,b9.falpha)
		
	def test_render_hv_sections_z(self):
		r = self.do_render(3,2,12,13,[4,8],[4,8])
		b1 = find_with(self,r,"b",(8.5,7.5))
		self.assertEquals(-0.5,b1.z)
		b2 = find_with(self,r,"b",(8.5,11.5))
		self.assertEquals(-0.5,b2.z)
		b3 = find_with(self,r,"a",(3.5,11.5))
		self.assertEquals(-0.5,b3.z)
		b4 = find_with(self,r,"b",(12.5,7.5))
		self.assertEquals(-0.5,b4.z)
		b5 = find_with(self,r,"b",(12.5,11.5))
		self.assertEquals(-0.5,b5.z)
		b6 = find_with(self,r,"a",(8.5,11.5))
		self.assertEquals(-0.5,b6.z)		
		b7 = find_with(self,r,"b",(16.5,7.5))
		self.assertEquals(-0.5,b7.z)
		b8 = find_with(self,r,"b",(16.5,11.5))
		self.assertEquals(-0.5,b8.z)
		b9 = find_with(self,r,"a",(12.5,11.5))
		self.assertEquals(-0.5,b9.z)


if __name__ == "__main__":
	unittest.main()
