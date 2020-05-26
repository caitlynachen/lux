from lux.vizLib.altair.AltairRenderer import AltairRenderer
from lux.utils.utils import checkImportLuxWidget
class ViewCollection():
	'''
	ViewCollection is a list of View objects. 
	'''
	def __init__(self,collection):
		self.collection=collection

	def __getitem__(self, key):
		return self.collection[key]
	def __setitem__(self, key, value):
		self.collection[key] = value
	def __len__(self):
		return len(self.collection)
	def __repr__(self):
		return f"<ViewCollection: {str(self.collection)}>"

	def map(self,function):
		# generalized way of applying a function to each element
		return map(function, self.collection)
	
	def get(self,fieldName):
		# Get the value of the field for all objects in the collection
		def getField(dObj):
			fieldVal = getattr(dObj,fieldName)
			# Might want to write catch error if key not in field
			return fieldVal
		return self.map(getField)

	def set(self,fieldName,fieldVal):
		return NotImplemented

	def sort(self, removeInvalid=True, descending = True):
		# remove the items that have invalid (-1) score
		if (removeInvalid): self.collection = list(filter(lambda x: x.score!=-1,self.collection))
		# sort in-place by “score” by default if available, otherwise user-specified field to sort by
		self.collection.sort(key=lambda x: x.score, reverse=descending)

	def topK(self,k):
		#sort and truncate list to first K items
		self.sort()
		return ViewCollection(self.collection[:k])
	def bottomK(self,k):
		#sort and truncate list to first K items
		self.sort(descending=False)
		return ViewCollection(self.collection[:k])
	def normalizeScore(self, invertOrder = False):
		maxScore = max(list(self.get("score")))
		for dobj in self.collection:
			dobj.score = dobj.score/maxScore
			if (invertOrder): dobj.score = 1 - dobj.score
	def _repr_html_(self):
		from lux.luxDataFrame.LuxDataframe import LuxDataFrame
		# widget  = LuxDataFrame.renderWidget(inputCurrentView=self,renderTarget="viewCollectionOnly")
		recommendation = {"action": "View Collection",
					  "description": "Shows a view collection defined by the context"}
		recommendation["collection"] = self

		checkImportLuxWidget()
		import luxWidget
		recJSON = LuxDataFrame.recToJSON([recommendation])
		widget =  luxWidget.LuxWidget(
				currentView={},
				recommendations=recJSON,
				context={}
			)
		display(widget)	