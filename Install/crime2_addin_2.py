import arcpy
import pythonaddins
import os

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

def returnLayer(layername):
    mxd = arcpy.mapping.MapDocument('CURRENT')
    layers = arcpy.mapping.ListLayers(mxd)
    for layer in layers:
        if layer.name.upper() == layername.upper():
            return layer
        
def CreateGrid(featureClass,GridSize,output):
    desc = arcpy.Describe(featureClass)
    try:
        newGrid =arcpy.InsertCursor(output)
    except:
        arcpy.CreateFeatureclass_management(os.path.split(output)[0],os.path.split(output)[1],'POLYGON')
        print arcpy.GetMessages()
        newGrid = arcpy.InsertCursor(output)
    
    XStart = desc.extent.XMin
    XMin = desc.extent.XMin
    YMin = desc.extent.YMin
    
    for ycoord in range(int(desc.extent.YMin+GridSize),int(desc.extent.YMax+GridSize),GridSize):
        XMin = XStart
        for xcoord in range(int(desc.extent.XMin+GridSize),int(desc.extent.XMax+GridSize),GridSize):
            newPolygon = newGrid.newRow()
            pointList = [arcpy.Point(XMin,YMin),
                         arcpy.Point(xcoord,YMin),
                         arcpy.Point(xcoord,ycoord),
                         arcpy.Point(XMin,ycoord)]
            polyArray = arcpy.Array(pointList)
            polygon = arcpy.Polygon(polyArray)
            newPolygon.Shape = polygon
            newGrid.insertRow(newPolygon)
    
            XMin = xcoord
        YMin = ycoord
    del newGrid
    del polygon

class Assault_Type(object):
    """Implementation for crime2_addin.asType (ComboBox)"""
    def __init__(self):
        self.items = ["item1", "item2"]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWWWWWWWWW'
        self.width = 'WWWWWW'
        mxd = arcpy.mapping.MapDocument('CURRENT')
        layers = arcpy.mapping.ListLayers(mxd)
        self.items = []
        for layer in layers:
            if layer.name == 'Assault':
                self.items = unique_values(layer, 'Assault_Ty')
                self.items.append('<Clear>')
    def onSelChange(self, selection):
        mxd = arcpy.mapping.MapDocument('CURRENT')
        layers = arcpy.mapping.ListLayers(mxd)
        for layer in layers:
            if layer.name == 'Assault' or layer.name == '<Clear>':
                if layer.name <> '<Clear>':
                    query = "ASSAULT_TY = '" + selection + "'"
                    arcpy.management.SelectLayerByAttribute(layer,"NEW_SELECTION",query)
                    arcpy.mapping.ListDataFrames(mxd)[0].extent = layer.getSelectedExtent()
                else:
                    arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")                
                df = arcpy.mapping.ListDataFrames(mxd)[0]
                df.zoomToSelectedFeatures()                
                arcpy.RefreshActiveView()
    
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass    

class Buffer_1000(object):
    """Implementation for crime2_addin.buf1000 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        outputbuffer = 'c:\\temp\\output.shp'
        if arcpy.Exists(outputbuffer):
            arcpy.Delete_management(outputbuffer)
        try:
            arcpy.Buffer_analysis(returnLayer('Assault'), outputbuffer , "1000 Meters")
        except:
            text = arcpy.GetMessages(2)
            pythonaddins.MessageBox(text,'Error performing buffer')
            arcpy.RefreshActiveView()

class Buffer_1500(object):
    """Implementation for crime2_addin.buf1500 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        outputbuffer = 'c:\\temp\\output.shp'
        if arcpy.Exists(outputbuffer):
            arcpy.Delete_management(outputbuffer)
        try:
            arcpy.Buffer_analysis(returnLayer('Assault'), outputbuffer , "1500 Meters")
        except:
            text = arcpy.GetMessages(2)
            pythonaddins.MessageBox(text,'Error performing buffer')
            arcpy.RefreshActiveView()

