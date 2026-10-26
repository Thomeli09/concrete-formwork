# concrete-formwork



## Disclaimer

This project is provided as-is, without warranty of any kind.

Before using it in laboratory, industrial, safety-critical, or regulated environments, verify that the software behaves correctly with your specific balance, communication interface, and measurement workflow.

The author is not responsible for incorrect measurements, data loss, equipment damage, or other consequences resulting from the use of this software.

**Status:** early development (`0.0.1`). The API may change before a stable release.

## Features
-
-
-
-
- Use general 2D drawing helpers for lines, bars, histograms, heatmaps and more.

## Requirements

- **Python 3.15 or later** (package metadata restricts installation accordingly).
- NumPy >= 2.5.4 and Matplotlib >= 3.11.2.
- Optional: Pandas for `to_dataframe()`; `highlight_text` for enriched figure text.

## Installation

Clone the repository:

```bash
git clone https://github.com/Thomeli09/concrete-formwork.git
cd concrete-formwork
```

Create a virtual environment (example commands for Windows PowerShell):

```powershell
py -3.15 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

On Linux/macOS, use `python3.15 -m venv .venv` and `source .venv/bin/activate`.
Alternatively, `python -m pip install -r requirements.txt` installs the editable
package. To install development dependencies:

```bash
python -m pip install -e ".[dev]"
# Or: python -m pip install -r requirements-dev.txt
```



## Quick start: Concrete formwork

```python
from ganttchart import GanttChart
from ganttchart.visualization import PlotParameters, save_figure

chart = GanttChart()
chart.add_task("Design", "2026-10-01", "2026-10-10", completion=1.0, group="Planning")
chart.add_task("Build", "2026-10-11", "2026-10-25", completion=0.4, group="Construction")

style = PlotParameters(
    title="Project schedule", xlabel="Date", figsize=(12, 5),
    show_grid=True, grid_axis="x", date_format="%d %b",
)
fig, ax = chart.plot(parameters=style, show_weekends=True)
save_figure(fig, "schedule.png")
```
## Runnable examples

For supported balances, serial communication settings, and API examples, see the project documentation and source code.
## Runnable examples

Complete scripts are stored in [`examples/`](examples/README.md):

| File | What it demonstrates |
| --- | --- |
| [`01_formwork_basic.py`](examples/01_formwork_basic.py) | Simple task schedule and PNG export |
| [`02_concrete-formwork.py`](examples/02_concrete-formwork.py) | Task groups, colors, weekends, fixed today, PNG/PDF |
| [`03_concrete-formwork_dashboard.py`](examples/03_concrete-formwork_dashboard.py) | Gantt and progress curve in one figure |
| [`04_concrete-formwork_dataframe.py`](examples/04_concrete-formwork_dataframe.py) | Optional Pandas DataFrame and CSV export |

After installation, run any example from the repository root:

```bash
python examples/01_formwork_basic.py
python examples/02_concrete-formwork.py
python examples/03_concrete-formwork_dashboard.py
python examples/04_concrete-formwork_dataframe.py
```

Outputs are written to `examples/output/` (ignored by Git). To override the
output folder, set the `concrete-formwork_EXAMPLE_OUTPUT` environment variable.
The examples have fixed input data and do not depend on external files.

## Package structure

```text
src/concrete_formwork/
  __init__.py                # GanttChart, Task, add_days
  concrete_formwork.py              # Task management; plot() delegates to the renderer
  utils/                     # List, vector and matrix operations
  visualization/
    __init__.py
    plot_parameters.py       # PlotParameters dataclass
    plot_basic.py            # Figure and axes management, legend, export
    plot_2d.py               # General 2D plotting artists
    plot_gantt.py            # Gantt-specific rendering
examples/                    # Runnable examples
tests/                      # Unit and smoke tests
```

## Testing

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

Run the smoke tests in headless mode on a CI server by setting `MPLBACKEND=Agg`.
You can also run all seven examples with `python -m pytest -q tests/test_examples.py`.

## Contributing

Contributions are welcome.

Examples of useful contributions include:

* support for additional balances or communication protocols;
* bug fixes;
* improvements to serial communication handling;
* additional tests;
* documentation improvements;
* usage examples;
* compatibility improvements for different operating systems.

If you plan to make a significant change, consider opening an issue first to discuss the proposed implementation.

## Citation

If you use this software in technical or published work, cite the project.
Citation details are in [`CITATION.cff`](CITATION.cff).

```bibtex
@software{Thommes_ConcreteFormwork_2026,
  author  = {Thommes, Eliott},
  title   = {Concrete-formwork: A Python concrete formwork, },
  year    = {2026},
  version = {0.0.1},
  url     = {https://github.com/Thomeli09/concrete-formwork}
}
```

Author: **Eliott Thommes** · [ORCID 0009-0005-0697-2438](https://orcid.org/0009-0005-0697-2438)

## License

Copyright © 2026 Eliott Thommes.

Licensed under the **GNU General Public License, version 3 or later**
(`GPL-3.0-or-later`). See [`LICENSE`](LICENSE) for the complete GPL-3.0 text.