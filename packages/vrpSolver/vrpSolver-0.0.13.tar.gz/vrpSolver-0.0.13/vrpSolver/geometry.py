import math
import heapq

from .const import *
from .common import *

def getSweepSeq(
    nodes:      "Dictionary, returns the coordinate of given nodeID, \
                    {\
                        nodeID1: {'loc': (x, y)}, \
                        nodeID2: {'loc': (x, y)}, \
                        ... \
                    }" = None,
    excludeIDs: "List of nodeIDs that will be excluded in sweeping, usually includes depot" = [],
    centerLoc:  "List, [x, y], the center point" = None,
    isClockwise: "True if the sweeping direction is clock-wise, False otherwise" = True,
    initDeg:    "Starting direction of the sweeping, 0 as North" = 0
    ) -> "Given a set of locations, and a center point, gets the sequence from sweeping":

    # Initialize heap =========================================================
    degHeap = []
    centerLocNodes = []
    
    # Build heap ==============================================================
    for nodeID in nodes:
        if (nodeID not in excludeIDs):
            dist = distEuclidean2D(nodes[nodeID]['loc'], centerLoc)
            # If the nodes are too close, separate it/them
            if (dist <= CONST_EPSILON):
                centerLocNodes.append(nodeID)
            else:
                dx = nodes[nodeID]['loc'][0] - centerLoc[0]
                dy = nodes[nodeID]['loc'][1] - centerLoc[1]
                (_, deg) = vec2ValDeg([dx, dy])
                # Calculate angles
                evalDeg = None
                if (isClockwise):
                    evalDeg = deg - initDeg
                else:
                    evalDeg = initDeg - deg
                while(evalDeg > 360):
                    evalDeg -= 360
                while(evalDeg < 0):
                    evalDeg += 360
                heapq.heappush(degHeap, (evalDeg, nodeID))

    # Sweep ===================================================================
    sweepSeq = []
    while (len(degHeap)):
        sweepSeq.append(heapq.heappop(degHeap)[1])
    sweepSeq.extend(centerLocNodes)

    return sweepSeq

def seqCutSharpEar(
    nodes:      "Dictionary, returns the coordinate of given nodeID, \
                    {\
                        nodeID1: {'loc': (x, y)}, \
                        nodeID2: {'loc': (x, y)}, \
                        ... \
                    }" = None, 
    seq:        "A sequence of nodeIDs" = None,
    ) -> "Given a sequence of nodes, cut the 'sharp ears' of the sequence":
    cut = [seq[0]]
    for i in range(1, len(seq) - 1):
        vec1 = [nodes[seq[i - 1]]['loc'][0] - nodes[seq[i]]['loc'][0], nodes[seq[i - 1]]['loc'][1] - nodes[seq[i]]['loc'][1]]
        vec2 = [nodes[seq[i + 1]]['loc'][0] - nodes[seq[i]]['loc'][0], nodes[seq[i + 1]]['loc'][1] - nodes[seq[i]]['loc'][1]]
        cosAngle = (vec1[0] * vec2[0] + vec1[1] * vec2[1]) / (math.sqrt(vec1[0] * vec1[0] + vec1[1] * vec1[1]) * math.sqrt(vec2[0] * vec2[0] + vec2[1] * vec2[1]))
        if (cosAngle <= 0.5):
            cut.append(seq[i])
    cut.append(seq[-1])
    return cut

def getNodesConvexHull(
    nodes:      "Dictionary, returns the coordinate of given nodeID, \
                    {\
                        nodeID1: {'loc': (x, y)}, \
                        nodeID2: {'loc': (x, y)}, \
                        ... \
                    }" = None,
    algo:       "1) String, 'Jarvis', O(nH) (current implementation is O(nHlog n)) or\
                 2) String, (not available) 'DNC', O(nlog n) or\
                 3) String, (not available) 'Graham', O(nlog n) or\
                 4) String, (not available) 'Melkman'" = "Jarvis"
    ) -> "Given a set of node locations, return a list of nodeID which construct the convex hull":

    # Initialize ==============================================================
    chSeq = None

    # Some extreme cases ======================================================
    if (len(nodes) == 0):
        return None
    elif (len(nodes) <= 3):
        chSeq = []
        for n in nodes:
            chSeq.append(n)
        return chSeq

    # Call subroutines ========================================================
    if (algo == "Jarvis"):
        chSeq = _getNodesConvexHullJavis(nodes)
    else:
        return None
    
    return chSeq

def _getNodesConvexHullJavis(nodes):
    # References ==============================================================
    # 1. https://blog.csdn.net/Bone_ACE/article/details/46239187
    # 2. chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/viewer.html?pdfurl=http%3A%2F%2Fwww.ams.sunysb.edu%2F~jsbm%2Fcourses%2F345%2F13%2Fmelkman.pdf&clen=46562&chunk=true
    # 3. https://en.wikipedia.org/wiki/Convex_hull_algorithms

    # Initialize ==============================================================
    chSeq = []

    # Get the location of the left-most nodeID ================================
    # Find an initial point which guaranteed to be in convex hull
    leftMostID = None
    leftMostX = None
    for n in nodes:
        if (leftMostID == None or nodes[n]['loc'][0] < leftMostX):
            leftMostID = n
            leftMostX = nodes[n]['loc'][0]

    # Jarvis march ============================================================
    curNodeID = leftMostID
    curDirection = 0
    marchFlag = True
    while (marchFlag):
        sweepSeq = getSweepSeq(
            nodes = nodes,
            excludeIDs = chSeq,
            centerLoc = nodes[curNodeID]['loc'],
            initDeg = curDirection)
        if (sweepSeq[0] == leftMostID):
            marchFlag = False
        chSeq.append(sweepSeq[0])
        curDirection = getHeadingXY(nodes[curNodeID]['loc'], nodes[sweepSeq[0]]['loc'])    
        curNodeID = sweepSeq[0]

    return chSeq