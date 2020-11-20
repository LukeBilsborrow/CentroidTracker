from scipy import spatial
from collections import OrderedDict
import numpy as np

coords = (int, int)
class CentroidTracker():
    def __init__(self, max_disappeared=50):
        self.max_disappeared = max_disappeared
        self.current_id = 0

        self.object_ids = []
        self.objects = OrderedDict()
        self.objects_bb = OrderedDict()
        self.disappeared = OrderedDict()

    def get_new_id(self):
        new_id = self.current_id
        self.current_id += 1
        return new_id
    
    def register(self, coords: coords):
        new_id = self.get_new_id()
        self.objects_bb[new_id] = coords
        self.objects[new_id] = self.get_center(coords)
        self.disappeared[new_id] = 0

    def deregister(self, id):
        del self.objects[id]
        del self.disappeared[id]

    def get_center(self, bbox):
        startX, startY, endX, endY = bbox
        cX = int((startX + endX) / 2.0)
        cY = int((startY + endY) / 2.0)
        return (cX, cY)

    def update(self, bbox_data):
        # if we detected no objects, increase the disappeared count of all of our objects
        if len(bbox_data) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1

                if self.disappeared[object_id] == self.max_disappeared:
                    self.deregister(object_id)
            return list(self.objects_bb.items())

        inputCentroids = np.zeros((len(bbox_data), 2), dtype="int")
        # loop over the bounding box rectangles
        for (i, (startX, startY, endX, endY)) in enumerate(bbox_data):
            # use the bounding box coordinates to derive the centroid
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)

        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(bbox_data[i])
        
        else:
            object_ids = list(self.objects.keys())
            objectCentroids = list(self.objects.values())

            #calculate the distances between the objects we already know and the new objects
            dists = spatial.distance.cdist(np.array(objectCentroids), inputCentroids)
            row_indexes = dists.min(axis=1).argsort()

            col_indexes = dists.argmin(axis=1)[row_indexes]
            usedRows = set()
            usedCols = set()
            # loop over the combination of the (row, column) index
            # tuples
            for (row, col) in zip(row_indexes, col_indexes):
                # if we have already examined either the row or
                # column value before, ignore it
                # val
                if row in usedRows or col in usedCols:
                    continue
                # otherwise, grab the object ID for the current row,
                # set its new centroid, and reset the disappeared
                # counter
                objectID = object_ids[row]
                self.objects_bb[objectID] = bbox_data[col]
                self.objects[objectID] = inputCentroids[col]
                self.disappeared[objectID] = 0
                # indicate that we have examined each of the row and
                # column indexes, respectively
                usedRows.add(row)
                usedCols.add(col)

            unusedRows = set(range(0, dists.shape[0])).difference(usedRows)
            unusedCols = set(range(0, dists.shape[1])).difference(usedCols)

            if dists.shape[0] >= dists.shape[1]:

                for row in unusedRows:

                    objectID = object_ids[row]
                    self.disappeared[objectID] += 1
                    if self.disappeared[objectID] > self.max_disappeared:
                        self.deregister(objectID)
            else:
                for col in unusedCols:
                    self.register(bbox_data[col])

        return list(self.objects_bb.items())

if __name__ == "__main__":
    sample_data = [
        [[0,0,2,2]],
        [[1,1,3,3]],
        [[1,1,3,3]],
        [[2,2,4,4], [5,5,7,7]],
        [[6,6,8,8], [2,2,5,5]]
    ]
    a = CentroidTracker()
    [print(a.update(x)) for x in sample_data]