# Automating Enclosure Generation in FreeCAD
Welcome to my FYP journey.    
This repository contains the macro files that automate the generation of electronic enclosures in FreeCAD.  
FreeCAD supports two modelling techniques: 
- constructive solid geometry (CSG) modelling which is done using the Part Workbench
- parametric modelling which is done mostly using the Sketcher and Part Design Workbench

Although parametric modelling is a more modern type of modelling, the Python script is much longer and more difficult to generalize into functions. Using CSG modelling (the Part Workbench), the script is easier to simplify and functionalize making it possible to reuse for other PCB boards.
However, there is an issue with CSG modelling, it creates too many pieces which can complicate editing the generated enclosure. With parametric modelling, there are less pieces involved which makes it easier for the user to pickup where the script left off.

So far there are only macros for the RaspberryPi 4.

### Images:
Raspberry Pi 4 case (created using CSG)
<img width="2300" alt="image" src="https://github.com/user-attachments/assets/5946d7fe-e48f-4ade-8436-a64ac2be7d3f" />
<img width="2300" alt="image" src="https://github.com/user-attachments/assets/b1a555f3-9a95-4cad-a4a1-d055b48c8dec" />
<img width="2300" alt="image" src="https://github.com/user-attachments/assets/5a47cb86-419c-4a1f-9c6d-c0ff12d4993d" />
