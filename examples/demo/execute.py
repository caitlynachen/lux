import papermill as pm

pm.execute_notebook(
   'input.ipynb',
   'output.ipynb',
)

import json

cell_count = []
duration = []
with open('output.ipynb') as json_file:
    data = json.load(json_file)
    for cell in data['cells']:
    	# if ("execution_count" in cell):
	    # 	cell_count.append(cell["execution_count"])
	    # 	duration.append(cell["metadata"]["papermill"]["duration"])
    	if "outputs" in cell and len(cell["outputs"]) > 0:
	    	if cell["outputs"][0]["output_type"] == "display_data":
	    		cell_count.append(count)
	    		count += 1
	    		duration.append(cell["metadata"]["papermill"]["duration"])
	    		print(cell["outputs"][0]["output_type"])

print(cell_count, duration)
import matplotlib.pyplot as plt
plt.xlabel('cell execution count')
plt.ylabel('time (s)')
plt.plot(cell_count, duration)
plt.show()

# import nbformat as nbf
# nb = nbf.v4.new_notebook()
# 
# with open('input.ipynb') as json_file:
# 	data = json.load(json_file)
# 	cell = data["cells"][5]
# 	cell["source"][0] = "df = pd.read_csv(\"lux/data/college.csv\")\n"
# 	nb = nbf.from_dict(data)
# nbf.write(nb, 'input.ipynb')





