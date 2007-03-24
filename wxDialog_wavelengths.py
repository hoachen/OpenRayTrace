#Boa:Dialog:wxDialog_wavelengths

from wxPython.wx import *
from wxPython.grid import *

def create(parent):
    return wxDialog_wavelengths(parent)

[wxID_WXDIALOG_WAVELENGTHS, wxID_WXDIALOG_WAVELENGTHSBUTTON_CANCEL, 
 wxID_WXDIALOG_WAVELENGTHSBUTTON_OK, wxID_WXDIALOG_WAVELENGTHSGRID1, 
] = map(lambda _init_ctrls: wxNewId(), range(4))

class wxDialog_wavelengths(wxDialog):
    def _init_utils(self):
        # generated method, don't edit
        pass

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wxDialog.__init__(self, id=wxID_WXDIALOG_WAVELENGTHS,
              name='wxDialog_wavelengths', parent=prnt, pos=wxPoint(469, 281),
              size=wxSize(481, 373), style=wxDEFAULT_DIALOG_STYLE,
              title='Wave Lengths')
        self._init_utils()
        self.SetClientSize(wxSize(473, 339))

        self.grid1 = wxGrid(id=wxID_WXDIALOG_WAVELENGTHSGRID1, name='grid1',
              parent=self, pos=wxPoint(40, 48), size=wxSize(280, 232), style=0)

        self.button_ok = wxButton(id=wxID_WXDIALOG_WAVELENGTHSBUTTON_OK,
              label='Ok', name='button_ok', parent=self, pos=wxPoint(360, 40),
              size=wxSize(75, 23), style=0)
        EVT_BUTTON(self.button_ok, wxID_WXDIALOG_WAVELENGTHSBUTTON_OK,
              self.OnButton_okButton)

        self.button_cancel = wxButton(id=wxID_WXDIALOG_WAVELENGTHSBUTTON_CANCEL,
              label='Cancel', name='button_cancel', parent=self,
              pos=wxPoint(360, 80), size=wxSize(75, 23), style=0)
        EVT_BUTTON(self.button_cancel, wxID_WXDIALOG_WAVELENGTHSBUTTON_CANCEL,
              self.OnButton_cancelButton)

    def __init__(self, parent):
        self._init_ctrls(parent)

        self.rows = 5
        self.col_label = ['Wavelength [nm]', 'Weight']
        self.grid1.CreateGrid(self.rows,len(self.col_label))

        [self.grid1.SetColLabelValue(i,self.col_label[i]) for i in range(len(self.col_label))]
        self.grid1.SetDefaultCellAlignment(wxALIGN_CENTRE,wxALIGN_CENTRE)
        
        self.grid1.SetCellValue(0,0,str('650'))
        self.grid1.SetCellValue(0,1,str('1'))
        
        self.grid1.SetCellValue(1,0,str('480'))
        self.grid1.SetCellValue(1,1,str('1'))
        
        self.grid1.SetCellValue(2,0,str('700'))
        self.grid1.SetCellValue(2,1,str('1'))
        
        self.grid1.AutoSize()
                
        for row in range(self.rows):
            for col in range(len(self.col_label)):
                self.grid1.SetCellEditor(row, col, apply(wxGridCellFloatEditor,[]))                    

    def OnButton_okButton(self, event):
        self.Hide()
        event.Skip()

    def OnButton_cancelButton(self, event):
        self.Hide()
        event.Skip()
        
    def GetWaveLengths(self):
        res = [float(self.grid1.GetCellValue(i,0)) for i in range(3)]
        return res
