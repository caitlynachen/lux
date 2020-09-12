import papermill as pm

pm.execute_notebook(
   'nycinput.ipynb',
   'output.ipynb',
)

import json

import nbformat as nbf
# nb = nbf.v4.new_notebook()

# with open('nycinput.ipynb') as json_file:
#   data = json.load(json_file)
#   # new_cell = nbf.v4.new_code_cell("df.default_display='lux'")
#   # data["cells"].append(new_cell)
#   for i in range(185):
#       new_cell = nbf.v4.new_code_cell("df")
#       data["cells"].append(new_cell)
#       new_cell = nbf.v4.new_code_cell("df.expire_recs()")
#       data["cells"].append(new_cell)
#   nb = nbf.from_dict(data)
# nbf.write(nb, 'nycinput.ipynb')

cell_count = []
duration = []
with open('output.ipynb') as json_file:
    data = json.load(json_file)
    for cell in data['cells']:
        # if ("execution_count" in cell):
        #   cell_count.append(cell["execution_count"])
        #   duration.append(cell["metadata"]["papermill"]["duration"])
        if "outputs" in cell and len(cell["outputs"]) > 0:
            if cell["outputs"][0]["output_type"] == "display_data":
                cell_count.append(cell["execution_count"])
                duration.append(cell["metadata"]["papermill"]["duration"])

# print(cell_count, duration)
import csv
with open('output6mil_200_nc.csv', mode='w') as output:
    file = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    file.writerow(['cell execution count', 'time (s)'])
    for i in range(len(cell_count)):
        file.writerow([cell_count[i], duration[i]])

import matplotlib.pyplot as plt
plt.xlabel('cell execution count')
plt.ylabel('time (s)')
plt.plot(cell_count, duration, marker="o")
plt.show()

# import nbformat as nbf
# nb = nbf.v4.new_notebook()
# 
# with open('input.ipynb') as json_file:
#   data = json.load(json_file)
#   cell = data["cells"][5]
#   cell["source"][0] = "df = pd.read_csv(\"lux/data/college.csv\")\n"
#   nb = nbf.from_dict(data)
# nbf.write(nb, 'input.ipynb')
