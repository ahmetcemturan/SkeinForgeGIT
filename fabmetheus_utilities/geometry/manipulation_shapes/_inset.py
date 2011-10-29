"""
Create inset.

"""

from __future__ import absolute_import
#Init has to be imported first because it has code to workaround the python bug where relative imports don't work if the module is imported as a main module.
import __init__

from fabmetheus_utilities.geometry.creation import lineation
from fabmetheus_utilities.geometry.creation import solid
from fabmetheus_utilities.geometry.geometry_utilities import boolean_geometry
from fabmetheus_utilities.geometry.geometry_utilities import evaluate
from fabmetheus_utilities.geometry.geometry_utilities import matrix
from fabmetheus_utilities.geometry.solids import triangle_mesh
from fabmetheus_utilities.vector3index import Vector3Index
from fabmetheus_utilities import euclidean
from fabmetheus_utilities import intercircle


__author__ = 'Enrique Perez (perez_enrique@yahoo.com)'
__credits__ = 'Art of Illusion <http://www.artofillusion.org/>'
__date__ = '$Date: 2008/02/05 $'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'


globalExecutionOrder = 80


def getManipulatedPaths(close, elementNode, loop, prefix, sideLength):
	"Get inset path."
	radius = lineation.getStrokeRadiusByPrefix(elementNode, prefix)
	return intercircle.getInsetLoopsFromVector3Loop(loop, radius)

def getManipulatedGeometryOutput(elementNode, geometryOutput, prefix):
	'Get inset geometryOutput.'
	copyShallow = elementNode.getCopyShallow()
	solid.processElementNodeByGeometry(copyShallow, geometryOutput)
	targetMatrix = matrix.getBranchMatrixSetElementNode(elementNode)
	matrix.setElementNodeDictionaryMatrix(copyShallow, targetMatrix)
	transformedVertexes = copyShallow.xmlObject.getTransformedVertexes()
	minimumZ = boolean_geometry.getMinimumZ(copyShallow.xmlObject)
	maximumZ = euclidean.getTopPath(transformedVertexes)
	layerThickness = 0.4
	importRadius = 0.36
	zoneArrangement = triangle_mesh.ZoneArrangement(layerThickness, transformedVertexes)
	copyShallow.attributes['visible'] = True
	loopLayers = boolean_geometry.getLoopLayers([copyShallow.xmlObject], importRadius, layerThickness, maximumZ, minimumZ, False, zoneArrangement)
	copyShallow.parentNode.xmlObject.archivableObjects.remove(copyShallow.xmlObject)
	loops = []
	vertexes = []
	for loopLayer in loopLayers:
		vector3Loop = []
		loops.append(vector3Loop)
		for loop in loopLayer.loops[: 1]: # just one for now
			for point in loop:
				vector3Index = Vector3Index(len(vertexes), point.real, point.imag, 2.0 * loopLayer.z)
				print(  len(vertexes))
				vector3Loop.append(vector3Index)
				vertexes.append(vector3Index)
	geometryOutput = triangle_mesh.getPillarOutput(loops)
	print(  minimumZ)
	print(  geometryOutput)
	return geometryOutput

def processElementNode(elementNode):
	"Process the xml element."
	solid.processElementNodeByFunctions(elementNode, getManipulatedGeometryOutput, getManipulatedPaths)
