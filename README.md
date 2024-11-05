# UM-SearchAlgorithm
This project was developed for the subject IA (Inteligencia Artificial/_Artificial Intelligence_) from University of Minho - Software Engineering degree.

#### Requirements:
To run this project you might need to install some of its dependencies:

```shell
$ pip install colorama matplotlib osmnx geopandas networkx shapely
```

## How to run
```shell
$ make
```
or if you want to run a specific test:
```shell
$ make args="[test|run_dynamic|run_irl]"
```

## Report
The pre-compiled version of the report can be found in the `relatorio` folder (`relatorio.pdf`). If you want to compile it yourself, you can do so by running:
```shell
$ make relatorio
```
###### Attention: You need to have [Typst](https://typst.app/) installed to compile

### Developement Team
A104365 - Fábio Magalhães