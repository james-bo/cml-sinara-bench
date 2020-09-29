# CML Sinara Bench

## Description
* Program version: 0.8
* Date: 29/09/2020

## Run
```shell script
python sinara.py [-h] -j $path_to_JSON_file [-k] [-v $path_to_folder] [-d]
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
|`submodels`         |*list&lt;str&gt;*  |List of submodels' basenames. Files must be placed into *Local storage* specified in `src/cfg/config.cfg` directory                     |
|`results`           |*list&lt;str&gt;*  |List of simulation result files which should be downloaded for further usage                                                            |
|`parents`           |*list&lt;int&gt;*  |List of IDs of parent objects, which task statuses must be *Finished* to allow current object to start processing                       |
|`targets`           |*list&lt;obj&gt;*  |List of objects with properties `name`, `value`, `condition`, `dimension`, `tolerance`, `description` describing Target CML-Bench object|
|`values`            |*list&lt;obj&gt;*  |List of objects with properties `name`, `value`, `dimension`, `description` describing Value CML-Bench object                           |

### Type *Solve*
Main type of user input file. Used for start calculations of selected simulations.
```json
{
    "Root": {
        "Behaviour": "Solve",
        "LCs": [
            {
                "vertex_id": 1,
                "loadcase_id": 691356,
                "base_simulation_id": 715467,
                "curr_task_status": "New",
                "solver": null,
                "storyboard": null,
                "submodels": [
                    "05192020_In_Loco.csv"
                ],
                "results": [
                    "In_Bearing_Out_Solution.xlsx"
                ],
                "parents": []
            },
            {
                "vertex_id": 2,
                "loadcase_id": 724312,
                "base_simulation_id": 724316,
                "curr_task_status": "New",
                "solver": null,
                "storyboard": null,
                "submodels": [
                    "05192020_In_Loco.csv"
                ],
                "results": [
                    "In_Bearing_Out_Solution.xlsx"
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
                "loadcase_id": 691356,
                "base_simulation_id": 715467,
                "targets": [
                    {
                        "name": "L1 Тестовый",
                        "value": 3000000.0,
                        "condition": 1,
                        "dimension": "км",
                        "tolerance": null,
                        "description": "Расчетный ресурс подшипника"
                    },
                    {
                        "name": "L1 ISO Тестовый",
                        "value": 3000000,
                        "condition": 1,
                        "dimension": "км",
                        "tolerance": null,
                        "description": "Расчетный ресурс подшипника"
                    }
                ]
            },
            {
                "vertex_id": 2,
                "loadcase_id": 724312,
                "base_simulation_id": 724316,
                "targets": [
                    {
                        "name": "L1 Тестовый",
                        "value": 3000000.0,
                        "condition": 1,
                        "dimension": "км",
                        "tolerance": null,
                        "description": "Расчетный ресурс подшипника"
                    },
                    {
                        "name": "L1 ISO Тестовый",
                        "value": 3000000,
                        "condition": 1,
                        "dimension": "км",
                        "tolerance": null,
                        "description": "Расчетный ресурс подшипника"
                    }
                ]
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
                "loadcase_id": 691356,
                "values": [
                    {
                        "name": "L1iso",
                        "value": "3169829.14142267",
                        "dimension": "",
                        "description": ""
                    },
                    {
                        "name": "L1",
                        "value": "3085763.49323079",
                        "dimension": "",
                        "description": ""
                    }
                ]
            },
            {
                "vertex_id": 2,
                "loadcase_id": 724312,
                "values": [
                    {
                        "name": "L2iso",
                        "value": "2859507.52350189",
                        "dimension": "",
                        "description": ""
                    },
                    {
                        "name": "L2",
                        "value": "1154161.06941917",
                        "dimension": "",
                        "description": ""
                    },
                    {
                        "name": "L1iso",
                        "value": "3583420.74003418",
                        "dimension": "",
                        "description": ""
                    },
                    {
                        "name": "L1",
                        "value": "1373667.31125683",
                        "dimension": "",
                        "description": ""
                    }
                ]
            }
        ]
    }
}
```

## Authors
* @james-bo
* @univang