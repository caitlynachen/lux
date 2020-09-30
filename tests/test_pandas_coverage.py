from .context import lux
import pytest
import pandas as pd

###################
# DataFrame Tests #
###################

def test_deepcopy():
    url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
    df = pd.read_csv(url)
    df["Year"] = pd.to_datetime(df["Year"], format='%Y') 
    df._repr_html_();
    saved_df = df.copy(deep=True)
    saved_df._repr_html_();
    check_metadata_equal(df, saved_df)

def test_rename_inplace():
    url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
    df = pd.read_csv(url)
    df["Year"] = pd.to_datetime(df["Year"], format='%Y') 
    df._repr_html_();
    new_df = df.copy(deep=True)
    df.rename(columns={"Name": "Car Name"}, inplace = True)
    df._repr_html_();
    new_df._repr_html_();
    new_df, df = df, new_df # new_df is the old dataframe (df) with the new column name changed inplace
    
    assert df.data_type_lookup != new_df.data_type_lookup

    assert df.data_type_lookup["Name"] == new_df.data_type_lookup["Car Name"]

    assert df.data_type != new_df.data_type

    assert df.data_type["nominal"][0] == "Name"
    assert new_df.data_type["nominal"][0] == "Car Name"

    assert df.data_model_lookup != new_df.data_model_lookup

    assert df.data_model_lookup["Name"] == new_df.data_model_lookup["Car Name"]

    assert df.data_model != new_df.data_model

    assert df.data_model["dimension"][0] == "Name"
    assert new_df.data_model["dimension"][0] == "Car Name"

    assert list(df.unique_values.values()) == list(new_df.unique_values.values())
    assert list(df.cardinality.values()) == list(new_df.cardinality.values())
    assert df._min_max == new_df._min_max
    assert df.pre_aggregated == new_df.pre_aggregated
def test_rename():
    url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
    df = pd.read_csv(url)
    df["Year"] = pd.to_datetime(df["Year"], format='%Y') 
    df._repr_html_();
    new_df = df.rename(columns={"Name": "Car Name"}, inplace = False)
    new_df._repr_html_();
    assert df.data_type_lookup != new_df.data_type_lookup

    assert df.data_type_lookup["Name"] == new_df.data_type_lookup["Car Name"]

    assert df.data_type != new_df.data_type

    assert df.data_type["nominal"][0] == "Name"
    assert new_df.data_type["nominal"][0] == "Car Name"

    assert df.data_model_lookup != new_df.data_model_lookup

    assert df.data_model_lookup["Name"] == new_df.data_model_lookup["Car Name"]

    assert df.data_model != new_df.data_model

    assert df.data_model["dimension"][0] == "Name"
    assert new_df.data_model["dimension"][0] == "Car Name"

    assert list(df.unique_values.values()) == list(new_df.unique_values.values())
    assert list(df.cardinality.values()) == list(new_df.cardinality.values())
    assert df._min_max == new_df._min_max
    assert df.pre_aggregated == new_df.pre_aggregated
