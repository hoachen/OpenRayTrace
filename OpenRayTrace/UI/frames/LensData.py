from __future__ import division
#OpenRayTrace.UI.frames.LensData
##    OpenRayTrace: Free optical design software
##    Copyright (C) 2004 Andrew Wilson
##
##    This file is part of OpenRayTrace.

##

##    OpenRayTrace is free software; you can redistribute it and/or modify

##    it under the terms of the GNU General Public License as published by

##    the Free Software Foundation; either version 2 of the License, or

##    (at your option) any later version.

##

##    OpenRayTrace is distributed in the hope that it will be useful,

##    but WITHOUT ANY WARRANTY; without even the implied warranty of

##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

##    GNU General Public License for more details.

##

##    You should have received a copy of the GNU General Public License

##    along with OpenRayTrace; if not, write to the Free Software

##    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA




import wx
import wx.grid
from wx.grid import *
from OpenRayTrace.UI import Dialog_wavelengths

from OpenRayTrace.UI.myCanvas import *
from OpenRayTrace.ray_trace import *
from OpenRayTrace import DataModel

import os, string
from cmath import *
import math
import numpy as np
from numpy.linalg import norm


WIDTH=640.0
HEIGHT=480.0

class LensData(wx.MDIChildFrame):
    wxID = wx.NewId()
    col_labels = ('surf type','comment','radius','thickness','aperature radius','glass')
    @property 
    def RADIUS_COL(self): return self.col_labels.index('radius')
    @property 
    def THICKNESS_COL(self): return self.col_labels.index('thickness')
    @property 
    def APERATURE_RADIUS_COL(self): return self.col_labels.index('aperature radius')
    @property 
    def GLASS_COL(self): return self.col_labels.index('aperature radius')
    MENU_GLASSBK7 = wx.NewId()
    MENU_GLASSDIRECT = wx.NewId()
    MENU_THICKNESSPARAXIALFOCUS = wx.NewId()

    [wxID_BUTTON_COMPUTE_ALL, 
     wxID_BUTTON_IMAGE, 
     wxID_BUTTON_SPOT_DIAGRAMS, 
     wxID_BUTTON_WAVE_LENGTHS, 
     wxID_CHECKBOX_AUTOFOCUS, 
     wxID_GRID1, 
     wxID_RADIOBUTTON_CONST_POWER, 
     wxID_RADIOBUTTON_CONST_RADIUS, 
     wxID_STATICBOX1, 
     wxID_STATICTEXT1, 
     wxID_STATICTEXT_EFL, 
     wxID_STATICTEXT_MAG, 
     wxID_STATICTEXT_MG, 
     wxID_STATICTEXT_OBJ_HEIGHT, 
     wxID_STATICTEXT_PARAXIAL_FOCUS, 
     wxID_TEXTCTRL_OBJECT_HEIGHT, 
    ] = [wx.NewId() for _ in range(16)]



    wxID_MENU_GLASSITEMS_BK7 = wx.NewId()
    wxID_MENU_GLASSITEMS_DIRECT = wx.NewId()

    [wxID_MENU1COPY, 
     wxID_MENU1DELETE, 
     wxID_MENU1INSERT_AFTER, 
     wxID_MENU1INSERT_BEFORE, 
     wxID_MENU1PASTE, 
    ] = [wx.NewId() for _ in range(5)]

    wxID_MENU_THICKNESSITEMS0 = wx.NewId()

    [wxID_BUTTON_COMPUTE_ALL, 
     wxID_BUTTON_IMAGE, 
     wxID_BUTTON_SPOT_DIAGRAMS, 
     wxID_BUTTON_WAVE_LENGTHS, 
     wxID_CHECKBOX_AUTOFOCUS, 
     wxID_GRID1, 
     wxID_RADIOBUTTON_CONST_POWER, 
     wxID_RADIOBUTTON_CONST_RADIUS, 
     wxID_STATICBOX1, 
     wxID_STATICTEXTEFFECTIVEFOCALLENGTH, 
     wxID_STATICTEXT_EFL, 
     wxID_STATICTEXT_MAG, 
     wxID_STATICTEXT_MG, 
     wxID_STATICTEXT_OBJ_HEIGHT, 
     wxID_STATICTEXT_PARAXIAL_FOCUS, 
     wxID_TEXTCTRL_OBJECT_HEIGHT, 
    ] = [wx.NewId() for _ in range(16)]


    [DATAROW_MENUCOPY, 
     DATAROW_MENUDELETE, 
     DATAROW_MENUINSERTAFTER, 
     DATAROW_MENUINSERTBEFORE, 
     DATAROW_MENU_SET_AS_STOP,
     DATAROW_MENUPASTE] = [wx.NewId() for _ in range(6)]

    @staticmethod
    def surfToRowData(surf):
        """Given a DataModel.Surface, return the row of values as a dictionary."""
        getter = {'surf type': lambda s: s.__class__.__name__.replace('Surface',''),
                  'comment': lambda s: None,
                  'radius': lambda s: s.R if hasattr(s, 'R') else np.inf,
                  'thickness': lambda s: s.thickness,
                  'aperature radius': lambda s: s.semidiam,
                  'glass': lambda s: s.n(None)}
        return dict((label, getter[label](surf)) for label in LensData.col_labels)
            
    def _init_coll_boxSizerBottom_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.grid1, 1, border=0, flag=0)

    def _init_coll_staticBoxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.gridBagSizerComputations, 0, border=0, flag=0)

    def _init_coll_flexGridSizerLensDataMain_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizertop, 0, border=0, flag=0)
        parent.AddSizer(self.boxSizerBottom, 0, border=0, flag=0)

    def _init_coll_flexGridSizerLensDataMain_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(1)
        parent.AddGrowableCol(0)

    def _init_coll_gridBagSizerTop_Items(self, parent):
        # generated method, don't edit
        parent.AddWindow(self.radioButton_const_power, (0, 0), border=0, flag=0,span=(1, 1))
        parent.AddWindow(self.radioButton_const_radius, (1, 0), border=0,flag=0, span=(1, 1))
        parent.AddWindow(self.checkBox_autofocus, (2, 0), border=0, flag=0,span=(1, 1))
        parent.AddWindow(self.staticText_obj_height, (0, 1), border=0, flag=0,span=(1, 1))
        parent.AddWindow(self.textCtrl_object_height, (1, 1), border=0, flag=0,span=(1, 1))
        parent.AddWindow(self.button_wave_lengths, (2, 1), border=0, flag=0,span=(1, 1))
        parent.AddSizer(self.staticBoxSizer1, (0, 2), border=0, flag=0, span=(3,1))
        parent.AddWindow(self.staticText_efl, (2, 8), border=0, flag=0, span=(1,1))
        parent.AddWindow(self.staticText_mg, (1, 7), border=0, flag=0, span=(1,1))
        parent.AddWindow(self.staticText_mag, (1, 8), border=0, flag=0, span=(1,1))
        parent.AddWindow(self.staticTextEffectiveFocalLength, (2, 7), border=0,flag=0, span=(1, 1))
        parent.AddWindow(self.staticText_paraxial_focus, (3, 7), border=0,flag=0, span=(1, 1))
                         

    def _init_coll_boxSizertop_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.gridBagSizerTop, 0, border=0, flag=0)

    def _init_coll_gridBagSizerComputations_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.button_spot_diagrams, (0, 0), border=0, flag=0,
              span=(1, 1))
        parent.AddWindow(self.button_image, (1, 0), border=0, flag=0, span=(1,
              1))
        parent.AddWindow(self.button_compute_all, (0, 1), border=0, flag=0,
              span=(1, 1))

    def _init_coll_row_menu_Items(self, parent):
        for ID, text in [(self.DATAROW_MENU_SET_AS_STOP, 'Set as system stop'),
                         (self.DATAROW_MENUINSERTBEFORE, 'Insert Before'),
                         (self.DATAROW_MENUINSERTAFTER,  'Insert After'),
                         (self.DATAROW_MENUDELETE,       'Delete'),
                         (self.DATAROW_MENUCOPY,         'Copy'),
                         (self.DATAROW_MENUPASTE,        'Paste')]:
            parent.Append(id=ID, text=text, kind=wx.ITEM_NORMAL, help='')
            self.Bind(id=ID, event=wx.EVT_MENU, handler=self.OnRow_menuitems0Menu)

    def _init_coll_menu_glass_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='',
                      id=self.MENU_GLASSDIRECT,
                      kind=wx.ITEM_NORMAL, text='Direct')
        parent.Append(help='', id=self.MENU_GLASSBK7,
                      kind=wx.ITEM_NORMAL, text='BK7')
        self.Bind(wx.EVT_MENU, self.OnMenu_glassitems0Menu,
                  id=self.MENU_GLASSDIRECT)
        self.Bind(wx.EVT_MENU, self.OnMenu_glassitems0Menu,
                  id=self.MENU_GLASSBK7)

    def _init_coll_menu_thickness_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='',
              id=self.MENU_THICKNESSPARAXIALFOCUS,
              kind=wx.ITEM_NORMAL, text='Paraxial Focus')
        self.Bind(wx.EVT_MENU, self.OnMenu_thicknessitems0Menu,
              id=self.MENU_THICKNESSPARAXIALFOCUS)

    def _init_sizers(self):
        # generated method, don't edit
        self.flexGridSizerLensDataMain = wx.FlexGridSizer(cols=0, hgap=0,
              rows=2, vgap=0)

        self.boxSizertop = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerBottom = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.gridBagSizerTop = wx.GridBagSizer(hgap=0, vgap=0)

        self.staticBoxSizer1 = wx.StaticBoxSizer(box=self.staticBox1,
              orient=wx.VERTICAL)

        self.gridBagSizerComputations = wx.GridBagSizer(hgap=0, vgap=0)

        self._init_coll_flexGridSizerLensDataMain_Items(self.flexGridSizerLensDataMain)
        self._init_coll_flexGridSizerLensDataMain_Growables(self.flexGridSizerLensDataMain)
        self._init_coll_boxSizertop_Items(self.boxSizertop)
        self._init_coll_boxSizerBottom_Items(self.boxSizerBottom)
        self._init_coll_gridBagSizerTop_Items(self.gridBagSizerTop)
        self._init_coll_staticBoxSizer1_Items(self.staticBoxSizer1)
        self._init_coll_gridBagSizerComputations_Items(self.gridBagSizerComputations)

        self.SetSizer(self.flexGridSizerLensDataMain)

    def _init_utils(self):
        # generated method, don't edit
        self.menu_thickness = wx.Menu(title='')

        self.menu_glass = wx.Menu(title='')

        self.row_menu = wx.Menu(title='')

        self._init_coll_menu_thickness_Items(self.menu_thickness)
        self._init_coll_menu_glass_Items(self.menu_glass)
        self._init_coll_row_menu_Items(self.row_menu)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=self.wxID,
                                  name='LensData', parent=prnt, pos=wx.Point(505,364), 
                                  size=wx.Size(847, 373), style=wx.DEFAULT_FRAME_STYLE,
              
              title='Lens Data')
        self._init_utils()
        self.SetClientSize(wx.Size(839, 339))
        self.Bind(EVT_CLOSE, lambda event: self.Hide)

        self.grid1 = wx.grid.Grid(id=self.wxID_GRID1,
              name='grid1', parent=self, pos=wx.Point(0, 87), size=wx.Size(839,
              773), style=0)
        self.grid1.Bind(EVT_GRID_CELL_CHANGE, self.OnGrid1GridCellChange)
        self.grid1.Bind(EVT_GRID_SELECT_CELL, self.OnGrid1GridCellChange) # To allow highlighting the active row.
        self.grid1.Bind(EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGrid1GridCellRightClick)
        self.grid1.Bind(EVT_GRID_LABEL_RIGHT_CLICK,
              self.OnGrid1GridLabelRightClick)

        self.radioButton_const_power = wx.RadioButton(id=self.wxID_RADIOBUTTON_CONST_POWER,
              label='Const Power/F-length', name='radioButton_const_power',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(136, 13), style=0)
        self.radioButton_const_power.SetValue(True)
        self.radioButton_const_power.Bind(EVT_RADIOBUTTON,
              self.OnRadiobutton_const_powerRadiobutton)

        self.radioButton_const_radius = wx.RadioButton(id=self.wxID_RADIOBUTTON_CONST_RADIUS,
              label='Const Radius', name='radioButton_const_radius',
              parent=self, pos=wx.Point(0, 22), size=wx.Size(79, 13), style=0)
        self.radioButton_const_radius.SetValue(False)
        self.radioButton_const_radius.Bind(EVT_RADIOBUTTON,
              self.OnRadiobutton_const_radiusRadiobutton)

        self.staticText_paraxial_focus = wx.StaticText(id=self.wxID_STATICTEXT_PARAXIAL_FOCUS,
              label='', name='staticText_paraxial_focus', parent=self,
              pos=wx.Point(436, 67), size=wx.Size(0, 13), style=0)

        self.checkBox_autofocus = wx.CheckBox(id=self.wxID_CHECKBOX_AUTOFOCUS,
              label='Autofocus (paraxial)', name='checkBox_autofocus',
              parent=self, pos=wx.Point(0, 44), size=wx.Size(120, 13), style=0)
        self.checkBox_autofocus.SetValue(False)

        self.textCtrl_object_height = wx.TextCtrl(id=self.wxID_TEXTCTRL_OBJECT_HEIGHT,
              name='textCtrl_object_height', parent=self, pos=wx.Point(136, 22),
              size=wx.Size(100, 21),
              style=wx.TAB_TRAVERSAL | wx.TE_PROCESS_TAB | wx.TE_PROCESS_ENTER,
              value='1.0')
        self.textCtrl_object_height.Enable(True)
        self.textCtrl_object_height.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL,
              wx.NORMAL, False, 'MS Shell Dlg'))
        self.textCtrl_object_height.Bind(EVT_TEXT,
              self.OnTextctrl_object_heightText)

        self.button_compute_all = wx.Button(id=self.wxID_BUTTON_COMPUTE_ALL,
              label='Compute All', name='button_compute_all', parent=self,
              pos=wx.Point(316, 17), size=wx.Size(75, 23), style=0)
        self.button_compute_all.Bind(EVT_BUTTON,
              self.OnButton_compute_allButton)

        self.staticText_obj_height = wx.StaticText(id=self.wxID_STATICTEXT_OBJ_HEIGHT,
              label='Object Height', name='staticText_obj_height', parent=self,
              pos=wx.Point(136, 0), size=wx.Size(65, 13), style=0)

        self.button_wave_lengths = wx.Button(id=self.wxID_BUTTON_WAVE_LENGTHS,
              label='Wave Lengths', name='button_wave_lengths', parent=self,
              pos=wx.Point(136, 44), size=wx.Size(88, 23), style=0)
        self.button_wave_lengths.Bind(EVT_BUTTON,
              self.OnButton_wave_lengthsButton)

        self.button_spot_diagrams = wx.Button(id=self.wxID_BUTTON_SPOT_DIAGRAMS,
              label='Spot Diagram', name='button_spot_diagrams', parent=self,
              pos=wx.Point(241, 17), size=wx.Size(75, 23), style=0)
        self.button_spot_diagrams.Bind(EVT_BUTTON,
              self.OnButton_spot_diagramsButton)

        self.staticBox1 = wx.StaticBox(id=self.wxID_STATICBOX1,
              label='Computations', name='staticBox1', parent=self,
              pos=wx.Point(236, 0), size=wx.Size(160, 68), style=0)

        self.button_image = wx.Button(id=self.wxID_BUTTON_IMAGE,
              label='Image', name='button_image', parent=self, pos=wx.Point(241,
              40), size=wx.Size(75, 23), style=0)
        self.button_image.Bind(EVT_BUTTON, self.OnButton_imageButton)

        self.staticText_mg = wx.StaticText(id=self.wxID_STATICTEXT_MG,
              label='Transverse Magnification', name='staticText_mg',
              parent=self, pos=wx.Point(436, 22), size=wx.Size(160, 13),
              style=0)

        self.staticText_mag = wx.StaticText(id=self.wxID_STATICTEXT_MAG,
              label='', name='staticText_mag', parent=self, pos=wx.Point(596,
              22), size=wx.Size(0, 13), style=0)

        self.staticTextEffectiveFocalLength = wx.StaticText(id=self.wxID_STATICTEXTEFFECTIVEFOCALLENGTH,
              label='EFL:', name='staticTextEffectiveFocalLength', parent=self,
              pos=wx.Point(436, 44), size=wx.Size(22, 13), style=0)

        self.staticText_efl = wx.StaticText(id=self.wxID_STATICTEXT_EFL,
              label='', name='staticText_efl', parent=self, pos=wx.Point(596,
              44), size=wx.Size(0, 13), style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.waves = Dialog_wavelengths.Dialog_wavelengths(self)
        stopSurface = DataModel.StandardSurface(thickness=0.0,R=np.inf,semidiam=1.0)
        self.__system = DataModel.System([DataModel.StandardSurface(thickness=np.inf,R=np.inf),
                                          stopSurface,
                                          DataModel.StandardSurface(thickness=0,R=np.inf)], 
                                         apertureStop = stopSurface,
                                         ndim=3)
        self.grid1.CreateGrid(max(1,self.rows), self.cols)       

        for i, label in enumerate(self.col_labels):
            self.grid1.SetColLabelValue(i, label)
        self.grid1.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        self.grid1.AutoSize()
                

        for row in range(self.rows):
            for col in range(self.cols):
                self.grid1.SetCellEditor(row, col, apply(GridCellFloatEditor, []))

        #self.n = []
        #self.c = []
        #self.t = []
        #self.c_unbent = [0 for i in range(self.rows)]                
            
        self.hold_power = self.radioButton_const_power.GetValue()        
        self.hold_radius = self.radioButton_const_radius.GetValue()        

        self.Layout()
        self.Centre()
        self.rays = 100
        self._sync_grid_to_system()
        
        
    @property
    def object_height(self):
        return float(self.textCtrl_object_height.GetValue())

    @property
    def rows(self): return len(self.__system)
    @property
    def cols(self): return len(self.col_labels)
    
    def setSystem(self, system):
        if system is not self.__system:
            self.__system = system
            self._sync_grid_to_system()
            self.OnGrid1GridCellChange()

    def OnWxframeopenmodalSize(self, event):
        event.Skip()
    
    def OnRadiobutton_const_powerRadiobutton(self, event=None):
        self.hold_power = True
        self.hold_radius = False
 #       event.Skip()

    def OnRadiobutton_const_radiusRadiobutton(self, event=None):
        self.hold_power = False
        self.hold_radius = True
    

    def OnGrid1GridCellChange(self, event=None,r=None,c=None):  
        ##        self.grid1.AutoSize()
        if event is not None:
            r = event.GetRow()
            c = event.GetCol() 
        
        val = None
        if r is not None and c is not None:
            val = self.grid1.GetCellValue(r,c)
        
        if val == '':
            return
        if val is not None:
            rowData = self.surfToRowData(self.__system.surfaces[r])
            if str(rowData[self.col_labels[c]]) != val:
                val = float(val)                 
                draw = self.fill_in_values(r,c,val)
        self.update_display(event)

        #compute paraxial focus
        y = 0.0
        u = 1.0
        if np.isfinite(self.t[0]):
            l, y, u = paraxial_ray(y,u,self.t,self.n,self.c)
        else:
            l, y, u = paraxial_ray(y,u,self.t[1:],self.n[1:],self.c[1:])
        #print u
        mag = u[0] / u[-1]
        print 'paraixal ray:'
        print l
        print y
        print u
        print 'mag',mag

        self.staticText_mag.SetLabel(str(mag))
        if self.checkBox_autofocus.GetValue():
            self.grid1.SetCellValue(len(self.t)-1,self.THICKNESS_COL,str(l))
            draw = self.fill_in_values(len(self.t)-1,self.THICKNESS_COL,l)            
            self.update_display()                            

        print 'stop at', self.__system.surfaces.index(self.__system.apertureStop)
        x   = [None] * self.rays
        y   = [None] * self.rays
        z   = [None] * self.rays
        X   = [None] * self.rays
        Y   = [None] * self.rays
        Z   = [None] * self.rays
        cnt = 0

        surf_i = 0
        for surf_i in range(len(self.t)): # Make surf_i index the first surface with finite thickness. 
            if np.isfinite(self.t[surf_i]): break

        if len(self.t) > 1:
            # Loop over field points:
            eppos, epsemidiam = self.__system.paraxialEPPosAndSemidiam()
            epslope = epsemidiam / eppos
            epCtr   = np.array([0,  0, eppos])
            topEdge = np.array([0,  epsemidiam, eppos])
            botEdge = np.array([0, -epsemidiam, eppos])
            normalized = lambda v: v / norm(v)

            for fp_i, objPt, color in [(10, (0,0,0), (0.8,0.2,0.2)),
                                       (10, (0,self.object_height,0), (0.2,0.8,0.2))]:
                pupilPts = np.array([topEdge * alpha + botEdge * (1-alpha)
                                     for alpha in np.linspace(0, 1, fp_i)])
                #for i in range(-fp_i//2+1, fp_i//2):
                if surf_i == 0:
                    raydirs = [normalized(target - objPt) for target in pupilPts]
                    offsets = np.zeros((len(raydirs),3))
                else:
                    # Object at -infinity => columnated rays
                    raydirs = [normalized(epCtr - objPt)] * fp_i
                    offsets = pupilPts - epCtr
                
                rays = DataModel.Rays(np.transpose([objPt+offset for offset in offsets]),
                                      np.transpose([direction for direction in raydirs]))
                traces, outbound = self.__system[surf_i:].cast(rays)
                for i, (offset, direction) in enumerate(zip(offsets,
                                                          raydirs)):
                    #go to aperature radius
                    # It looks like it is trying to aim the outermost ray at the clear aperature of the next surface:
                    #direction = [None, (i/(fp_i/2.0)) * self.h[surf_i+1] / norm([self.h[surf_i+1], self.t[surf_i]]), 0.0]
                    #direction[0] = np.sqrt(1.0 - direction[1]**2 - direction[2]**2)
                    #print "direction {}: {} -> {}".format(i, objPt + offset, direction)
                    
                    #rays = DataModel.Rays((objPt+offset)[:,None], direction[:,None]);
                    #traces, outbound = self.__system[surf_i:].cast(rays)
                    z[i], y[i], x[i] = traces[:,:,i].T
                    cnt+=1
                    self.GetParent().ogl.draw_ray(x[i],y[i],z[i],cnt, color=color)

            if not len(self.t_cum) or self.t_cum[-1] == 0: 
                k = 1
            else:
                k = self.t_cum[-1] # Cumulative thickness.
            self.GetParent().ogl.K = k

            ##                #calc third order aberrations
            ##            
            #we need data from axial ray 
            #calc efL

            (l,y,u)    = paraxial_ray2(self.h[surf_i+1], 0.0,self.t,self.n,self.c)
            (lp,yp,up) = paraxial_ray2(0.0, 0.1,self.t,self.n,self.c)
            num = (y[surf_i]*up[surf_i] - u[surf_i]*yp[surf_i])
            den = (u[surf_i]*up[-1] - up[0]*u[-1])                
            if (den != 0):
                efl = num/den
                self.staticText_efl.SetLabel(str(efl))



                ##                #(l,y,u) = self.paraxial_ray2(18.5, 0)
                ##                #print y,u
                ##            
                ##                if(len(y) > 1):
                ##                    #data from a principal ray
                ##                    (lp,yp,up) = paraxial_ray2(0.0, 0.1,self.t,self.n,self.c)
                ##                    #(lp,yp,up) = self.paraxial_ray2(-6.3, 0.25)
                ##                    #print yp,up
                ##                    self.GetParent().trace.calc_third_order_abberations(y,u,yp,up,self.n,self.c)
                #self.GetParent().abr.calc_abr(self.t,self.n,self.c,self.t_cum,self.h,self.object_height)
                
        
    
    def fill_in_values(self,r,c,val):                               
        #AUTOFILL SOME STUFF
        autofills = {self.THICKNESS_COL: '0',
                     self.RADIUS_COL: '0',
                     self.APERATURE_RADIUS_COL: '1.0'}
        for col, default in autofills.iteritems():
            if self.grid1.GetCellValue(r, col) == '':
                self.grid1.SetCellValue(r, col, default)


        self._sync_system_to_grid(r, c, val)
        self._sync_grid_to_system(r, c)

        return True

    def update_display(self, event=None):
        print 'update_display',event
        thickness = 0                
        
        self.t = []
        self.t_cum = None
        self.c = []
        self.n = []
        self.h = []
        surf_i = []
        stop_index = None
            
        t1 = 0
        colors = [self.GetParent().ogl._lensSurfaceColor] * self.rows
        row = self.grid1.GetGridCursorRow()
        if event is not None:
            row = event.GetRow()
            #print "Row:", row, event.GetRow()
            if row is not None and row < self.rows:
                colors[row] = (1.0,0.0,0.0)
        for i, surf in enumerate(self.__system):                        
            if (surf.thickness is not None or
                surf.semidiam is not None):
                
                #if not np.isfinite(float(thickness)): continue # Skip object or image at infinity.
        
                self.c.append(float(1/surf.R))
                self.h.append(float(surf.semidiam))
                surf_i.append(i)
                self.n.append(surf.n(None))
                
                t1 += float(surf.thickness)
                self.t.append(float(surf.thickness))
                if surf is self.__system.apertureStop:
                    stop_index = i
        # We want t_cum to be the positions of each surface. Need to deel with infinate thicknesses at ends of the system.
        if len(self.t) == 0 or np.isfinite(self.t[0]):
            self.t_cum = np.hstack([[0], np.cumsum(self.t)])
        else:
            self.t_cum = np.hstack([[-np.inf, 0], np.cumsum(self.t[1:])])
            
        l = range(1,self.rows)
        self.GetParent().ogl.draw_lenses(self.t,surf_i,self.t_cum,self.c,self.n,self.h,colors=colors,
                                         stop_index=stop_index)

    def get_data(self):
        t = []
        tble = self.grid1.GetTable()                     
        for r in range(self.rows):
            t.append([tble.GetValue(r,c) for c in range(len(self.col_labels))])
        
        return t
        

    def set_data(self, data):
        self._sync_grid_to_system()
        for ri, row in enumerate(data):
            for ci, cell in enumerate(row):
                strval = str(cell) if cell is not None else ''
                self.grid1.SetCellValue(ri, ci, strval)

    def _sync_grid_to_system(self, row=None, col=None):
        newNumRows = max(1, self.rows)
        if self.grid1.GetNumberRows() < newNumRows:
            self.grid1.InsertRows(self.grid1.GetNumberRows(), newNumRows - self.grid1.GetNumberRows())
        rowIndsSurfaces = (enumerate(self.__system) if row is None 
                           else [(row, self.__system.surfaces[row])])
        for ri, surface in rowIndsSurfaces:
            rowData = self.surfToRowData(surface)
            if surface is self.__system.apertureStop:
                self.grid1.SetRowLabelValue(ri, '[{}]'.format(ri+1))
            else:
                self.grid1.SetRowLabelValue(ri, '{}'.format(ri+1))
            color = '#FFFFFF' if surface.n(None) == 1.0 else '#d7e6ec' # Default to white; glass gets light blue.
            for ci, col_label in enumerate(self.col_labels):
                cell = rowData[col_label]
                strval = str(cell) if cell is not None else ''
                if col_label == 'thickness':
                    if surface is self.__system.surfaces[-1]:
                        strval = '-'
                elif col_label == 'glass':
                    if strval == '1.0':
                        strval = '' # Don't bother writing the 1.0 for air.
                self.grid1.SetCellValue(ri, ci, strval)
                self.grid1.SetCellBackgroundColour(ri, ci, color)

    def _sync_system_to_grid(self, r, c=None, val=None):
        """Sync the given entry to the system model."""
        if c is None:
            if val is not None: raise TypeError('val must be unspecified if c is.')
            for c, label in enumerate(col_labels):
                if label in ('radius', 'thickness', 'aperature radius', 'glass'):
                    self._sync_system_to_grid(r, c)
            return

        if val is None:
            val = self.grid1.GetValue(r, c)

        surface = self.__system.surfaces[r]
        label = self.col_labels[c]
        if label == 'radius': surface.R = val
        elif label == 'thickness': surface.thickness = val
        elif label == 'aperature radius': surface.semidiam = val
        elif label == 'glass': surface.glass = DataModel.SimpleGlass(val)
        else:
            print "Unimplemented."
            
    def clear_data(self):       
        for r in range(self.rows):
            [self.grid1.SetCellValue(r,c,'') for c in range(len(self.col_labels))]

    def OnGrid1GridCellRightClick(self, event):
        r = event.GetRow()
        c = event.GetCol()
        self.grid1.SelectBlock(r,c,r,c)
        self.grid1.SetGridCursor(r,c)
        
        offset =  self.grid1.GetPosition()
        pos    =  event.GetPosition()
        pos.x += offset.x
        pos.y += offset.y
        
        if c == self.THICKNESS_COL:
            self.PopupMenu(self.menu_thickness,pos)
        elif c == self.GLASS_COL:
            id = self.PopupMenu(self.menu_glass,pos)
        
        event.Skip()

    def OnGrid1GridLabelRightClick(self, event):
        r = event.GetRow()
        c = event.GetCol()
        
        self.grid1.SetGridCursor(r,0)
        offset = self.grid1.GetPosition()
        pos    = event.GetPosition()
        pos.x += offset.x - 80
        pos.y += offset.y
                        
        self.PopupMenu(self.row_menu,pos)
        event.Skip()

    def OnRow_menuitems0Menu(self, event):
        r, c = self.grid1.GetGridCursorRow(), self.grid1.GetGridCursorCol()
        id = event.GetId()
        
        if id == self.DATAROW_MENU_SET_AS_STOP:
            self.__system.apertureStop = self.__system.surfaces[r]
            self._sync_grid_to_system()
            self.OnGrid1GridCellChange()
        elif id == self.DATAROW_MENUINSERTAFTER:
            self.grid1.InsertRows(r+1)
            self.__system.insert_surface(r+1, DataModel.StandardSurface(thickness=0, R=np.inf))
            self._sync_grid_to_system()
        elif id == self.DATAROW_MENUINSERTBEFORE:
            self.grid1.InsertRows(r)            
            self.__system.insert_surface(r, DataModel.StandardSurface(thickness=0, R=np.inf))
            self._sync_grid_to_system()
        elif id == self.DATAROW_MENUDELETE:
            self.grid1.DeleteRows(r)
            self.__system.delete_surface(r)
            
            
##        if(id ==   self.wxID_MENU1COPY):
##            print 'not yet implemented'
##        if(id == self.wxID_MENU1PASTE):
##            print 'not yet implemented'
            
        event.Skip()
        

    def OnMenu_thicknessitems0Menu(self, event):
        (r,c) = (self.grid1.GetGridCursorRow(),self.grid1.GetGridCursorCol())
        id = event.GetId()
        if(id == self.wxID_MENU_THICKNESSITEMS0):
            self.checkBox_autofocus.SetValue(True)
            self.OnGrid1GridCellChange(None,r, c)
            self.checkBox_autofocus.SetValue(False)
    
    def OnMenu_glassitems0Menu(self, event):
        r, c = self.grid1.GetGridCursorRow(), self.grid1.GetGridCursorCol()
        id = event.GetId()
        if id == self.MENU_GLASSDIRECT:
            self.grid1.SetCellValue(r,c,'')
        elif id == self.MENU_GLASSBK7:            
            self.grid1.SetCellValue(r,c,'BK7')
 
 
        #event.Skip()

    def OnTextctrl_object_heightText(self, event):
        #self.object_height = float(self.textCtrl_object_height.GetValue())
        self.OnGrid1GridCellChange() #event=None,r=0,c=self.THICKNESS_COL)               
        event.Skip()

    def OnButton_compute_allButton(self, event):
        self.OnButton_spot_diagramsButton()
        self.OnButton_imageButton()

    def OnButton_wave_lengthsButton(self, event):
        self.waves.Show()                                                         
        event.Skip()

    def OnButton_spot_diagramsButton(self, event = None):
        if(not self.GetParent().spot.IsShown()):
            self.GetParent().spot.Show()
        self.GetParent().spot.draw_spots(self.t,self.n,self.c,self.t_cum,self.h,self.object_height)            
        
        

    def OnButton_imageButton(self, event=None):           
        self.GetParent().img.Show()

        img = np.array([[1,1,1,1,1],
                        [1,0,1,.8,1],    
                        [1,1,1,1,1],
                        [1,.5,1,0,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1]])                                     
        self.GetParent().img.draw_image(img,self.object_height,self.t,self.n,self.c,self.t_cum,self.h)

