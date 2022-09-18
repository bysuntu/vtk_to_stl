import vtk
import numpy as np

def stlTri(tri, normal, handle):
    handle.write('facet normal {} {} {}\n'.format(normal[0], normal[1], normal[2]))
    handle.write('  outer loop\n')
    for p in tri:
        handle.write('      vertex {} {} {}\n'.format(p[0], p[1], p[2]))
    handle.write('  endloop\n')
    handle.write('endfacet\n')


def calNormal(points):
    assert len(points) == 3
    edge0 = points[0] - points[1]
    edge1 = points[1] - points[2]
    normal = np.cross(edge0, edge1)
    normal = normal / np.linalg.norm(normal)
    return normal


def vtk_to_stl(polydata, stlname):
    with open(stlname, 'w') as f:
        f.write('solid vtk2stl\n')
        for k in range(polydata.GetNumberOfCells()):
            cur = polydata.GetCell(k)
            points = []
            for p in range(cur.GetNumberOfPoints()):
                points.append(list(cur.GetPoints().GetPoint(p)))
            if len(points) == 3:
                pts = np.array(points)
                normal = calNormal(pts)
                stlTri(pts, normal, f)
            else:
                center = np.mean(points, axis = 0)
                for n in range(len(points)):
                    p0 = points[n]
                    p1 = points[(n + 1) % len(points)]
                    pts = np.array([p0, center, p1])
                    normal = calNormal(pts)
                    stlTri(pts, normal, f)
        f.write('endsolid vtk2stl\n')

    print(polydata.GetNumberOfCells())


def readVTKPolyData(vtkname):
    with open(vtkname, 'r') as f:
        for k in range(4):
            line = f.readline()
            if line.find('DATASET') >= 0:
                _, fType = line[:-1].split(' ')
    if fType == 'POLYDATA':
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(vtkname)
        reader.Update()
        polydata = reader.GetOutput()
        return polydata
    elif fType == 'UNSTRUCTURED_GRID':
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(vtkname)
        reader.Update()
        unstructured = reader.GetOutput()
        return unstructured
    else:
        raise TypeError("Wrong VTK File Type: {}".format(fType))

polydata = readVTKPolyData('sideHole.vtk')
vtk_to_stl(polydata, 'sideHole.stl')
