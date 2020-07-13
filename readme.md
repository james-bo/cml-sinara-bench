# CML Sinara Bench

## Description
* Program version: 0.7
* Date: 13/07/2020

## Run
```shell script
python sinara.py [-h] -j <path_to_JSON_file> [-k] [-v <path_to_folder>] [-d]
```
* `-h` shows help message and exit
* `-j` select JSON (**mandatory argument**)
* `-k` if there is a file with username and password in `./cfg` directory
* `-v` if JSON is of type *Solve* writes all simulation key results into output file `results.json` in selected directory
* `-d` shows additional debug information in terminal

## Dependencies
* [`python 3.7+`](https://www.python.org/downloads/)
* [`requests`](https://requests.readthedocs.io/en/master/user/install/#install)
* [`colorama`](https://pypi.org/project/colorama/)

## Examples of input and output JSON files

### JSON properties description
|Property            |Type               |Description                                                                                                                             |
|--------------------|-------------------|----------------------------------------------------------------------------------------------------------------------------------------|
|`vertex_id`         |*int*              |Unique identifier of object in JSON file                                                                                                |
|`loadcase_id`       |*int* &#x7c; *null*|Loadcase ID from CML-Bench, or *null*, if unknown. In this case Loadcase ID will be restored from the base simulation                   |
|`base_simulation_id`|*int*              |Base simulation ID from CML-Bench                                                                                                       |
|`curr_simulation_id`|*int* &#x7c; *null*|Current simulation ID from CML-Bench, or *null*, if unknown (for new tasks)                                                             |
|`curr_task_id`      |*int* &#x7c; *null*|Current task ID from CML-Bench, or *null*, if unknown (for new tasks)                                                                   |
|`curr_task_status`  |*str*              |Task status of current simulation. For the first time must be *"New"*                                                                   |
|`solver`            |*str* &#x7c; *null*|Solver name, or *null*, if unknown. In this case value obtained from the base simulation will be used                                   |
|`storyboard`        |*int* &#x7c; *null*|Storyboard ID from CML-Bench, or *null* if unknown. In this case value obtained from the base simulation will be used                   |
|`submodels`         |*list<str>*        |List of submodels' basenames. Files must be placed into *Local storage* specified in `src/cfg/config.cfg` directory                     |
|`results`           |*list<str>*        |List of simulation result files which should be downloaded for further usage                                                            |
|`parents`           |*list<int>*        |List of IDs of parent objects, which task statuses must be *Finished* to allow current object to start processing                       |
|`targets`           |*list<obj>*        |List of objects with properties `name`, `value`, `condition`, `dimension`, `tolerance`, `description` describing Target CML-Bench object|
|`values`            |*list<obj>*        |List of objects with properties `name`, `value`, `dimension`, `description` describing Value CML-Bench object                           |

### Type *Solve*
Main type of user input file. Used for start calculations of selected simulations.
```json
{
    "Root": {
        "Behaviour": "Solve",
        "LCs": [
            {
                "vertex_id": 1,
                "loadcase_id": null,
                "base_simulation_id": 699033,
                "curr_task_status": "New",
                "solver": null,
                "storyboard": null,
                "submodels": [
                    "In_Loco v.04.01.csv"
                ],
                "results": [],
                "parents": []
            },
            {
                "vertex_id": 2,
                "loadcase_id": null,
                "base_simulation_id": 695587,
                "curr_task_status": "New",
                "solver": null,
                "storyboard": null,
                "submodels": [
                    "Material.dat",
                    "Property.dat",
                    "shveller.dat"
                ],
                "results": [
                    "start.f06",
                    "start.op2"
                ],
                "parents": [
                    1
                ]
            }
        ]
    }
}
```

### Type *Update targets*
User input file using for add target values to specified loadcases.
```json
{
    "Root": {
        "Behaviour": "Update targets",
        "LCs": [
            {
                "vertex_id": 1,
                "loadcase_id": null,
                "base_simulation_id": 699033,
                "targets": [{"name": "",
                             "value": 100.0,
                             "condition": 1,
                             "dimension": "mm",
                             "tolerance": null,
                             "description": null},
                            {"name": "",
                             "value": 200.0,
                             "condition": 2,
                             "dimension": "mm",
                             "tolerance": null,
                             "description": null}]
            },
            {
                "vertex_id": 2,
                "loadcase_id": null,
                "base_simulation_id": 695587,
                "targets": [{"name": "",
                             "value": 300.0,
                             "condition": 2,
                             "dimension": "MPa",
                             "tolerance": null,
                             "description": null},
                            {"name": "",
                             "value": 400.0,
                             "condition": 1,
                             "dimension": "MPa",
                             "tolerance": null,
                             "description": null}]
            }
        ]
    }
}
```

### Type *Values*
Output file with key results.
```json
{
    "Root": {
        "Behaviour": "Values",
        "LCs": [
            {
                "vertex_id": 1,
                "loadcase_id": null,
                "values": [{"name": "abc",
                            "value": 123.0,
                            "dimension": "mm",
                            "description": null}, 
                           {"name": "def",
                            "value": 198.0,
                            "dimension": "mm",
                            "description": null}]
            },
            {
                "vertex_id": 2,
                "loadcase_id": null,
                "values": [{"name": "hig",
                            "value": 298.0,
                            "dimension": "MPa",
                            "description": null}, 
                           {"name": "klm",
                            "value": 512.0,
                            "dimension": "MPa",
                            "description": null}]
            }
        ]
    }
}
```
