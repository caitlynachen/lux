# from ..luxDataFrame.LuxDataframe import LuxDataFrame

class Validator:
	def __init__(self):
		self.name = "Validator"

	def __repr__(self):
		return f"<Validator>"

	@staticmethod
	# def validateSpec(ldf: LuxDataFrame):
	def validateSpec(ldf):
		def existsInDF(value,uniqueValues):
			return any(value in uniqueValues[vals] for vals in uniqueValues)

		def validateAttr(spec):
			if not((spec.attribute and spec.attribute == "?") or (spec.value and spec.value=="?")):
				if isinstance(spec.attribute,list):
					checkAttrExistsGroup = all(attr in list(ldf.columns) for attr in spec.attribute)
					if spec.attribute and not checkAttrExistsGroup:
						printWarning = True
				else:
						checkAttrExists = spec.attribute in list(ldf.columns)
						if spec.attribute and not checkAttrExists:
							printWarning = True

						if isinstance(spec.value, list):
							checkValExists = spec.attribute in uniqueVals and all(v in uniqueVals[spec.attribute] for v in spec.value)
						else:
							checkValExists = spec.attribute in uniqueVals and spec.value in uniqueVals[spec.attribute]
						if spec.value and not checkValExists:
							printWarning = True
				
				if isinstance(spec.value, list):
					checkValExistsGroup = all(existsInDF(val, uniqueVals) for val in spec.value)
					if spec.value and not checkValExistsGroup:
						printWarning = True

		# 1. Parse all string specification into Spec objects (nice-to-have)
		# 2. Validate that the parsed specification is corresponds to the content in the LuxDataframe.
		context = ldf.getContext()
		uniqueVals = ldf.uniqueValues
		printWarning = False
		for spec in context:
			if type(spec) is list:
				for s in spec:
					validateAttr(s)
			else:
				validateAttr(spec)


		if printWarning:
			#print warning
			raise ValueError("Input spec is inconsistent with DataFrame.")

		# lux.setContext(lux.Spec(attr = "Horsepower"))
		# lux.setContext(lux.Spec(attr = "A")) --> Warning