def test_rename3():

    url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
    df = pd.read_csv(url)
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    df.columns = ["col1", "col2", "col3", "col4","col5", "col6", "col7", "col8", "col9", "col10"]
    df._repr_html_()
    assert list(df.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal'] 
    assert len(df.cardinality) == 10
    assert "col2" in list(df.cardinality.keys())

def test_concat():

    url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
    df = pd.read_csv(url)
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    new_df = pd.concat([df.loc[:, "Name":"Cylinders"], df.loc[:, "Year":"Origin"]], axis = "columns")
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Distribution', 'Occurrence', 'Temporal'] 
    assert len(new_df.cardinality) == 5

def test_groupby_agg():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    new_df = df.groupby("Year").agg(sum)
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Column Groups']
    assert len(new_df.cardinality) == 7

# def test_groupby_agg_very_small():

#     url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
#     df = pd.read_csv(url)
#     df["Year"] = pd.to_datetime(df["Year"], format='%Y')
#     new_df = df.groupby("Origin").agg(sum).reset_index()
#     new_df._repr_html_()
#     assert list(new_df.recommendation.keys() ) == ['Column Groups']
#     assert len(new_df.cardinality) == 7

# def test_groupby_multi_index():
#     url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
#     df = pd.read_csv(url)
#     df["Year"] = pd.to_datetime(df["Year"], format='%Y')
#     new_df = df.groupby(["Year", "Cylinders"]).agg(sum).stack().reset_index()
#     new_df._repr_html_()
#     assert list(new_df.recommendation.keys() ) == ['Column Groups'] # TODO
#     assert len(new_df.cardinality) == 7 # TODO

def test_query():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    new_df = df.query("Weight > 3000")
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal']
    assert len(new_df.cardinality) == 9

def test_pop():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    df.pop("Weight")
    df._repr_html_()
    assert list(df.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal']
    assert len(df.cardinality) == 8

def test_transform():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    new_df = df.iloc[:,1:].groupby("Origin").transform(sum)
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence']
    assert len(new_df.cardinality) == 6

def test_get_group():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    gbobj = df.groupby("Origin")
    new_df = gbobj.get_group("Japan")
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal']
    assert len(new_df.cardinality) == 9

def test_applymap():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    mapping = {"USA": 0, "Europe": 1, "Japan":2}
    df["Origin"] = df[["Origin"]].applymap(mapping.get)
    df._repr_html_()
    assert list(df.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal']
    assert len(df.cardinality) == 9

def test_strcat():
    url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
    df = pd.read_csv(url)
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    df["combined"] = df["Origin"].str.cat(df["Brand"], sep = ", ")
    df._repr_html_()
    assert list(df.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal']
    assert len(df.cardinality) == 11

def test_named_agg():
    url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
    df = pd.read_csv(url)
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    new_df = df.groupby("Brand").agg(avg_weight = ("Weight", "mean"), max_weight = ("Weight", "max"), mean_displacement = ("Displacement", "mean"))
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Column Groups']
    assert len(new_df.cardinality) == 4

def test_change_dtype():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    df["Cylinders"] = pd.Series(df["Cylinders"], dtype = "Int64")
    df._repr_html_()
    assert list(df.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal']
    assert len(df.data_type_lookup) == 9

def test_get_dummies():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    new_df = pd.get_dummies(df)
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal']
    assert len(new_df.data_type_lookup) == 310

def test_drop():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    new_df = df.drop([0, 1, 2], axis = "rows")
    new_df2 = new_df.drop(["Name", "MilesPerGal", "Cylinders"], axis = "columns")
    new_df2._repr_html_()
    assert list(new_df2.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal']
    assert len(new_df2.cardinality) == 6

def test_merge():
    url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
    df = pd.read_csv(url)
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    new_df = df.drop([0, 1, 2], axis = "rows")
    new_df2 = pd.merge(df, new_df, how = "left", indicator = True)
    new_df2._repr_html_()
    assert list(new_df2.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal']  # TODO once bug is fixed
    assert len(new_df2.cardinality) == 11 # TODO once bug is fixed

def test_prefix():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    new_df = df.add_prefix("1_")
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal']
    assert len(new_df.cardinality) == 9
    assert new_df.cardinality["1_Name"] == 300

def test_loc():
    url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
    df = pd.read_csv(url)
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    new_df = df.loc[:,"Displacement":"Origin"]
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal']
    assert len(new_df.cardinality) == 6
    new_df = df.loc[0:10,"Displacement":"Origin"]
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Correlation', 'Distribution']
    assert len(new_df.cardinality) == 6
    new_df = df.loc[0:10,"Displacement":"Horsepower"]
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Correlation', 'Distribution']
    assert len(new_df.cardinality) == 2
    import numpy as np
    inter_df = df.groupby("Brand")[["Acceleration", "Weight", "Horsepower"]].agg(np.mean)
    new_df = inter_df.loc["chevrolet":"fiat", "Acceleration":"Weight"]
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Column Groups']
    assert len(new_df.cardinality) == 3

def test_iloc():
    url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
    df = pd.read_csv(url)
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    new_df = df.iloc[:,3:9]
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Correlation', 'Distribution', 'Occurrence', 'Temporal']
    assert len(new_df.cardinality) == 6
    new_df = df.iloc[0:11,3:9]
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Correlation', 'Distribution']
    assert len(new_df.cardinality) == 6
    new_df = df.iloc[0:11,3:5]
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Correlation', 'Distribution']
    assert len(new_df.cardinality) == 2
    import numpy as np
    inter_df = df.groupby("Brand")[["Acceleration", "Weight", "Horsepower"]].agg(np.mean)
    new_df = inter_df.iloc[5:10, 0:2]
    new_df._repr_html_()
    assert list(new_df.recommendation.keys() ) == ['Column Groups']
    assert len(new_df.cardinality) == 3

def check_metadata_equal(df1, df2):
    # Checks to make sure metadata for df1 and df2 are equal.
    for attr in df1._metadata:
        if attr == "_recommendation":
            x = df1._recommendation
            y = df2._recommendation
            for key in x:
                if key in y:
                    assert len(x[key]) == len(y[key])
                    for i in range(len(x[key])):
                        vis1 = x[key][i]
                        vis2 = y[key][i]
                        compare_vis(vis1, vis2)
        elif attr == "_rec_info":
            x = df1._rec_info
            y = df2._rec_info
            assert len(x) == len(y)
            for i in range(len(x)):
                x_info, y_info = x[i], y[i]
                for key in x_info:
                    if key in y_info and key == "collection":
                        assert len(x_info[key]) == len(y_info[key])
                        for i in range(len(x_info[key])):
                            vis1 = x_info[key][i]
                            vis2 = y_info[key][i]
                            compare_vis(vis1, vis2)
                    elif key in y_info:
                        assert x_info[key] == y_info[key]

        elif attr != "_widget":
            print(attr)
            assert getattr(df1, attr) == getattr(df2, attr)


def compare_clauses(clause1, clause2):
    assert clause1.description == clause2.description
    assert clause1.attribute == clause2.attribute
    assert clause1.value == clause2.value
    assert clause1.filter_op == clause2.filter_op
    assert clause1.channel == clause2.channel
    assert clause1.data_type == clause2.data_type
    assert clause1.data_model == clause2.data_model
    assert clause1.bin_size == clause2.bin_size
    assert clause1.weight == clause2.weight
    assert clause1.sort == clause2.sort
    assert clause1.exclude == clause2.exclude

def compare_vis(vis1, vis2):
    assert len(vis1._intent) == len(vis2._intent)
    for j in range(len(vis1._intent)):
        compare_clauses(vis1._intent[j], vis2._intent[j])
    assert len(vis1._inferred_intent) == len(vis2._inferred_intent)
    for j in range(len(vis1._inferred_intent)):
        compare_clauses(vis1._inferred_intent[j], vis2._inferred_intent[j])
    assert vis1._source == vis2._source 
    assert vis1._code == vis2._code
    assert vis1._mark == vis2._mark
    assert vis1._min_max == vis2._min_max
    assert vis1._plot_config == vis2._plot_config
    assert vis1.title == vis2.title
    assert vis1.score == vis2.score

################
# Series Tests #
################

# TODO: These will all fail right now since LuxSeries isn't implemented yet
# def test_df_to_series():
#     # Ensure metadata is kept when going from df to series
#     url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
#     df = pd.read_csv(url)
#     df._repr_html_() # compute metadata
#     assert df.cardinality is not None
#     series = df["Weight"]
#     assert isinstance(series,lux.core.series.LuxSeries), "Derived series is type LuxSeries."
#     assert df["Weight"]._metadata == ['name','_intent', 'data_type_lookup', 'data_type', 'data_model_lookup', 'data_model', 'unique_values', 'cardinality', 'min_max', 'plot_config', '_current_vis', '_widget', '_recommendation'], "Metadata is lost when going from Dataframe to Series."
#     assert df.cardinality is not None, "Metadata is lost when going from Dataframe to Series."
#     assert series.name == "Weight", "Pandas Series original `name` property not retained."

# def test_value_counts():
#     url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
#     df = pd.read_csv(url)
#     df._repr_html_() # compute metadata
#     assert df.cardinality is not None
#     series = df["Weight"]
#     series.value_counts()
#     assert isinstance(series,lux.core.series.LuxSeries), "Derived series is type LuxSeries."
#     assert df["Weight"]._metadata == ['name','_intent', 'data_type_lookup', 'data_type', 'data_model_lookup', 'data_model', 'unique_values', 'cardinality', 'min_max', 'plot_config', '_current_vis', '_widget', '_recommendation'], "Metadata is lost when going from Dataframe to Series."
#     assert df.cardinality is not None, "Metadata is lost when going from Dataframe to Series."
#     assert series.name == "Weight", "Pandas Series original `name` property not retained."

# def test_str_replace():
#     url = 'https://github.com/lux-org/lux-datasets/blob/master/data/cars.csv?raw=true'
#     df = pd.read_csv(url)
#     df._repr_html_() # compute metadata
#     assert df.cardinality is not None
#     series = df["Brand"].str.replace("chevrolet", "chevy")
#     assert isinstance(series,lux.core.series.LuxSeries), "Derived series is type LuxSeries."
#     assert df["Brand"]._metadata == ['name','_intent', 'data_type_lookup', 'data_type', 'data_model_lookup', 'data_model', 'unique_values', 'cardinality', 'min_max', 'plot_config', '_current_vis', '_widget', '_recommendation'], "Metadata is lost when going from Dataframe to Series."
#     assert df.cardinality is not None, "Metadata is lost when going from Dataframe to Series."
#     assert series.name == "Brand", "Pandas Series original `name` property not retained."

