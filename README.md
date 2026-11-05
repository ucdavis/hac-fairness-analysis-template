# Fairness Analysis Methods Template

This repository provides a Jupyter notebook for evaluating performance differences in binary clinical prediction models across race/ethnicity, sex or gender, age, and Healthy Places Index (HPI) groups. It supports Phase 2 of the UC Davis Health fairness assessment approach described in Taylor et al., *From Performance Metrics to Patient Consequences: A Framework for Assessing Fairness in Clinical Prediction Models* (forthcoming).

The notebook reports subgroup sample sizes, prevalence, confusion-matrix measures, AUROC, AUPRC, calibration, statistical comparisons, and disparity ratios. It is an analysis aid—not a certification that a model is fair or suitable for clinical deployment.

## Privacy and appropriate use

Do not commit patient-level data, protected health information (PHI), personally identifiable information (PII), credentials, or generated reports containing sensitive values. The included `.gitignore` blocks common data and output formats, but users remain responsible for reviewing every staged file before committing it.

Use only data and computing environments approved by your organization. Results require clinical, statistical, operational, and community interpretation and should not be used as the sole basis for deployment or patient-care decisions.

## Requirements

- Python 3.13 (the currently tested environment)
- JupyterLab, Jupyter Notebook, VS Code notebooks, or another compatible notebook runner
- The packages in `requirements.txt`

Create and activate a virtual environment, then install the tested dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Equivalent environment-management tools may be used. If a different Python or package version is required, validate the full notebook before relying on the results.

## Input data

The notebook reads CSV, Excel (`.xlsx` or `.xls`), or Parquet (`.parquet` or `.pq`) files. Configure the source-column mapping in the notebook's first cell.

Required template variables:

| Template variable | Meaning | Accepted values |
| --- | --- | --- |
| `time_var` | Encounter or prediction time | Six-digit `YYYYMM` values or parseable datetimes |
| `final_outcome` | Observed binary outcome | `0`/`1` or `Y`/`N` |
| `probability` | Model score | Probabilities from 0–1, or percentages from 0–100 |

Optional variables:

| Template variable | Meaning |
| --- | --- |
| `id_var` | Patient or encounter identifier; generated if omitted |
| `race_ethnicity` | Race/ethnicity group |
| `gender_identity` | Sex or gender group, according to the approved analysis definition |
| `age_group` | Numeric age or an existing age-group label |
| `hpi_score` | Continuous HPI score or an existing quartile/category |
| `cohort_flag_with_copd_asthma` | Optional cohort field for subsetting |

Columns declared in `column_mapping` but absent from the input are ignored when they are optional. Missing required columns produce a descriptive error.

## Running the analysis

1. Keep the input data outside the repository when possible.
2. Open `FairnessAnalysisMethodsTemplate.ipynb`.
3. Edit the first configuration cell:
   - `data_dir` and `data_name`
   - `model_name` and `project_info`
   - `column_mapping`
   - threshold, resampling counts, minimum group size, and optional subgroup filters
4. Leave `subset_filters = {}` to analyze all eligible rows.
5. Run the notebook from top to bottom.
6. Review warnings, excluded-row counts, group sizes, assumptions, and all results before interpretation.

The notebook renders results inline. It does not save datasets or reports automatically.

## Important methodological limitations

- The template supports binary outcomes and model scores only.
- Statistical significance does not establish clinical importance, discrimination, causation, or fairness.
- Nonsignificant findings do not demonstrate equivalence, especially for small groups.
- Results depend on data quality, outcome definition, threshold choice, subgroup definitions, missingness, and sample size.
- Multiple comparisons, sparse outcomes, calibration instability, and intersectional harms require explicit consideration.
- HPI and other area-level measures should not be interpreted as individual-level characteristics.
- The default minimum group size is a screening rule, not a universal adequacy standard.

## Repository contents

- `FairnessAnalysisMethodsTemplate.ipynb` — configurable analysis notebook
- `requirements.txt` — pinned runtime and input-format dependencies
- `.gitignore` — safeguards against committing common sensitive/generated files
- `LICENSE-NOTICE.md` — current licensing status and approval requirement
- `RELEASE_CHECKLIST.md` — items to confirm before making the repository public

## Citation

The accompanying methods manuscript is:

> Taylor et al. *From Performance Metrics to Patient Consequences: A Framework for Assessing Fairness in Clinical Prediction Models*. Forthcoming.

Add the final author list, year, journal, DOI, and a `CITATION.cff` file when the publication information is available and approved.

## License status

No open-source license has been granted yet. See `LICENSE-NOTICE.md` before copying, redistributing, or modifying this work outside authorized UC Davis use.

Complete `RELEASE_CHECKLIST.md` before changing the repository visibility to public.

