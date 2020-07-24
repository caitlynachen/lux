********
Hello World
********

This tutorial provides an overview of how you can use Lux in your data exploration workflow. 
You can follow along the tutorial using this Jupyter notebook. 

Note: This tutorial assumes that you have already installed Lux and the associate Jupyter widget, if you have not done so already, please check out this page.

.. TODO: add link to page

Lux Overview
---------------------

Lux is designed to be tightly integrated with `Pandas <https://pandas.pydata.org/>`_, so that Lux can be used as-is, without modifying your existing Pandas code.
Lux preserves the Pandas dataframe semantics -- which means that you can apply any command from Pandas's API to the dataframes in Lux and expect the same behavior.

Some intro text here...

.. helloworld::
    import pandas as pd
    import lux
    df = pd.read_csv("../lux/data/college.csv")
    df._repr_html_()
    df.renderHTML()

.. TODO: insert image


When you click on this button, you should see three tabs of visualizations recommended to you. 

.. TODO: insert image

Voila! You have generated your first set of recommendations through Lux!
We will describe the details of how these recommendations are generated in the later portion of this tutorial.

.. TODO: insert link

Context: Specification of User Intent
-------------------------------------

We just saw an example of how recommendations can be generated for the dataset without providing additional information.
Beyond these overview visualizations, you can further specify the data attributes and values that you are interested in to Lux. 
This specification is known as the _context_.  
For example, let's say that you are interested in learning more about the median earning of students after they attend the college (i.e. the attribute `MedianEarning`).

.. code-block:: python

    df.setContext(["MedianEarnings"])

When you print out the dataframe again, you should see three tabs of visualizations recommended to you. 

.. code-block:: python

    df

.. TODO: insert image

Lux is built on the principle that users should always be able to visualize and explore anything they specify, without having to think about how the visualization should look like. 
Here, the Current View visualization represent the visualization that you have specified. 
On the right, you will again see the recommendations based on this Current View.

You can specify a variety of things that you might be interested in, for example, let's say that you are interested in the the median earnings of students in publicly-funded colleges.

.. code-block:: python

    df.setContext(["MedianEarnings", "FundingModel=Public"])

For more advance use of context, refer to this page on how to specify the context.

Recommendations in Lux
----------------------

Recommendations highlight interesting patterns and trends in your dataset. 
Lux offers different types of recommendations, known as called `analytical actions`.
We show a set of default recommendations depending on what you have specified in the context.

By default, if no context is specified, we display three different types of actions by default: 

- Correlation (:mod:`lux.action.Correlation`) displays relationships between two quantitative variables, ranked by the most to least correlated scatterplots.
- Distribution (:mod:`lux.action.Distribution`) displays histogram distributions of different quantitative attributes in the dataset, ranked by the most to least skewed distributions.
- Category displays bar chart distributions of different categorical attributes in the dataset, ranked by the most to least uneven bar charts.

In the earlier example, when `MedianEarning` is added to the context, the current context is represented as C = {MedianEarnings}.

.. code-block:: python

    df.setContext(["MedianEarnings"])

Given the updated context, additional actions are generated. 

- Enhance adds an additional attribute to current context (:mod:`lux.action.Enhance`). For example, enhance displays visualizations involving C' = {MedianEarnings, *added attribute*}, including:

    - {MedianEarnings, **Expenditure**}
    - {MedianEarnings, **AverageCost**}
    - {MedianEarnings, **AverageFacultySalary**}.

- Filter adds an additional filter to the current context (:mod:`lux.action.Filter`). For example, Filter displays visualizations involving C' = {MedianEarnings, *added filter*}, including: 

    - {MedianEarnings, **FundingModel=Public**}
    - {MedianEarnings, **Region=Southeast**}
    - {MedianEarnings, **Region=Great Lakes**}.

Refer to this page for additional information about the different types of action or how to define your own action types.

.. Add link to recommendation type details page