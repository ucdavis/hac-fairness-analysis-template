import csv
import io
import json
import os
import random
import tempfile
import unittest
import warnings
from contextlib import redirect_stdout
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = REPO_ROOT / "FairnessAnalysisMethodsTemplate.ipynb"


FULL_MAPPING = {
    "patientdurablekey": "id_var",
    "encmonth": "time_var",
    "y_ObservedOutcome": "final_outcome",
    "y_prob": "probability",
    "age_group_str": "age_group",
    "sex": "gender_identity",
    "DerivedRaceEthnicity": "race_ethnicity",
    "CAHPIQuartile": "hpi_score",
    "cohort_flag": "cohort_flag_with_copd_asthma",
}

REQUIRED_ONLY_MAPPING = {
    "patientdurablekey": "id_var",
    "encmonth": "time_var",
    "y_ObservedOutcome": "final_outcome",
    "y_prob": "probability",
}


def mimic_rows(n, include_demographics=True):
    """Create deterministic synthetic records; these are not derived from patient data."""
    rng = random.Random(20261110)
    rows = []
    for i in range(n):
        outcome = int(((i * 7) % 11) < 4)
        score = min(0.99, max(0.01, 0.25 + 0.35 * outcome + rng.uniform(-0.30, 0.30)))
        row = {
            "patientdurablekey": f"SYNTH-{i:05d}",
            "encmonth": 202601 + (i % 10),
            "y_ObservedOutcome": outcome,
            "y_prob": round(score, 6),
        }
        if include_demographics:
            row.update(
                {
                    "age_group_str": (10, 40, 75)[i % 3],
                    "sex": ("Female", "Male")[i % 2],
                    "DerivedRaceEthnicity": ("Group A", "Group B", "Group C")[i % 3],
                    "CAHPIQuartile": 1 + (i % 4),
                    "cohort_flag": "All",
                }
            )
        rows.append(row)
    return rows


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def execute_notebook(csv_path, *, mapping, min_group_n):
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    namespace = {"__name__": "__main__"}
    caught = []
    with warnings.catch_warnings(record=True) as warning_records, redirect_stdout(io.StringIO()):
        warnings.simplefilter("always")
        for index, cell in enumerate(notebook["cells"]):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            exec(compile(source, f"notebook-cell-{index}", "exec"), namespace)
            if "data_dir =" in source and "column_mapping =" in source:
                namespace.update(
                    data_dir=str(csv_path.parent),
                    data_name=csv_path.name,
                    model_name="Synthetic mimic model",
                    project_info="Automated regression test using synthetic data only.",
                    id_unit="patient",
                    column_mapping=mapping,
                    n_bootstrap=30,
                    n_permutation=30,
                    MIN_GROUP_N=min_group_n,
                    classification_threshold=0.5,
                )
            elif "import matplotlib.pyplot as plt" in source:
                namespace["plt"].switch_backend("Agg")
                namespace["display"] = lambda *args, **kwargs: None
                namespace["plt"].show = lambda *args, **kwargs: namespace["plt"].close("all")
        caught.extend(warning_records)
    return namespace, caught


class NotebookMimicDataTests(unittest.TestCase):
    def run_case(self, rows, *, mapping, min_group_n):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "synthetic_predictions.csv"
            write_csv(csv_path, rows)
            return execute_notebook(csv_path, mapping=mapping, min_group_n=min_group_n)

    def test_normal_synthetic_analysis_runs_all_cells(self):
        namespace, caught = self.run_case(
            mimic_rows(240), mapping=FULL_MAPPING, min_group_n=20
        )
        self.assertEqual(len(namespace["data"]), 240)
        self.assertFalse(namespace["race_table"].empty)
        self.assertFalse(
            any(type(item.message).__name__ == "PerfectSeparationWarning" for item in caught)
        )

        patient_summary = namespace["build_summary"](
            namespace["data"], "race_ethnicity", "Race/Ethnicity", min_n=20
        )
        self.assertIn("# Unique Patients", patient_summary.columns)
        self.assertIn("Patient-Level Prevalence", patient_summary.columns)

        namespace["id_unit_effective"] = "encounter"
        encounter_summary = namespace["build_summary"](
            namespace["data"], "race_ethnicity", "Race/Ethnicity", min_n=20
        )
        self.assertIn("# Unique Encounters", encounter_summary.columns)
        self.assertIn("Encounter-Level Prevalence", encounter_summary.columns)

    def test_undersized_groups_are_skipped_without_crashing(self):
        namespace, _ = self.run_case(
            mimic_rows(30), mapping=FULL_MAPPING, min_group_n=100
        )
        self.assertTrue(namespace["race_table"].empty)
        self.assertEqual(list(namespace["race_table"].columns), ["Metric"])
        summary = namespace["build_summary"](
            namespace["data"], "race_ethnicity", "Race/Ethnicity", min_n=100
        )
        self.assertTrue(summary.empty)
        self.assertIn("# Unique Patients", summary.columns)

    def test_required_only_input_skips_demographic_analysis(self):
        namespace, _ = self.run_case(
            mimic_rows(150, include_demographics=False),
            mapping=REQUIRED_ONLY_MAPPING,
            min_group_n=20,
        )
        self.assertFalse(namespace["has_race_ethnicity"])
        self.assertFalse(namespace["has_gender_identity"])
        self.assertFalse(namespace["has_age_group"])
        self.assertFalse(namespace["has_hpi_score"])
        self.assertEqual(namespace["metric_list_by_var"], {})

    def test_perfect_separation_is_skipped_not_reported(self):
        namespace, _ = self.run_case(
            mimic_rows(120), mapping=FULL_MAPPING, min_group_n=20
        )
        pd = namespace["pd"]
        separated = pd.DataFrame(
            {
                "race_ethnicity": ["A"] * 20 + ["B"] * 20,
                "y": [1] * 40,
                "pred": [0] * 20 + [1] * 20,
                "id_var": [f"ID-{i}" for i in range(40)],
            }
        )
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = namespace["pairwise_pvalues_all_metrics_min"](
                separated,
                group_col="race_ethnicity",
                id_col="id_var",
                metrics=["Sensitivity"],
            )
        self.assertIsNone(result)
        self.assertTrue(any("perfect separation" in str(w.message).lower() for w in caught))
        self.assertFalse(
            any(type(item.message).__name__ == "PerfectSeparationWarning" for item in caught)
        )


if __name__ == "__main__":
    unittest.main()
