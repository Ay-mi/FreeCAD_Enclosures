import FreeCAD as App
import FreeCADGui
import Part
import Sketcher
import PartDesignGui

if App.ActiveDocument is None:
    App.newDocument("Unnamed")

doc = App.ActiveDocument

# Ensure there's a Body
body = doc.getObject("Body")
if body is None:
    body = doc.addObject("PartDesign::Body", "Body")
    doc.recompute()

App.ActiveDocument.getObject('Body').newObject('Sketcher::SketchObject','Sketch')
App.ActiveDocument.getObject('Sketch').AttachmentSupport = (App.ActiveDocument.getObject('XY_Plane'),[''])
App.ActiveDocument.getObject('Sketch').MapMode = 'FlatFace'
App.ActiveDocument.recompute()

ActiveSketch = App.ActiveDocument.getObject('Sketch')

lastGeoId = len(ActiveSketch.Geometry)

geoList = []
geoList.append(Part.LineSegment(App.Vector(-49.500000, -34.500000, 0.000000),App.Vector(49.500000, -34.500000, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(49.500000, -34.500000, 0.000000),App.Vector(49.500000, 34.500000, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(49.500000, 34.500000, 0.000000),App.Vector(-49.500000, 34.500000, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-49.500000, 34.500000, 0.000000),App.Vector(-49.500000, -34.500000, 0.000000)))
App.ActiveDocument.getObject('Sketch').addGeometry(geoList,False)
del geoList

constrGeoList = []
constrGeoList.append(Part.Point(App.Vector(0.000000, 0.000000, 0.000000)))
App.ActiveDocument.getObject('Sketch').addGeometry(constrGeoList,True)
del constrGeoList

constraintList = []
constraintList.append(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
constraintList.append(Sketcher.Constraint('Coincident', 1, 2, 2, 1))
constraintList.append(Sketcher.Constraint('Coincident', 2, 2, 3, 1))
constraintList.append(Sketcher.Constraint('Coincident', 3, 2, 0, 1))
constraintList.append(Sketcher.Constraint('Horizontal', 0))
constraintList.append(Sketcher.Constraint('Horizontal', 2))
constraintList.append(Sketcher.Constraint('Vertical', 1))
constraintList.append(Sketcher.Constraint('Vertical', 3))
constraintList.append(Sketcher.Constraint('Symmetric', 2, 1, 0, 1, 4, 1))
App.ActiveDocument.getObject('Sketch').addConstraint(constraintList)
del constraintList

App.ActiveDocument.getObject('Sketch').addConstraint(Sketcher.Constraint('Distance',1,1,3,2,100.000000)) 
App.ActiveDocument.getObject('Sketch').addConstraint(Sketcher.Constraint('Distance',0,1,2,2,70.000000)) 
App.ActiveDocument.getObject('Sketch').addConstraint(Sketcher.Constraint('Coincident', 4, 1, -1, 1))

# Gui.getDocument('Unnamed').resetEdit()
App.ActiveDocument.recompute()

App.ActiveDocument.recompute()
### Begin command PartDesign_Pad
App.ActiveDocument.getObject('Body').newObject('PartDesign::Pad','Pad')
App.ActiveDocument.getObject('Pad').Profile = (App.ActiveDocument.getObject('Sketch'), ['',])
App.ActiveDocument.getObject('Pad').Length = 10
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Pad').ReferenceAxis = (App.ActiveDocument.getObject('Sketch'),['N_Axis'])
App.ActiveDocument.getObject('Sketch').Visibility = False
App.ActiveDocument.recompute()

App.ActiveDocument.getObject('Pad').Length = 30.00000
App.ActiveDocument.getObject('Pad').TaperAngle = 0.000000
App.ActiveDocument.getObject('Pad').UseCustomVector = 0
App.ActiveDocument.getObject('Pad').Direction = (0, 0, 1)
App.ActiveDocument.getObject('Pad').ReferenceAxis = (App.ActiveDocument.getObject('Sketch'), ['N_Axis'])
App.ActiveDocument.getObject('Pad').AlongSketchNormal = 1
App.ActiveDocument.getObject('Pad').Type = 0
App.ActiveDocument.getObject('Pad').UpToFace = None
App.ActiveDocument.getObject('Pad').Reversed = 0
App.ActiveDocument.getObject('Pad').Midplane = 0
App.ActiveDocument.getObject('Pad').Offset = 0
App.ActiveDocument.recompute()
# Gui.getDocument('Unnamed').resetEdit()
App.ActiveDocument.getObject('Sketch').Visibility = False
# Gui.Selection.addSelection('Unnamed','Body','Pad.Face6',-21.6638,12.3227,28.5)
### Begin command PartDesign_Thickness
App.ActiveDocument.getObject('Body').newObject('PartDesign::Thickness','Thickness')

pad = App.ActiveDocument.getObject('Pad')
shape = pad.Shape

# Try to select a Z+ face
z_up = App.Vector(0, 0, 1)
face_name = None
for i, face in enumerate(shape.Faces, 1):
    if face.normalAt(0.5, 0.5).getAngle(z_up) < 0.01:  # approx 0 deg
        face_name = f"Face{i}"
        break

if face_name:
    App.ActiveDocument.getObject('Thickness').Base = (pad, [face_name])
else:
    raise Exception("No upward-facing face found for Thickness.")


# Gui.Selection.clearSelection()
App.ActiveDocument.getObject('Pad').Visibility = False
App.ActiveDocument.recompute()

App.ActiveDocument.getObject('Thickness').Value = 5
App.ActiveDocument.getObject('Thickness').Reversed = 1
App.ActiveDocument.getObject('Thickness').Mode = 0
App.ActiveDocument.getObject('Thickness').Intersection = 0
App.ActiveDocument.getObject('Thickness').Join = 0
App.ActiveDocument.getObject('Thickness').Base = (App.ActiveDocument.getObject('Pad'),["Face6",])
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Pad').Visibility = False

print("Sketch in Body:", "Sketch" in [obj.Name for obj in body.Group])
print("Sketch visibility:", doc.getObject("Sketch").Visibility)

#Part 2 Creating cavity using thickness -------------------
App.ActiveDocument.getObject('Body').newObject('Sketcher::SketchObject','Sketch001')
App.ActiveDocument.getObject('Sketch001').AttachmentSupport = (App.ActiveDocument.getObject('Thickness'),['Face1',])
App.ActiveDocument.getObject('Sketch001').MapMode = 'FlatFace'
App.ActiveDocument.recompute()

ActiveSketch = App.ActiveDocument.getObject('Sketch001')

lastGeoId = len(ActiveSketch.Geometry)

geoList = []
geoList.append(Part.LineSegment(App.Vector(-10.000000, 25.461521, 0.000000),App.Vector(10.000000, 25.461521, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(10.000000, 25.461521, 0.000000),App.Vector(10.000000, 35.461521, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(10.000000, 35.461521, 0.000000),App.Vector(-10.000000, 35.461521, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-10.000000, 35.461521, 0.000000),App.Vector(-10.000000, 25.461521, 0.000000)))
App.ActiveDocument.getObject('Sketch001').addGeometry(geoList,False)
del geoList
 
constrGeoList = []
constrGeoList.append(Part.Point(App.Vector(0.000000, 30.461521, 0.000000)))
App.ActiveDocument.getObject('Sketch001').addGeometry(constrGeoList,True)
del constrGeoList
 
constraintList = []
constraintList.append(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
constraintList.append(Sketcher.Constraint('Coincident', 1, 2, 2, 1))
constraintList.append(Sketcher.Constraint('Coincident', 2, 2, 3, 1))
constraintList.append(Sketcher.Constraint('Coincident', 3, 2, 0, 1))
constraintList.append(Sketcher.Constraint('Horizontal', 0))
constraintList.append(Sketcher.Constraint('Horizontal', 2))
constraintList.append(Sketcher.Constraint('Vertical', 1))
constraintList.append(Sketcher.Constraint('Vertical', 3))
constraintList.append(Sketcher.Constraint('Symmetric', 2, 1, 0, 1, 4, 1))
App.ActiveDocument.getObject('Sketch001').addConstraint(constraintList)
del constraintList
 
App.ActiveDocument.getObject('Sketch001').addConstraint(Sketcher.Constraint('Distance',1,1,3,2,20.000000)) 
App.ActiveDocument.getObject('Sketch001').addConstraint(Sketcher.Constraint('Distance',0,1,2,2,10.000000)) 
App.ActiveDocument.getObject('Sketch001').addConstraint(Sketcher.Constraint('PointOnObject', 4, 1, -2))

App.ActiveDocument.getObject('Sketch001').addExternal("Thickness","Edge4")

### Begin command Sketcher_Dimension
App.ActiveDocument.getObject('Sketch001').addConstraint(Sketcher.Constraint('Distance',2,2,-3,6.961521)) 
### End command Sketcher_Dimension

App.ActiveDocument.getObject('Sketch001').setDatum(12,App.Units.Quantity('0.500000 mm'))
App.ActiveDocument.recompute()

App.ActiveDocument.getObject('Body').newObject('PartDesign::Pocket','Pocket')
App.ActiveDocument.getObject('Pocket').Profile = (App.ActiveDocument.getObject('Sketch001'), ['',])
App.ActiveDocument.getObject('Pocket').Length = 5
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Pocket').ReferenceAxis = (App.ActiveDocument.getObject('Sketch001'),['N_Axis'])
App.ActiveDocument.getObject('Sketch001').Visibility = False
App.ActiveDocument.recompute()

App.ActiveDocument.getObject('Pocket').Length = 3.000000
App.ActiveDocument.getObject('Pocket').TaperAngle = 0.000000
App.ActiveDocument.getObject('Pocket').UseCustomVector = 0
App.ActiveDocument.getObject('Pocket').Direction = (0, 1, -0)
App.ActiveDocument.getObject('Pocket').ReferenceAxis = (App.ActiveDocument.getObject('Sketch001'), ['N_Axis'])
App.ActiveDocument.getObject('Pocket').AlongSketchNormal = 1
App.ActiveDocument.getObject('Pocket').Type = 0
App.ActiveDocument.getObject('Pocket').UpToFace = None
App.ActiveDocument.getObject('Pocket').Reversed = 0
App.ActiveDocument.getObject('Pocket').Midplane = 0
App.ActiveDocument.getObject('Pocket').Offset = 0
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Thickness').Visibility = False
App.ActiveDocument.getObject('Sketch001').Visibility = False

#Part 3 ----------------------------
App.ActiveDocument.getObject('Body').newObject('Sketcher::SketchObject','Sketch002')
App.ActiveDocument.getObject('Sketch002').AttachmentSupport = (App.ActiveDocument.getObject('Pocket'),['Face7',])
App.ActiveDocument.getObject('Sketch002').MapMode = 'FlatFace'
App.ActiveDocument.recompute()

ActiveSketch = App.ActiveDocument.getObject('Sketch002')

App.ActiveDocument.getObject('Sketch002').addExternal("Pocket","Edge6")
App.ActiveDocument.getObject('Sketch002').addExternal("Pocket","Edge27")

App.ActiveDocument.getObject('Sketch002').addGeometry(Part.LineSegment(App.Vector(-31.500000,28.500000,0),App.Vector(-34.500000,26.455278,0)),False)
App.ActiveDocument.getObject('Sketch002').addConstraint(Sketcher.Constraint('Coincident',-4,1,0,1)) 
App.ActiveDocument.getObject('Sketch002').addConstraint(Sketcher.Constraint('PointOnObject',0,2,-3)) 
App.ActiveDocument.getObject('Sketch002').addGeometry(Part.LineSegment(App.Vector(-34.500000,26.455278,0),App.Vector(-31.500000,24.904482,0)),False)
App.ActiveDocument.getObject('Sketch002').addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
App.ActiveDocument.getObject('Sketch002').addConstraint(Sketcher.Constraint('PointOnObject',1,2,-4)) 
App.ActiveDocument.getObject('Sketch002').addGeometry(Part.LineSegment(App.Vector(-31.500000,24.904482,0),App.Vector(-31.500000,28.500000,0)),False)
App.ActiveDocument.getObject('Sketch002').addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
App.ActiveDocument.getObject('Sketch002').addConstraint(Sketcher.Constraint('Coincident',2,2,0,1)) 
#App.ActiveDocument.getObject('Sketch002').addConstraint(Sketcher.Constraint('Vertical',2)) 

App.ActiveDocument.getObject('Sketch002').addConstraint(Sketcher.Constraint('Equal',0,1))
App.ActiveDocument.getObject('Sketch002').addConstraint(Sketcher.Constraint('Equal',1,2))

App.ActiveDocument.recompute()

App.ActiveDocument.getObject('Body').newObject('PartDesign::Pad','Pad001')
App.ActiveDocument.getObject('Pad001').Profile = (App.ActiveDocument.getObject('Sketch002'), ['',])
App.ActiveDocument.getObject('Pad001').Length = 10
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Pad001').ReferenceAxis = (App.ActiveDocument.getObject('Sketch002'),['N_Axis'])
App.ActiveDocument.getObject('Sketch002').Visibility = False
App.ActiveDocument.recompute()

App.ActiveDocument.getObject('Pad001').UseCustomVector = 0
App.ActiveDocument.getObject('Pad001').Direction = (1, 0, 0)
App.ActiveDocument.getObject('Pad001').ReferenceAxis = (App.ActiveDocument.getObject('Sketch002'), ['N_Axis'])
App.ActiveDocument.getObject('Pad001').AlongSketchNormal = 1
App.ActiveDocument.getObject('Pad001').Type = 3
App.ActiveDocument.getObject('Pad001').UpToFace = (App.ActiveDocument.Pocket, ["Face5"])
App.ActiveDocument.getObject('Pad001').Reversed = 0
App.ActiveDocument.getObject('Pad001').Midplane = 0
App.ActiveDocument.getObject('Pad001').Offset = 0
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Pocket').Visibility = False
App.ActiveDocument.getObject('Sketch002').Visibility = False

### Part 4 Mirroring --------------------
### Begin command PartDesign_Mirrored
App.ActiveDocument.getObject('Body').newObject('PartDesign::Mirrored','Mirrored')
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Mirrored').Originals = [App.ActiveDocument.getObject('Pocket'), App.ActiveDocument.getObject('Pad001')]
App.ActiveDocument.getObject('Mirrored').MirrorPlane = (App.ActiveDocument.getObject('Sketch001'), ['V_Axis'])
App.ActiveDocument.recompute()

App.ActiveDocument.getObject('Body').Tip = App.ActiveDocument.getObject('Mirrored')
App.ActiveDocument.recompute()
### End command PartDesign_Mirrored
# Gui.Selection.clearSelection()
App.ActiveDocument.getObject('Mirrored').Visibility = True
App.ActiveDocument.getObject('Mirrored').Visibility = True
App.ActiveDocument.getObject('Mirrored').MirrorPlane = (App.ActiveDocument.getObject('XZ_Plane'), [''])
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Pad001').Visibility = False

### Part 5 Adding holes for ports Side 1 -------------------------
App.ActiveDocument.getObject('Body').newObject('Sketcher::SketchObject','Sketch003')
App.ActiveDocument.getObject('Sketch003').AttachmentSupport = (App.ActiveDocument.getObject('Mirrored'),['Face1',])
App.ActiveDocument.getObject('Sketch003').MapMode = 'FlatFace'
App.ActiveDocument.recompute()

ActiveSketch = App.ActiveDocument.getObject('Sketch003')

lastGeoId = len(ActiveSketch.Geometry)

geoList = []
geoList.append(Part.LineSegment(App.Vector(-38.619640, 12.767712, 0.000000),App.Vector(-38.619640, 7.852376, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-38.619640, 7.852376, 0.000000),App.Vector(-28.024366, 7.852376, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-28.024366, 7.852376, 0.000000),App.Vector(-28.024366, 12.767712, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-28.024366, 12.767712, 0.000000),App.Vector(-38.619640, 12.767712, 0.000000)))
App.ActiveDocument.getObject('Sketch003').addGeometry(geoList,False)
del geoList

constraintList = []
constraintList.append(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
constraintList.append(Sketcher.Constraint('Coincident', 1, 2, 2, 1))
constraintList.append(Sketcher.Constraint('Coincident', 2, 2, 3, 1))
constraintList.append(Sketcher.Constraint('Coincident', 3, 2, 0, 1))
constraintList.append(Sketcher.Constraint('Vertical', 0))
constraintList.append(Sketcher.Constraint('Vertical', 2))
constraintList.append(Sketcher.Constraint('Horizontal', 1))
constraintList.append(Sketcher.Constraint('Horizontal', 3))
App.ActiveDocument.getObject('Sketch003').addConstraint(constraintList)
del constraintList

constraintList = []
ActiveSketch = App.ActiveDocument.getObject('Sketch003')

lastGeoId = len(ActiveSketch.Geometry)

geoList = []
geoList.append(Part.LineSegment(App.Vector(-22.999802, 12.713097, 0.000000),App.Vector(-22.999802, 7.797761, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-22.999802, 7.797761, 0.000000),App.Vector(-14.097582, 7.797761, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-14.097582, 7.797761, 0.000000),App.Vector(-14.097582, 12.713097, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-14.097582, 12.713097, 0.000000),App.Vector(-22.999802, 12.713097, 0.000000)))
App.ActiveDocument.getObject('Sketch003').addGeometry(geoList,False)
del geoList

constraintList = []
constraintList.append(Sketcher.Constraint('Coincident', 4, 2, 5, 1))
constraintList.append(Sketcher.Constraint('Coincident', 5, 2, 6, 1))
constraintList.append(Sketcher.Constraint('Coincident', 6, 2, 7, 1))
constraintList.append(Sketcher.Constraint('Coincident', 7, 2, 4, 1))
constraintList.append(Sketcher.Constraint('Vertical', 4))
constraintList.append(Sketcher.Constraint('Vertical', 6))
constraintList.append(Sketcher.Constraint('Horizontal', 5))
constraintList.append(Sketcher.Constraint('Horizontal', 7))
App.ActiveDocument.getObject('Sketch003').addConstraint(constraintList)
del constraintList

constraintList = []
ActiveSketch = App.ActiveDocument.getObject('Sketch003')

lastGeoId = len(ActiveSketch.Geometry)

geoList = []
geoList.append(Part.LineSegment(App.Vector(-9.455320, 12.494637, 0.000000),App.Vector(-9.455320, 7.852376, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-9.455320, 7.852376, 0.000000),App.Vector(-0.880794, 7.852376, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-0.880794, 7.852376, 0.000000),App.Vector(-0.880794, 12.494637, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-0.880794, 12.494637, 0.000000),App.Vector(-9.455320, 12.494637, 0.000000)))
App.ActiveDocument.getObject('Sketch003').addGeometry(geoList,False)
del geoList

constraintList = []
constraintList.append(Sketcher.Constraint('Coincident', 8, 2, 9, 1))
constraintList.append(Sketcher.Constraint('Coincident', 9, 2, 10, 1))
constraintList.append(Sketcher.Constraint('Coincident', 10, 2, 11, 1))
constraintList.append(Sketcher.Constraint('Coincident', 11, 2, 8, 1))
constraintList.append(Sketcher.Constraint('Vertical', 8))
constraintList.append(Sketcher.Constraint('Vertical', 10))
constraintList.append(Sketcher.Constraint('Horizontal', 9))
constraintList.append(Sketcher.Constraint('Horizontal', 11))
App.ActiveDocument.getObject('Sketch003').addConstraint(constraintList)
del constraintList

constraintList = []
ActiveSketch = App.ActiveDocument.getObject('Sketch003')

lastGeoId = len(ActiveSketch.Geometry)

geoList = []
geoList.append(Part.LineSegment(App.Vector(5.072227, 15.443838, 0.000000),App.Vector(5.072227, 7.797761, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(5.072227, 7.797761, 0.000000),App.Vector(13.919830, 7.797761, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(13.919830, 7.797761, 0.000000),App.Vector(13.919830, 15.443838, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(13.919830, 15.443838, 0.000000),App.Vector(5.072227, 15.443838, 0.000000)))
App.ActiveDocument.getObject('Sketch003').addGeometry(geoList,False)
del geoList

constraintList = []
constraintList.append(Sketcher.Constraint('Coincident', 12, 2, 13, 1))
constraintList.append(Sketcher.Constraint('Coincident', 13, 2, 14, 1))
constraintList.append(Sketcher.Constraint('Coincident', 14, 2, 15, 1))
constraintList.append(Sketcher.Constraint('Coincident', 15, 2, 12, 1))
constraintList.append(Sketcher.Constraint('Vertical', 12))
constraintList.append(Sketcher.Constraint('Vertical', 14))
constraintList.append(Sketcher.Constraint('Horizontal', 13))
constraintList.append(Sketcher.Constraint('Horizontal', 15))
App.ActiveDocument.getObject('Sketch003').addConstraint(constraintList)
del constraintList

constraintList = []
# Gui.getDocument('DrawingDoc').resetEdit()
App.ActiveDocument.recompute()

App.ActiveDocument.recompute()
### Begin command PartDesign_Pocket
App.ActiveDocument.getObject('Body').newObject('PartDesign::Pocket','Pocket001')
App.ActiveDocument.getObject('Pocket001').Profile = (App.ActiveDocument.getObject('Sketch003'), ['',])
App.ActiveDocument.getObject('Pocket001').Length = 5
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Pocket001').ReferenceAxis = (App.ActiveDocument.getObject('Sketch003'),['N_Axis'])
App.ActiveDocument.getObject('Sketch003').Visibility = False
App.ActiveDocument.recompute()

App.ActiveDocument.getObject('Pocket001').Length = 5.000000
App.ActiveDocument.getObject('Pocket001').TaperAngle = 0.000000
App.ActiveDocument.getObject('Pocket001').UseCustomVector = 0
App.ActiveDocument.getObject('Pocket001').Direction = (0, 1, -0)
App.ActiveDocument.getObject('Pocket001').ReferenceAxis = (App.ActiveDocument.getObject('Sketch003'), ['N_Axis'])
App.ActiveDocument.getObject('Pocket001').AlongSketchNormal = 1
App.ActiveDocument.getObject('Pocket001').Type = 0
App.ActiveDocument.getObject('Pocket001').UpToFace = None
App.ActiveDocument.getObject('Pocket001').Reversed = 0
App.ActiveDocument.getObject('Pocket001').Midplane = 0
App.ActiveDocument.getObject('Pocket001').Offset = 0
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Mirrored').Visibility = False
# Gui.getDocument('DrawingDoc').resetEdit()
App.ActiveDocument.getObject('Sketch003').Visibility = False

App.ActiveDocument.getObject('Body').newObject('Sketcher::SketchObject','Sketch004')
App.ActiveDocument.getObject('Sketch004').AttachmentSupport = (App.ActiveDocument.getObject('Pocket001'),['Face1',])
App.ActiveDocument.getObject('Sketch004').MapMode = 'FlatFace'
App.ActiveDocument.recompute()

ActiveSketch = App.ActiveDocument.getObject('Sketch004')

lastGeoId = len(ActiveSketch.Geometry)

geoList = []
geoList.append(Part.LineSegment(App.Vector(17.684753, 17.671261, 0.000000),App.Vector(-42.258995, 17.671261, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-42.258995, 17.671261, 0.000000),App.Vector(-42.258995, 6.687156, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-42.258995, 6.687156, 0.000000),App.Vector(17.684753, 6.687156, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(17.684753, 6.687156, 0.000000),App.Vector(17.684753, 17.671261, 0.000000)))
App.ActiveDocument.getObject('Sketch004').addGeometry(geoList,False)
del geoList

constraintList = []
constraintList.append(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
constraintList.append(Sketcher.Constraint('Coincident', 1, 2, 2, 1))
constraintList.append(Sketcher.Constraint('Coincident', 2, 2, 3, 1))
constraintList.append(Sketcher.Constraint('Coincident', 3, 2, 0, 1))
constraintList.append(Sketcher.Constraint('Horizontal', 0))
constraintList.append(Sketcher.Constraint('Horizontal', 2))
constraintList.append(Sketcher.Constraint('Vertical', 1))
constraintList.append(Sketcher.Constraint('Vertical', 3))
App.ActiveDocument.getObject('Sketch004').addConstraint(constraintList)
del constraintList

constraintList = []
# Gui.getDocument('DrawingDoc').resetEdit()
App.ActiveDocument.recompute()

# Gui.Selection.addSelection('DrawingDoc','Body','Sketch004.')
App.ActiveDocument.recompute()
### Begin command PartDesign_Pocket
App.ActiveDocument.getObject('Body').newObject('PartDesign::Pocket','Pocket002')
App.ActiveDocument.getObject('Pocket002').Profile = (App.ActiveDocument.getObject('Sketch004'), ['',])
App.ActiveDocument.getObject('Pocket002').Length = 5
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Pocket002').ReferenceAxis = (App.ActiveDocument.getObject('Sketch004'),['N_Axis'])
App.ActiveDocument.getObject('Sketch004').Visibility = False
App.ActiveDocument.recompute()

# Gui.Selection.clearSelection()
App.ActiveDocument.getObject('Pocket002').Length = 2.000000
App.ActiveDocument.getObject('Pocket002').TaperAngle = 0.000000
App.ActiveDocument.getObject('Pocket002').UseCustomVector = 0
App.ActiveDocument.getObject('Pocket002').Direction = (0, 1, -0)
App.ActiveDocument.getObject('Pocket002').ReferenceAxis = (App.ActiveDocument.getObject('Sketch004'), ['N_Axis'])
App.ActiveDocument.getObject('Pocket002').AlongSketchNormal = 1
App.ActiveDocument.getObject('Pocket002').Type = 0
App.ActiveDocument.getObject('Pocket002').UpToFace = None
App.ActiveDocument.getObject('Pocket002').Reversed = 0
App.ActiveDocument.getObject('Pocket002').Midplane = 0
App.ActiveDocument.getObject('Pocket002').Offset = 0
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Pocket001').Visibility = False
# Gui.getDocument('DrawingDoc').resetEdit()
App.ActiveDocument.getObject('Sketch004').Visibility = False

### Part 6 Other side of box with USB ports ---------------------------
### Begin command PartDesign_CompSketches
App.ActiveDocument.getObject('Body').newObject('Sketcher::SketchObject','Sketch005')
App.ActiveDocument.getObject('Sketch005').AttachmentSupport = (App.ActiveDocument.getObject('Pocket002'),['Face4',])
App.ActiveDocument.getObject('Sketch005').MapMode = 'FlatFace'
App.ActiveDocument.recompute()

ActiveSketch = App.ActiveDocument.getObject('Sketch005')

lastGeoId = len(ActiveSketch.Geometry)

geoList = []
geoList.append(Part.LineSegment(App.Vector(-26.733162, 25.753414, 0.000000),App.Vector(-26.733162, 6.464256, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-26.733162, 6.464256, 0.000000),App.Vector(-9.654222, 6.464256, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-9.654222, 6.464256, 0.000000),App.Vector(-9.654222, 25.753414, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-9.654222, 25.753414, 0.000000),App.Vector(-26.733162, 25.753414, 0.000000)))
App.ActiveDocument.getObject('Sketch005').addGeometry(geoList,False)
del geoList

constraintList = []
constraintList.append(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
constraintList.append(Sketcher.Constraint('Coincident', 1, 2, 2, 1))
constraintList.append(Sketcher.Constraint('Coincident', 2, 2, 3, 1))
constraintList.append(Sketcher.Constraint('Coincident', 3, 2, 0, 1))
constraintList.append(Sketcher.Constraint('Vertical', 0))
constraintList.append(Sketcher.Constraint('Vertical', 2))
constraintList.append(Sketcher.Constraint('Horizontal', 1))
constraintList.append(Sketcher.Constraint('Horizontal', 3))
App.ActiveDocument.getObject('Sketch005').addConstraint(constraintList)
del constraintList

constraintList = []
ActiveSketch = App.ActiveDocument.getObject('Sketch005')

lastGeoId = len(ActiveSketch.Geometry)

geoList = []
geoList.append(Part.LineSegment(App.Vector(-8.180744, 25.820389, 0.000000),App.Vector(-8.180744, 6.397280, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-8.180744, 6.397280, 0.000000),App.Vector(8.161459, 6.397280, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(8.161459, 6.397280, 0.000000),App.Vector(8.161459, 25.820389, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(8.161459, 25.820389, 0.000000),App.Vector(-8.180744, 25.820389, 0.000000)))
App.ActiveDocument.getObject('Sketch005').addGeometry(geoList,False)
del geoList

constraintList = []
constraintList.append(Sketcher.Constraint('Coincident', 4, 2, 5, 1))
constraintList.append(Sketcher.Constraint('Coincident', 5, 2, 6, 1))
constraintList.append(Sketcher.Constraint('Coincident', 6, 2, 7, 1))
constraintList.append(Sketcher.Constraint('Coincident', 7, 2, 4, 1))
constraintList.append(Sketcher.Constraint('Vertical', 4))
constraintList.append(Sketcher.Constraint('Vertical', 6))
constraintList.append(Sketcher.Constraint('Horizontal', 5))
constraintList.append(Sketcher.Constraint('Horizontal', 7))
App.ActiveDocument.getObject('Sketch005').addConstraint(constraintList)
del constraintList

constraintList = []
ActiveSketch = App.ActiveDocument.getObject('Sketch005')

lastGeoId = len(ActiveSketch.Geometry)

geoList = []
geoList.append(Part.LineSegment(App.Vector(9.434008, 23.208317, 0.000000),App.Vector(9.434008, 7.803781, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(9.434008, 7.803781, 0.000000),App.Vector(28.053404, 7.803781, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(28.053404, 7.803781, 0.000000),App.Vector(28.053404, 23.208317, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(28.053404, 23.208317, 0.000000),App.Vector(9.434008, 23.208317, 0.000000)))
App.ActiveDocument.getObject('Sketch005').addGeometry(geoList,False)
del geoList

constraintList = []
constraintList.append(Sketcher.Constraint('Coincident', 8, 2, 9, 1))
constraintList.append(Sketcher.Constraint('Coincident', 9, 2, 10, 1))
constraintList.append(Sketcher.Constraint('Coincident', 10, 2, 11, 1))
constraintList.append(Sketcher.Constraint('Coincident', 11, 2, 8, 1))
constraintList.append(Sketcher.Constraint('Vertical', 8))
constraintList.append(Sketcher.Constraint('Vertical', 10))
constraintList.append(Sketcher.Constraint('Horizontal', 9))
constraintList.append(Sketcher.Constraint('Horizontal', 11))
App.ActiveDocument.getObject('Sketch005').addConstraint(constraintList)
del constraintList

constraintList = []
# Gui.getDocument('DrawingDoc').resetEdit()
App.ActiveDocument.recompute()

App.ActiveDocument.recompute()
### Begin command PartDesign_Pocket
App.ActiveDocument.getObject('Body').newObject('PartDesign::Pocket','Pocket003')
App.ActiveDocument.getObject('Pocket003').Profile = (App.ActiveDocument.getObject('Sketch005'), ['',])
App.ActiveDocument.getObject('Pocket003').Length = 5
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Pocket003').ReferenceAxis = (App.ActiveDocument.getObject('Sketch005'),['N_Axis'])
App.ActiveDocument.getObject('Sketch005').Visibility = False
App.ActiveDocument.recompute()

App.ActiveDocument.getObject('Pocket003').Length = 5.000000
App.ActiveDocument.getObject('Pocket003').TaperAngle = 0.000000
App.ActiveDocument.getObject('Pocket003').UseCustomVector = 0
App.ActiveDocument.getObject('Pocket003').Direction = (-1, 0, 0)
App.ActiveDocument.getObject('Pocket003').ReferenceAxis = (App.ActiveDocument.getObject('Sketch005'), ['N_Axis'])
App.ActiveDocument.getObject('Pocket003').AlongSketchNormal = 1
App.ActiveDocument.getObject('Pocket003').Type = 0
App.ActiveDocument.getObject('Pocket003').UpToFace = None
App.ActiveDocument.getObject('Pocket003').Reversed = 0
App.ActiveDocument.getObject('Pocket003').Midplane = 0
App.ActiveDocument.getObject('Pocket003').Offset = 0
App.ActiveDocument.recompute()
App.ActiveDocument.getObject('Pocket002').Visibility = False
# Gui.getDocument('DrawingDoc').resetEdit()
App.ActiveDocument.getObject('Sketch005').Visibility = False
