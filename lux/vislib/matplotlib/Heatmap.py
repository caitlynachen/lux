#  Copyright 2019-2020 The Lux Authors.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from lux.vislib.matplotlib.MatplotlibChart import MatplotlibChart
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lux.utils.utils import matplotlib_setup


class Heatmap(MatplotlibChart):
    """
    Heatmap is a subclass of MatplotlibChart that render as a heatmap.
    All rendering properties for heatmap are set here.

    See Also
    --------
    matplotlib.org
    """

    def __init__(self, vis, fig, ax):
        super().__init__(vis, fig, ax)

    def __repr__(self):
        return f"Heatmap <{str(self.vis)}>"

    def initialize_chart(self):
        # return NotImplemented
        x_attr = self.vis.get_attr_by_channel("x")[0]
        y_attr = self.vis.get_attr_by_channel("y")[0]

        x_attr_abv = x_attr.attribute
        y_attr_abv = y_attr.attribute

        if len(x_attr.attribute) > 25:
            x_attr_abv = x_attr.attribute[:15] + "..." + x_attr.attribute[-10:]
        if len(y_attr.attribute) > 25:
            y_attr_abv = y_attr.attribute[:15] + "..." + y_attr.attribute[-10:]
        
        color_attr = self.vis.get_attr_by_channel("color")
        df = None
        color_attr_name = ""
        color_map = "Blues"
        if len(color_attr) == 1:
            color_attr_name = color_attr[0].attribute
            df = pd.pivot_table(data=self.data, index="xBinStart", values=color_attr_name, columns="yBinStart")
            color_map = "viridis"
            self.fig, self.ax = matplotlib_setup(6, 4)
        else:
            df = pd.pivot_table(data=self.data, index="xBinStart", values="count", columns="yBinStart")
            df = df.apply(lambda x: np.log(x), axis=1)
        df = df.values

        plt.imshow(df, cmap=color_map)
        self.ax.set_aspect("auto")
        plt.gca().invert_yaxis()

        if len(color_attr) == 1:
            cbar = plt.colorbar(label=color_attr_name)
            cbar.outline.set_linewidth(0)

        self.ax.set_xlabel(x_attr_abv)
        self.ax.set_ylabel(y_attr_abv)
        self.ax.grid(False)

        self.code += "import matplotlib.pyplot as plt\n"
        self.code += "import numpy as np\n"
        self.code += "from math import nan\n"
        self.code += f"df = pd.pivot_table({str(self.data.to_dict())}, index='xBinStart', values='count', columns='yBinStart')\n"
        self.code += f"df = df.apply(lambda x: np.log(x), axis=1)\n"
        self.code += f"df = df.values\n"

        self.code += f"fig, ax = plt.subplots()\n"
        self.code += f"plt.imshow(df, cmap='Blues')\n"
        self.code += f"ax.set_aspect('auto')\n"
        self.code += f"plt.gca().invert_yaxis()\n"

        self.code += f"ax.set_xlabel('{x_attr_abv}')\n"
        self.code += f"ax.set_ylabel('{y_attr_abv}')\n"
        self.code += f"ax.grid(False)\n"
        self.code += f"fig\n"
