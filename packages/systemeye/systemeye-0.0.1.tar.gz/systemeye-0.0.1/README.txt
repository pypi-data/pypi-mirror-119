# *IMPORTING PACKAGE AND MODULE <br />
## *syntax* <br />
*from buildingblocks import bb*  <br /> <br />

# *INTERPOLATE in ONE STEP*  <br />
## *syntax* <br />
**Ynew = bb.interpolate(Xdata, Ydata, Xnew, iter)** <br /><br />

## **Description:** Given (Xdata and Ydata) data is used to build a model. Xdata and Ydata are the first two arguments to the function *interpolate*.<br /> 
The third argument Xnew is the x-axis values of the interpolated data that the user wishes to have. <br /> 
The function returns Ynew for the given Xnew. *iter* is number of iterations given by the user (between 1 and 150)<br /> <br />

## *Example*<br />
import matplotlib.pyplot as plt<br />
import numpy as np<br />
from buildingblocks import bb<br /><br />

Xdata=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]<br />
Ydata=[2.841, 3.909, 4.141, 4.243, 5.041, 6.720, 8.656, 9.989, 10.412, 10.455, 11.000, 12.463, 14.420, 15.990, 16.650, 16.712, 17.038, 18.249, 20.149, 21.9129]<br />
Xnew=list(np.linspace(1, 20,191))<br /><br />


Ynew=bb.interpolate(Xdata,Ydata,Xnew,40)<br />
plt.figure()<br />
plt.plot(Xdata,Ydata,'*')<br />
plt.plot(Xnew,Ynew)<br /><br />

# *INTERPOLATE in TWO STEPS and use the Model* <br />
## *syntax*<br />
**ParameterSet=buildmodel(Xdata,Ydata,40)**<br />
**Ynew=usemodel(Xnew,ParameterSet)**<br /><br />

## **Description:** Given (Xdata and Ydata) data is used to build a model. Xdata and Ydata are the first two arguments to the function *buildmodel*.<br /> 
Its returns a set of parameters *ParameterSet* and this is passed to *usemodel* to predict the required Ynew using *usemodel* with Xnew as argument. <br /> 
*iter* is number of iterations given by the user (between 1 and 150)<br /> <br />

## *Example*<br />
import matplotlib.pyplot as plt<br />
import numpy as np<br />
from buildingblocks import bb <br /><br />

Xdata=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]<br />
Ydata=[2.841, 3.909, 4.141, 4.243, 5.041, 6.720, 8.656, 9.989, 10.412, 10.455, 11.000, 12.463, 14.420, 15.990, 16.650, 16.712, 17.038, 18.249, 20.149, 21.9129]<br />
Xnew=list(np.linspace(1, 20,191))<br /><br />


ParaSet=buildmodel(Xdata,Ydata,40)<br />
Ynew=usemodel(Xnew,ParaSet)<br /><br /><br />

plt.figure()<br />
plt.plot(Xdata,Ydata,'*')<br />
plt.plot(Xnew,Ynew)<br /><br />



