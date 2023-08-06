from paraview.simple import *
import os
import math
#pylint: skip-file
paraview.simple._DisableFirstRenderCameraReset()

def Load(filename:str):
    """Calls pvpython and displays the file

    Args:
        filename (str): [description]

    Returns:
        (tuple): tuple containing:

            - **Plot3D** (paraview.source): source object for plot3d 
            - **plot3D_Display** (paraview display): this is the display object for the source. Colors and things 
            - **View** (paraview.source): source object for plot3d 

    """
    extension = os.path.basename(filename).split('.')[1]
    plot3D = PLOT3DReader(registrationName=os.path.splitext(filename)[0],
            QFileName='',
            FileName=filename,
            FunctionFileName='')

    # set active source
    SetActiveSource(plot3D)
    # get active view
    View = GetActiveViewOrCreate('RenderView')    
    # show data in view
    plot3D_Display = Show(plot3D, View)
    # trace defaults for the display properties.
    plot3D_Display.Representation = 'Outline'
    plot3D_Display.ColorArrayName = ['POINTS', '']
    plot3D_Display.OSPRayScaleFunction = 'PiecewiseFunction'
    plot3D_Display.SelectOrientationVectors = 'None'
    plot3D_Display.ScaleFactor = 0.5376288175582886
    plot3D_Display.SelectScaleArray = 'None'
    plot3D_Display.GlyphType = 'Arrow'
    plot3D_Display.PolarAxes = 'PolarAxesRepresentation'
    plot3D_Display.ScalarOpacityUnitDistance = 0.11673090489063437

    # reset view to fit data
    View.ResetCamera()
    
    # show color bar/color legend
    ColorBy(plot3D_Display, ('FIELD', 'vtkBlockColors'))
    LUT = GetColorTransferFunction('vtkBlockColors')
    plot3D_Display.SetRepresentationType('Surface With Edges')
    ColorBy(plot3D_Display, ('FIELD', 'Solid Color'))
    HideScalarBarIfNotNeeded(LUT, View) # Change to solid color
    return plot3D,plot3D_Display,View,LUT

def SetCamera(View,position,focalPoint,ViewUp):  
    # current camera placement for renderView1
    View.CameraPosition = position
    View.CameraFocalPoint = focalPoint
    View.CameraViewUp = ViewUp
    View.CameraParallelScale = 3.242501630387953

# Extracts the mesh block
# Block indicies should be an array format
def ExtractBlocks(source,View,BlockIndicies):
    extractBlock1 = ExtractBlock(Input=source)
    extractBlock1.BlockIndices = BlockIndicies
    extractBlock1Display = Show(extractBlock1, View)
    extractBlock1Display.Representation = 'Outline'
    extractBlock1Display.ColorArrayName = ['POINTS', '']
    extractBlock1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    extractBlock1Display.SelectOrientationVectors = 'None'
    extractBlock1Display.ScaleFactor = 0.2489664673805237
    extractBlock1Display.SelectScaleArray = 'None'
    extractBlock1Display.GlyphType = 'Arrow'
    extractBlock1Display.PolarAxes = 'PolarAxesRepresentation'
    extractBlock1Display.ScalarOpacityUnitDistance = 0.07851226208722488
    Hide(source, View)
    SetActiveSource(extractBlock1)
    # set scalar coloring
    ColorBy(extractBlock1Display, ('FIELD', 'vtkBlockColors'))

    # show color bar/color legend
    extractBlock1Display.SetScalarBarVisibility(View, True)

    # show color bar/color legend
    ColorBy(extractBlock1Display, ('FIELD', 'vtkBlockColors'))
    LUT = GetColorTransferFunction('vtkBlockColors')
    extractBlock1Display.SetRepresentationType('Surface With Edges')
    ColorBy(extractBlock1Display, ('FIELD', 'Solid Color'))
    HideScalarBarIfNotNeeded(LUT, View) # Change to solid color
    return extractBlock1,extractBlock1Display,LUT

