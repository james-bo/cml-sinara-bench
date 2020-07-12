# CML Sinara Bench

## Description
* Program version: 0.6
* Date: 12/07/2020

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

### Type "Solve"
Main type of user input file. Used for start calculations of selected simulations.
```json
{
  "Root": {
    "Behaviour": "Solve",
    "LCs": [
      {
        "object_id": 1,
        "bench_id": null,
        "task_id": null,
        "task_status": "New",
        "solver": null,
        "storyboard": null,
        "base_simulation_id": 699033,
        "submodels": [
          "In_Loco v.04.01.csv"
        ],
        "results": [
        ],
        "parents": [
        ]
      },
      {
        "object_id": 2,
        "bench_id": null,
        "task_id": null,
        "task_status": "New",
        "solver": null,
        "storyboard": null,
        "base_simulation_id": 695587,
        "target_value": null,
        "target_condition": null,
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

### Type "Update targets"
User input file using for add target values to specified loadcases.
```json
{
  "Root": {
    "Behaviour": "Update targets",
    "LCs": [
      {
        "object_id": 1,
        "bench_id": null,
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
                     "description": null}],
        "current_values": []
      },
      {
        "object_id": 2,
        "bench_id": null,
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
                     "description": null}],
        "current_values": []
      }
    ]
  }
}
```

### Type "Values"
Output file with key results.
```json
{
  "Root": {
    "Behaviour": "Values",
    "LCs": [
      {
        "object_id": 1,
        "bench_id": null,
        "current_values": [{"name": "abc",
                            "value": 123.0,
                            "dimension": "mm",
                            "description": null}, 
                           {"name": "def",
                            "value": 198.0,
                            "dimension": "mm",
                            "description": null}]
      },
      {
        "object_id": 2,
        "bench_id": null,
        "current_values": [{"name": "hig",
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
