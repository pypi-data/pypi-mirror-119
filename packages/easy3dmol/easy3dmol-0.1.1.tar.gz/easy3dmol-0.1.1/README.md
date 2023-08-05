# easy3dmol
This is a developing tool which add parameters comments on py3Dmol
# Example
```python
# jupyter
from easy3dmol import view
from rdkit import Chem
from rdkit.Chem import AllChem
from easy3dmol.type import ArrowSpec,Vector3,BoxSpec,CurveSpec,CylinderSpec,LabelSpec,AtomSelectionSpec,LineSpec
a=view()
m=Chem.AddHs(Chem.MolFromSmiles("C"))
AllChem.EmbedMolecule(m)
m=Chem.MolToMolBlock(m)


a.add.Model(m,"mol")
a.add.Arrow(ArrowSpec(start=Vector3(0,0,0),end=Vector3(10,10,10)))
a.add.Box(BoxSpec(corner=Vector3(0,0,0),center=Vector3(5,5,5)))
a.add.Cylinder(CylinderSpec(start=Vector3(-2,-2,-2),end=Vector3(2,3,4),radius=0.2,dashed=True))
a.add.Label("hello world",LabelSpec(fontsize=10),AtomSelectionSpec(elem="C"))
a.add.Line(LineSpec(Vector3(0,5,0),Vector3(5,5,0)))
a.set.Style({}, {"sphere":{}})
a.show()
```
![img.png](img.png)
```python
from easy3dmol import view,AtomSpec,AtomStyleSpec,CartoonStyleSpec

pdb=open("test.pdb","r").read()
v=view()
v.add.Model(pdb,"pdb")
v.set.Style(AtomSpec(),AtomStyleSpec(cartoon=CartoonStyleSpec()))
v.show()
```
![img_1.png](img_1.png)
# Current Tested GLViewer API
## dipaly methods
1. show(): Ipyhon html show()
2. js(): returned js string
## general viewer methods
1. clear
2. render
3. zoom
4. zoomto
## subclass `add`
This subclass is used to **add** any elements on viewer!
## subclass `remove`
## subclass `set`
## subclass `get`
## subclass `anminate`

# type
## Object
## enum & constant
## type dict