def ExtractSurface(source,View):
    Hide(source, View)
    extractSubset1 = ExtractSubset(Input=source)    
    SetActiveSource(extractSubset1)
    extractSubset1Display = Show(extractSubset1, View)
    extractSubset1Display.Representation = 'Outline'
    extractSubset1Display.ColorArrayName = ['POINTS', '']
    extractSubset1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    extractSubset1Display.SelectOrientationVectors = 'None'
    extractSubset1Display.ScaleFactor = 0.4354984998703003
    extractSubset1Display.SelectScaleArray = 'None'
    extractSubset1Display.GlyphType = 'Arrow'
    extractSubset1Display.PolarAxes = 'PolarAxesRepresentation'
    extractSubset1Display.ScalarOpacityUnitDistance = 0.3237142687497664
    extractSubset1Display.SetScalarBarVisibility(View, True)

    # show color bar/color legend
    ColorBy(extractSubset1Display, ('FIELD', 'vtkBlockColors'))
    LUT = GetColorTransferFunction('vtkBlockColors')
    extractSubset1Display.SetRepresentationType('Surface With Edges')
    ColorBy(extractSubset1Display, ('FIELD', 'Solid Color'))
    HideScalarBarIfNotNeeded(LUT, View) # Change to solid color
    return extractSubset1,extractSubset1Display,LUT

def ChangeRepresentationMesh(source,sourceDisplay,View,LUT):
    SetActiveSource(source) # set active source
    HideScalarBarIfNotNeeded(LUT, View) # Hide the scalar bar for this color map if no visible data is colored by it.    
    sourceDisplay.SetRepresentationType('Surface With Edges') # set active source
    ColorBy(sourceDisplay, ('FIELD', 'Solid Color'))


def Periodicity(source,nBlades,BlockIndices,View):  
    # hide data in view
    Hide(source, View)
    angularPeriodicFilter1 = AngularPeriodicFilter(Input=source)

    # Properties modified on angularPeriodicFilter1
    angularPeriodicFilter1.BlockIndices = BlockIndices
    angularPeriodicFilter1.IterationMode = 'Manual'
    angularPeriodicFilter1.NumberOfPeriods = 2
    angularPeriodicFilter1.RotationAngle = 360.0/nBlades

    SetActiveSource(angularPeriodicFilter1)
    # get color transfer function/color map for 'Density'
    LUT = GetColorTransferFunction('Density')

    # show data in view
    angularPeriodicFilter1Display = Show(angularPeriodicFilter1, View)
    # trace defaults for the display properties.
    angularPeriodicFilter1Display.Representation = 'Surface'
    angularPeriodicFilter1Display.ColorArrayName = ['POINTS', 'Density']
    angularPeriodicFilter1Display.LookupTable = LUT
    angularPeriodicFilter1Display.OSPRayScaleArray = 'Density'
    angularPeriodicFilter1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    angularPeriodicFilter1Display.SelectOrientationVectors = 'Momentum'
    angularPeriodicFilter1Display.ScaleFactor = 0.6140377521514893
    angularPeriodicFilter1Display.SelectScaleArray = 'Density'
    angularPeriodicFilter1Display.GlyphType = 'Arrow'
    angularPeriodicFilter1Display.PolarAxes = 'PolarAxesRepresentation'
    angularPeriodicFilter1Display.ScalarOpacityUnitDistance = 0.35345957752629076
    # show color bar/color legend
    angularPeriodicFilter1Display.SetScalarBarVisibility(View, True)
    return angularPeriodicFilter1,angularPeriodicFilter1Display,LUT


def CreateNewLayout(source,layoutName):
    CreateLayout(layoutName)

    # Create a new 'Render View'
    renderView2 = CreateView('RenderView')
    #renderView2.ViewSize = [1233, 814]
    renderView2.AxesGrid = 'GridAxes3DActor'
    renderView2.StereoType = 0
    renderView2.Background = [0.32, 0.34, 0.43]
    layout = GetLayout()
    
    # set active source
    if (source):
        SetActiveSource(source)
        # show data in view
        sourceDisplay = Show(source, renderView2)
        # trace defaults for the display properties.
        sourceDisplay.Representation = 'Outline'
        sourceDisplay.ColorArrayName = ['POINTS', '']
        sourceDisplay.OSPRayScaleArray = 'Density'
        sourceDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
        sourceDisplay.SelectOrientationVectors = 'Momentum'
        sourceDisplay.ScaleFactor = 0.5376288175582886
        sourceDisplay.SelectScaleArray = 'Density'
        sourceDisplay.GlyphType = 'Arrow'
        sourceDisplay.PolarAxes = 'PolarAxesRepresentation'
        sourceDisplay.ScalarOpacityUnitDistance = 0.11673090489063437
        # reset view to fit data
        renderView2.ResetCamera()
        return layout,sourceDisplay,renderView2
    
    return layout,renderView2