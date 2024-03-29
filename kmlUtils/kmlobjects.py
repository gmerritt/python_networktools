__author__ = 'leahanderson'

from xml.dom.minidom import getDOMImplementation

ALT_CLAMPED  = "clampedToGround"
ALT_RELATIVE = "relativeToGround"
ALT_ABSOLUTE = "absolute"


class KML:

    def __init__(self, comment=None):
        impl = getDOMImplementation()
        self.xml = impl.createDocument(None, "kml", None)
        self.root = self.xml.documentElement
        self.root.setAttribute("xmlns", "http://earth.google.com/kml/2.1")
        if comment:
            self.root.appendChild(self.xml.createComment(comment))
        # dirty subclassing ;-)
        def __getattr__(self, name):
            if not hasattr(self.root, name):
                raise AttributeError, "%s instance has no attribute '%s'" %\
                                (self.__class__.__name__, name)
            else:
                return getattr(self.root, name)

    def createDocument(self, name, desc=None, visible=True):
        doc = self.xml.createElement("Document")
        nm = self.xml.createElement('name')
        nm.appendChild(self.xml.createTextNode(name))
        doc.appendChild(nm)
        if desc:
            elt = self.xml.createElement('description')
            elt.appendChild(self.xml.createCDATASection(desc))
            doc.appendChild(elt)
        if not visible:
            elt = self.xml.createElement('visibility')
            elt.appendChild(self.xml.createTextNode("0"))
            doc.appendChild(elt)
        return doc

    def createIcon(self, iconUrl=None, x=None, y=None, w=None, h=None, dim=None):
        icon = self.xml.createElement("Icon")
        if iconUrl is not None:
            url = self.xml.createElement("href")
            url.appendChild(self.xml.createTextNode(iconUrl))
            icon.appendChild(url)
        if dim:
            dimensions=dim
        else:
            dimensions = [ ('x', x), ('y', y), ('w', w), ('h', h) ]
        for d in dimensions:
            if d[1] is not None:
                elt = self.xml.createElement(d[0])
                elt.appendChild(self.xml.createTextNode(`d[1]`))
                icon.appendChild(elt)
        return icon

    def createIconStyle(self, scale=None, icon=None, color=None):
        istyle = self.xml.createElement("IconStyle")
        if scale is not None:
            elt = self.xml.createElement("scale")
            elt.appendChild(self.xml.createTextNode(`scale`))
            istyle.appendChild(elt)
        if icon is not None:
            istyle.appendChild(icon)
        if color:
            elt = self.xml.createElement("color")
            elt.appendChild(self.xml.createTextNode(color))
            istyle.appendChild(elt)
        return istyle

    def createLabelStyle(self, scale=None, color=None, colorMode=None):
        lstyle = self.xml.createElement("LabelStyle")
        if scale is not None:
            elt = self.xml.createElement("scale")
            elt.appendChild(self.xml.createTextNode(`scale`))
            lstyle.appendChild(elt)
        if color:
            elt = self.xml.createElement("color")
            elt.appendChild(self.xml.createTextNode(color))
            lstyle.appendChild(elt)
        if colorMode:
            elt = self.xml.createElement("colorMode")
            elt.appendChild(self.xml.createTextNode(colorMode))
            lstyle.appendChild(elt)
        return lstyle

    def createPolyStyle(self, color=None, outline=True):
        pstyle = self.xml.createElement("PolyStyle")
        if color:
            elt = self.xml.createElement("color")
            elt.appendChild(self.xml.createTextNode(color))
            pstyle.appendChild(elt)
        if not outline:
            elt = self.xml.createElement("outline")
            elt.appendChild(self.xml.createTextNode("0"))
            pstyle.appendChild(elt)
        return pstyle

    def createLineStyle(self, color=None, width=None):
        lstyle = self.xml.createElement("LineStyle")
        if color:
            elt = self.xml.createElement("color")
            elt.appendChild(self.xml.createTextNode(color))
            lstyle.appendChild(elt)
        if width is not None:
            elt = self.xml.createElement("width")
            elt.appendChild(self.xml.createTextNode("%f" % width))
            lstyle.appendChild(elt)
        return lstyle

    def createBalloonStyle(self, text, color=None):
        bstyle = self.xml.createElement("BalloonStyle")
        elt = self.xml.createElement("text")
        elt.appendChild(self.xml.createCDATASection(text))
        bstyle.appendChild(elt)
        if color:
            elt = self.xml.createElement("color")
            elt.appendChild(self.xml.createTextNode(color))
            bstyle.appendChild(elt)
        return bstyle

    def createStyle(self, id=None, children=None):
        style = self.xml.createElement("Style")
        if id:
            style.setAttribute("id", id)
        if children:
            if type(children) == list:
                [style.appendChild(c) for c in children]
            else:
                style.appendChild(children)
        return style

    def createLookAt(self, lat, lon,  range=None, tilt=None, heading=None):
        pt = self.xml.createElement("LookAt")
        elt = self.xml.createElement("longitude")
        elt.appendChild(self.xml.createTextNode("%f" % lon))
        pt.appendChild(elt)
        elt = self.xml.createElement("latitude")
        elt.appendChild(self.xml.createTextNode("%f" % lat))
        pt.appendChild(elt)
        if range is not None:
            elt = self.xml.createElement("range")
            elt.appendChild(self.xml.createTextNode(`range`))
            pt.appendChild(elt)
        if tilt is not None:
            elt = self.xml.createElement("tilt")
            elt.appendChild(self.xml.createTextNode(`tilt`))
            pt.appendChild(elt)
        if heading is not None:
            elt = self.xml.createElement("heading")
            elt.appendChild(self.xml.createTextNode(`heading`))
            pt.appendChild(elt)
        return pt

    def createFolder(self, name, isOpen=False):
        fld = self.xml.createElement("Folder")
        elt = self.xml.createElement("name")
        elt.appendChild(self.xml.createTextNode(name))
        fld.appendChild(elt)
        if isOpen:
            elt = self.xml.createElement("open")
            elt.appendChild(self.xml.createTextNode("1"))
            fld.appendChild(elt)
        return fld

    def createPlacemark(self, name, lat=None, lon=None, desc=None, style=None, range=None, tilt=None, alt=None,
                         heading=None, visible=True, altMode=None, timeStamp=None, timeSpan=None):
        pm = self.xml.createElement("Placemark")
        elt = self.xml.createElement("name")
        elt.appendChild(self.xml.createTextNode(name))
        pm.appendChild(elt)
        if lat is not None and lon is not None:
            pt = self.xml.createElement("Point")
            elt = self.xml.createElement("coordinates")
            coor = "%f,%f" % (lon, lat)
            if alt is not None: coor += ",%f" % alt
            elt.appendChild(self.xml.createTextNode(coor))
            pt.appendChild(elt)
            if altMode:
                elt = self.xml.createElement("altitudeMode")
                elt.appendChild(self.xml.createTextNode(altMode))
                pt.appendChild(elt)
            pm.appendChild(pt)
        if range or tilt:
            pm.appendChild(self.createLookAt(lat, lon, range, tilt, heading))
        if style:
            if type(style) == str or type(style) == unicode:
                elt = self.xml.createElement("styleUrl")
                elt.appendChild(self.xml.createTextNode(style))
                pm.appendChild(elt)
            else:
                pm.appendChild(style)
        if desc:
            elt = self.xml.createElement("description")
            elt.appendChild(self.xml.createCDATASection(desc))
            pm.appendChild(elt)
        if not visible:
            elt = self.xml.createElement("visibility")
            elt.appendChild(self.xml.createTextNode("0"))
            pm.appendChild(elt)
        if timeStamp:
            pm.appendChild(self.createTimeStamp(timeStamp))
        if timeSpan:
            pm.appendChild(self.createTimeSpan(timeSpan))
        return pm

    def createTimeStamp(self, dt, tz="Z"):
        ts = self.xml.createElement("TimeStamp")
        wh = self.xml.createElement("when")
        wh.appendChild(self.xml.createTextNode(dt.strftime("%Y-%m-%dT%H:%M:%S") + tz))
        ts.appendChild(wh)
        return ts

    def createTimeSpan(self, dt, tz="Z"):
        ts = self.xml.createElement("TimeSpan")
        beg = self.xml.createElement("begin")
        beg.appendChild(self.xml.createTextNode(dt["begin"].strftime("%Y-%m-%dT%H:%M:%S") + tz))
        ts.appendChild(beg)
        end = self.xml.createElement("end")
        end.appendChild(self.xml.createTextNode(dt["end"].strftime("%Y-%m-%dT%H:%M:%S") + tz))
        ts.appendChild(end)
        return ts

    def createMultiGeometry(self):
        return self.xml.createElement("MultiGeometry")

    def createLineString(self, coords, altMode=None, tessel=False, extrude=False):
        ls = self.xml.createElement("LineString")
        if tessel:
            elt = self.xml.createElement("tesselate")
            elt.appendChild(self.xml.createTextNode("1"))
            ls.appendChild(elt)
        if extrude:
            elt = self.xml.createElement("extrude")
            elt.appendChild(self.xml.createTextNode("1"))
            ls.appendChild(elt)
        if altMode:
            elt = self.xml.createElement("altitudeMode")
            elt.appendChild(self.xml.createTextNode(altMode))
            ls.appendChild(elt)
        elt = self.xml.createElement("coordinates")
        coo = ""
        for c in coords:
            coo += "%f,%f,%f " % (c[1], c[0], c[2])
        elt.appendChild(self.xml.createTextNode(coo))
        ls.appendChild(elt)
        return ls

    def createLink(self, url, refreshMode=None, refreshInterval=None): # TODO: all view... elts
        # This is KML 2.1 / GoogleEarth > 4.x
        ln = self.xml.createElement("Link")
        elt = self.xml.createElement("href")
        elt.appendChild(self.xml.createTextNode(url))
        ln.appendChild(elt)
        if refreshMode is not None:
            if not refreshMode in [ "onChange", "onInterval", "onExpire" ]:
                raise ValueError("Invalid refresh mode '%s'" % refreshMode)
            elt = self.xml.createElement("refreshMode")
            elt.appendChild(self.xml.createTextNode(refreshMode))
            ln.appendChild(elt)
        if refreshInterval is not None:
            elt = self.xml.createElement("refreshInterval")
            elt.appendChild(self.xml.createTextNode(str(refreshInterval)))
            ln.appendChild(elt)
        return ln

    def createNetworkLink(self, url, name=None, desc=None, visible=True, isOpen=True,
                            refreshMode=None, refreshInterval=None): # TODO: all view... elts
        nl = self.xml.createElement("NetworkLink")
        ln = self.createLink(url, refreshMode, refreshInterval)
        nl.appendChild(ln)
        if name is not None:
            elt = self.xml.createElement("name")
            elt.appendChild(self.xml.createTextNode(name))
            nl.appendChild(elt)
        if desc is not None:
            elt = self.xml.createElement("description")
            elt.appendChild(self.xml.createCDATASection(desc))
            nl.appendChild(elt)
        if not visible:
            elt = self.xml.createElement("visibility")
            elt.appendChild(self.xml.createTextNode("0"))
            nl.appendChild(elt)
        if isOpen:
            elt = self.xml.createElement("open")
            elt.appendChild(self.xml.createTextNode("1"))
            nl.appendChild(elt)
        return nl

    def createNetworkLinkControl(self, name=None, desc=None, refresh=None, msg=None, cookie=None):
        nlc = self.xml.createElement("NetworkLinkControl")
        if name is not None:
            elt = self.xml.createElement("linkName")
            elt.appendChild(self.xml.createTextNode(name))
            nlc.appendChild(elt)
        if desc is not None:
            elt = self.xml.createElement("linkDescription")
            elt.appendChild(self.xml.createCDATASection(desc))
            nlc.appendChild(elt)
        if refresh is not None:
            elt = self.xml.createElement("minRefreshPeriod")
            elt.appendChild(self.xml.createTextNode("%d" % refresh))
            nlc.appendChild(elt)
        if msg is not None:
            elt = self.xml.createElement("message")
            elt.appendChild(self.xml.createTextNode(msg))
            nlc.appendChild(elt)
        if cookie is not None:
            elt = self.xml.createElement("cookie")
            elt.appendChild(self.xml.createTextNode(cookie))
            nlc.appendChild(elt)
        return nlc

    def writePlain(self, f):
        print self.xml
        self.xml.writexml(f, '    ' ,'    ', '\n')

    def display(self):
        self.xml.toxml()

