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
from lux.utils.utils import get_agg_title


class LineChart(MatplotlibChart):
    """
    LineChart is a subclass of AltairChart that render as a line charts.
    All rendering properties for line charts are set here.

    See Also
    --------
    altair-viz.github.io
    """

    def __init__(self, dobj):
        super().__init__(dobj)

    def __repr__(self):
        return f"Line Chart <{str(self.vis)}>"

    def initialize_chart(self):
        self.tooltip = False  # tooltip looks weird for line chart
        x_attr = self.vis.get_attr_by_channel("x")[0]
        y_attr = self.vis.get_attr_by_channel("y")[0]

        x_attr_abv = x_attr.attribute
        y_attr_abv = y_attr.attribute

        if len(x_attr.attribute) > 25:
            x_attr_abv = x_attr.attribute[:15] + "..." + x_attr.attribute[-10:]
        if len(y_attr.attribute) > 25:
            y_attr_abv = y_attr.attribute[:15] + "..." + y_attr.attribute[-10:]

        # x_attr.attribute = x_attr.attribute.replace(".", "")
        # y_attr.attribute = y_attr.attribute.replace(".", "")

        # Remove NaNs only for Line Charts (offsets axis range)
        self.data = self.data.dropna(subset=[x_attr.attribute, y_attr.attribute])

        df = pd.DataFrame(self.data)

        objects = df[x_attr.attribute]
        y_pos = np.arange(len(objects))
        performance = df[y_attr.attribute]

        fig, ax = plt.subplots()
        ax.plot(objects, performance)

        if y_attr.data_model == "measure":
            agg_title = get_agg_title(y_attr)
            ax.set_xlabel(x_attr_abv)
            ax.set_ylabel(agg_title)
        else:
            agg_title = get_agg_title(x_attr)
            ax.set_xlabel(agg_title)
            ax.set_ylabel(y_attr_abv)

        # Convert chart to HTML
        import base64
        from io import BytesIO
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        chart_code = base64.b64encode(tmpfile.getvalue()).decode('utf-8') 
        # Inside chartGallery.tsx change VegaLite component to be adaptable to different rendering mechanism (e.g, img)
        # '<img src=\'data:image/png;base64,{}\'>
        return chart_code
