# BTE 413 Final Group Project: predicting the cost of a hospital stay at admission

Regression group demo (Ethan Grossman and Niko). University of Miami, BTE 413, Fall 2026.

## Run it (about a minute, no Google Drive needed)

1. Open the notebook in Google Colab: https://colab.research.google.com/github/ethanmooseg-star/bte413-hospital-cost/blob/main/BTE413_Demo.ipynb
2. Choose **Runtime > Run all**.
3. The last cell compares every number with the slides and prints OK or DIFFERS.

The notebook loads its data from a public link, so it also runs on a fresh runtime or for anyone else.

## What is in this folder

| File | What it is |
|---|---|
| `BTE413_Demo.ipynb` | The demo notebook: data, variable check, final model and test score, what drives cost |
| `sparcs_2024_clean_sample.csv.gz` | The cleaned data: 200,000 random stays, with a fixed `split` column (160,000 train, 40,000 test) |
| `clean_sparcs_2024.py` | The cleaning script that makes the data file from the raw state file |
| `BTE413_Demo_outputs_backup.html` | The notebook with its outputs, in case Colab or Wi-Fi fails |

## The project in short

- **Problem:** estimate what a hospital stay will cost at the moment of admission.
- **Data:** New York State Hospital Inpatient Discharges (SPARCS), 2024. It is a public, de-identified file (no names, no patient IDs, no dates). The full file has about 2.2 million stays; we use a random 200,000.
- **Rule:** the model only uses what a hospital knows when the patient arrives. Diagnosis, procedure, severity, length of stay and discharge status are set later, so they are left out.
- **Model:** linear regression on four variables (age group, type of admission, main payer, facility), predicting the log of cost. It is explainable, which a hospital needs.
- **Trimming:** we train and test on the 90% of stays under $54,107. That cutoff uses the final cost, so the model describes typical stays and a hospital could not apply the cutoff at admission.

## Results (test rows)

| Stays scored | R² (log) | Typical miss | Average miss |
|---|---|---|---|
| Typical stays under $54,107 (35,940) | 0.393 | $5,005 | $7,571 |
| All test stays (40,000) | 0.312 | $5,822 | $17,148 |

The "typical miss" is the median error in dollars. The model badly underestimates the costliest 10% of stays.

## Data source and privacy

- Source: [Hospital Inpatient Discharges (SPARCS De-Identified): 2024](https://health.data.ny.gov/), New York State Department of Health.
- We checked the four model variables against the HIPAA Safe Harbor list of identifiers: none is on it. This is a check against the list, not a compliance certification.
