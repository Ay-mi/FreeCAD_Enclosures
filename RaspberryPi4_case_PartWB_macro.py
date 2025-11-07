import FreeCAD as App
import FreeCADGui as Gui
import PartDesign
import Sketcher
from BOPTools import BOPFeatures

doc = FreeCAD.activeDocument()
bp = BOPFeatures.BOPFeatures(doc)

def makeBox(box_label, width, length, height, vector, face_num):
    cube = doc.addObject("Part::Box", box_label)
    cube.Label = box_label
    cube.Width = width
    cube.Length = length
    cube.Height = height

    if face_num == 2:
        cube.Placement.Base = App.Vector(43.3, vector, -3.43253)  # No change here unless needed
    elif face_num == 1:
        cube.Placement.Base = App.Vector(vector, -32.95, -3.2121)
    elif face_num == 'outer':
        cube.Placement.Base = App.Vector(-47.8, -32.95, -12)
    elif face_num == 'inner':
        cube.Placement.Base = App.Vector(-45.3, -30.45, -7)

    doc.recompute()
    return cube


def makeCylinder(cy_label, radius, height, vectorx, vectory, vectorz, face_num):
    cylinder = doc.addObject("Part::Cylinder", "Microphone_Cyl")
    cylinder.Label = cy_label
    cylinder.Radius = radius
    cylinder.Height = height
    cylinder.Placement.Base = App.Vector(vectorx, vectory, vectorz)
    if face_num == 1:
        cylinder.Placement.Rotation = App.Rotation(App.Vector(1,0,0), 90) # align along Y-axis
        doc.recompute()
    return cylinder

def cutBox(prev_shape, shape):
    # Cut it from the base shape
    cut_result = bp.make_cut([prev_shape.Name, shape.Name])
    print(cut_result)
    doc.recompute()

    return cut_result

extBox = makeBox("ExtBox", 65.9, 95.6, 28.5, 0, "outer")
inner_box = makeBox("InnerBox", 60.9, 90.6, 23.5, 0, "inner")

#subtract inner box from outer box to create crate
enclosure_basic = cutBox(extBox, inner_box)

#doc.getObject("BoxExt").Visibility = False
#doc.getObject("InnerBox").Visibility = False

doc.recompute()
Gui.SendMsgToActiveView("ViewFit")

#colour outside
Gui.ActiveDocument.getObject(enclosure_basic.Name).ShapeColor = (0.40,0.00,0.15)

#---------------------------------------------
usb2 = makeBox("Usb2Box", 15, 5, 16.5, -26.234, 2)
usb2_cut = cutBox(enclosure_basic, usb2)

usb3 = makeBox("Usb3Box", 15, 5, 16.5,-8.52865, 2)
usb3_cut = cutBox(usb2_cut, usb3)
ethernet = makeBox("EthernetBox", 17, 5, 14, 9.36328, 2)
ethernet_cut = cutBox(usb3_cut, ethernet)
usbc = makeBox("UsbcBox", 5, 10, 4.2, -38.3851, 1)
usbc_cut = cutBox(ethernet_cut, usbc)
hdmi1 = makeBox("MicroHDMI1_Box", 5, 8.5, 4.5, -22.3274, 1)
hdmi1_cut = cutBox(usbc_cut, hdmi1)
hdmi2 = makeBox("MicroHDMI2_Box", 5, 8.5, 4.5, -9.25, 1)
hdmi2_cut = cutBox(hdmi1_cut, hdmi2)

microphone = makeCylinder("Microphone_Cyl", 3.5, 7, 9.40268, -27.95, 0, 1)
microphone_cut = cutBox(hdmi2_cut, microphone)
Gui.SendMsgToActiveView("ViewFit")