class Buffer_500(object):
    """Implementation for crime2_addin.buf500 (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        outputbuffer = 'c:\\temp\\output.shp'
        if arcpy.Exists(outputbuffer):
            arcpy.Delete_management(outputbuffer)
        try:
            arcpy.Buffer_analysis(returnLayer('Assault'), outputbuffer , "500 Meters")
        except:
            text = arcpy.GetMessages(2)
            pythonaddins.MessageBox(text,'Error performing buffer')
            arcpy.RefreshActiveView()

class Count_Crimes(object):
    """Implementation for crime2_addin.cntCrimes (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        layer = returnLayer('Assault')
        count = int(arcpy.GetCount_management(layer).getOutput(0))
        pythonaddins.MessageBox('There are ' + str(count) + ' crimes in the selected area','Count Crimes')

class Overlay_Grid(object):
    """Implementation for crime2_addin.overlayGrid (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        try:
            CreateGrid(returnLayer('Precincts'),1000,'c:/temp/grid_output.shp')
        except:
            text = arcpy.GetMessages(2)
            pythonaddins.MessageBox(text,'Error creating grid')

class PrecinctID(object):
    """Implementation for crime2_addin.precinctId (ComboBox)"""
    def __init__(self):
        self.items = ["item1", "item2"]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        mxd = arcpy.mapping.MapDocument('CURRENT')
        layers = arcpy.mapping.ListLayers(mxd)
        self.items = []
        for layer in layers:
            if layer.name == 'Precincts':
                self.items = unique_values(layer, 'Precinct')
                self.items.append('<Clear>')
    def onSelChange(self, selection):
        mxd = arcpy.mapping.MapDocument('CURRENT')
        layers = arcpy.mapping.ListLayers(mxd)
        for layer in layers:
            if layer.name == 'Assault' or layer.name == '<Clear>':
                if layer.name <> '<Clear>':
                    query = "PRECINCT = '" + selection + "'"
                    arcpy.management.SelectLayerByAttribute(layer,"NEW_SELECTION",query)
                    arcpy.mapping.ListDataFrames(mxd)[0].extent = layer.getSelectedExtent()
                else:
                    arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")                
                df = arcpy.mapping.ListDataFrames(mxd)[0]
                df.zoomToSelectedFeatures()                
                arcpy.RefreshActiveView()
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass

class Select_Point(object):
    """Implementation for crime2_addin.selPoint (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        
        self.x = x
        self.y = y
        layer = returnLayer('Assault')
        in_layer=arcpy.PointGeometry(arcpy.Point(x, y))
        arcpy.SelectLayerByLocation_management(in_layer, layer, "NEW_SELECTION")
        
    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        pass
    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        pass
    def onRectangle(self, rectangle_geometry):
        pass

class Select_Rect(object):
    """Implementation for crime2_addin.selRect (Tool)"""
    def __init__(self):
        self.enabled = True
        self.cursor = 3
        self.shape = "Rectangle" # Can set to "Line", "Circle" or "Rectangle" for interactive shape drawing and to activate the onLine/Polygon/Circle event sinks.
    def onMouseDown(self, x, y, button, shift):
        pass
    def onMouseDownMap(self, x, y, button, shift):
        pass
    def onMouseUp(self, x, y, button, shift):
        pass
    def onMouseUpMap(self, x, y, button, shift):
        pass
    def onMouseMove(self, x, y, button, shift):
        pass
    def onMouseMoveMap(self, x, y, button, shift):
        pass
    def onDblClick(self):
        pass
    def onKeyDown(self, keycode, shift):
        pass
    def onKeyUp(self, keycode, shift):
        pass
    def deactivate(self):
        pass
    def onCircle(self, circle_geometry):
        pass
    def onLine(self, line_geometry):
        pass
    def onRectangle(self, rectangle_geometry):
        """Occurs when the rectangle is drawn and the mouse button is released.  
        The rectangle is a extent object."""  
  
        extent = rectangle_geometry
        mxd = arcpy.mapping.MapDocument('CURRENT')  
        df = mxd.activeDataFrame  
        ext = df.extent    
        layer = returnLayer('Assault')  
         
        a = arcpy.Array()  
        a.add(ext.lowerLeft)  
        a.add(ext.lowerRight)  
        a.add(ext.upperRight)  
        a.add(ext.upperLeft)  
        a.add(ext.lowerLeft)  
        thepoly = arcpy.Polygon(a)  
         
        arcpy.SelectLayerByLocation_management(layer, "WITHIN", thepoly, 0, "NEW_SELECTION")

class Time_Day(object):
    """Implementation for crime2_addin.timeDay (ComboBox)"""
    def __init__(self):
        self.items = ["item1", "item2"]
        self.editable = True
        self.enabled = True
        self.dropdownWidth = 'WWWWWW'
        self.width = 'WWWWWW'
        mxd = arcpy.mapping.MapDocument('CURRENT')
        layers = arcpy.mapping.ListLayers(mxd)
        self.items = []
        for layer in layers:
            if layer.name == 'Assault':
                pythonaddins.MessageBox('test','test')
                self.items = unique_values(layer, 'TimeofDay')
                self.items.append('<Clear>')
    def onSelChange(self, selection):
        mxd = arcpy.mapping.MapDocument('CURRENT')
        layers = arcpy.mapping.ListLayers(mxd)
        for layer in layers:
            if layer.name == 'Assault' or layer.name == '<Clear>':
                if layer.name <> '<Clear>':
                    query = "TIMEOFDAY = '" + selection + "'"
                    arcpy.management.SelectLayerByAttribute(layer,"NEW_SELECTION",query)
                    arcpy.mapping.ListDataFrames(mxd)[0].extent = layer.getSelectedExtent()
                else:
                    arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")                
                df = arcpy.mapping.ListDataFrames(mxd)[0]
                df.zoomToSelectedFeatures()                
                arcpy.RefreshActiveView()
                
    def onEditChange(self, text):
        pass
    def onFocus(self, focused):
        pass
    def onEnter(self):
        pass
    def refresh(self):
        pass    