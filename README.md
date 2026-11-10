# BTE 413 Final Group Project: hospital stays in New York, 2024

Regression group: Ethan Grossman and Niko. Classification group: Mac and Jacob. Ethics and fairness: Nikki. University of Miami, BTE 413, Fall 2026.

## Run it (about a minute, no Google Drive needed)

1. Open the notebook in Google Colab: https://colab.research.google.com/github/ethanmooseg-star/bte413-hospital-cost/blob/main/BTE413_Final_Group_Project_Notebook.ipynb
2. Choose **Runtime > Run all**.
3. The last cell compares every number with the slides and prints OK or DIFFERS.

The notebook loads its data from a public link, so it runs on a fresh runtime and for anyone else. By default it runs only the final models. To also rerun every experiment behind them (variable screens, k-NN, neural networks, cross-validation, ablation), set `RUN_FULL = True` in the first code cell. That took about 4 minutes on a laptop; on a free Colab runtime allow 20 to 30 minutes.

## What is in this folder

| File | What it is |
|---|---|
| `BTE413_Final_Group_Project_Notebook.ipynb` | The one notebook: data, regression, classification, the link between them, and a check against the slides |
| `sparcs_2024_clean_sample.csv.gz` | The cleaned data: 200,000 random stays, with a fixed `split` column (160,000 train, 40,000 test) |
| `oof_probabilities_admission.csv.gz` | The classification group's destination probabilities (admission-time variables, out-of-fold for the train rows), used in the link |
| `clean_sparcs_2024.py` | The cleaning script that makes the data file from the raw state file |
| `BTE413_Final_Group_Project_Notebook_outputs_backup.html` | The notebook with its outputs, in case Colab or Wi-Fi fails |

## The project in short

- **Data:** New York State Hospital Inpatient Discharges (SPARCS), 2024. A public, de-identified file (no names, no patient IDs, no dates). The full file has about 2.2 million stays; we use a random 200,000.
- **Regression (Ethan and Niko):** estimate what a stay will cost at the moment of admission. The model only uses what a hospital knows when the patient arrives. Linear regression on four variables (age group, type of admission, main payer, facility), predicting the log of cost. It is explainable, which a hospital needs. We train and test on the 90% of stays under $54,107, so it describes typical stays.
- **Classification (Mac and Jacob):** predict where the patient goes after the stay, in four groups: Home, Post-acute facility, Died or hospice, Other. Logistic regression, a decision tree and a neural network, compared by macro F1.
- **The link:** does knowing the likely destination help predict cost? Adding the predicted destination (from admission-time variables) to the cost model changes R² by +0.0006. Using the classification group's own exported probabilities gives the same answer (+0.0005). Even the true destination, which is only known after the stay, adds +0.025.

## Results (test rows)

| Model | Stays scored | Result |
|---|---|---|
| Cost, linear regression | 35,940 typical stays | R² 0.393, typical miss $5,005, average miss $7,571 |
| Cost, same model | all 40,000 | R² 0.312, typical miss $5,822, average miss $17,148 |
| Destination, logistic regression (with diagnosis code) | 40,000 | macro F1 0.379 (majority baseline 0.221) |
| Destination, logistic regression (admission-time variables only) | 40,000 | macro F1 0.321 |

The "typical miss" is the median error in dollars. The cost model badly underestimates the costliest 10% of stays. The destination classifier's best score uses the diagnosis code, which is assigned when the stay is coded and is not known at admission.

## Data source and privacy

- Source: [Hospital Inpatient Discharges (SPARCS De-Identified): 2024](https://health.data.ny.gov/), New York State Department of Health.
- We checked the four cost-model variables against the HIPAA Safe Harbor list of identifiers: none is on it. This is a check against the list, not a compliance certification.
