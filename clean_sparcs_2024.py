"""
Clean the NY SPARCS 2024 inpatient discharge file for the BTE 413 group project.

Input : the raw CSV downloaded from health.data.ny.gov (SPARCS Hospital Inpatient Discharges, 2024)
Output: sparcs_2024_clean_sample.csv  (cleaned random sample, ready to share)
        sparcs_2024_code_lookup.csv   (code -> description, for reading results)

Run:  python clean_sparcs_2024.py "<path to raw csv>"
Needs: pandas
"""
import math
import sys
import pandas as pd

RAW = sys.argv[1] if len(sys.argv) > 1 else \
    "../Hospital_Inpatient_Discharges_(SPARCS_De-Identified)__2024_20261029.csv"
OUT = "sparcs_2024_clean_sample.csv"
LOOKUP = "sparcs_2024_code_lookup.csv"
SAMPLE_N = 200_000   # rows shared with the group (full file is ~2.2M rows)
SEED = 42            # fixed so everyone gets the same sample and the same split
TEST_SHARE = 0.20    # share of rows marked as the test set

# 1. Load everything as text first, so codes like "001139" keep their leading zeros.
df = pd.read_csv(RAW, dtype=str)
print("raw rows:", len(df))
df = df.apply(lambda col: col.str.strip())

# 2. Save a code -> description lookup, then drop the description columns (they repeat the codes).
pairs = [("CCSR Diagnosis Code", "CCSR Diagnosis Description"),
         ("CCSR Procedure Code", "CCSR Procedure Description"),
         ("APR DRG Code", "APR DRG Description"),
         ("APR MDC Code", "APR MDC Description")]
lookup = pd.concat(
    [df[[c, d]].dropna().drop_duplicates().rename(columns={c: "code", d: "description"}).assign(field=c)
     for c, d in pairs])
lookup[["field", "code", "description"]].to_csv(LOOKUP, index=False)

# 3. Drop rows we cannot use.
df = df.dropna(subset=["Hospital County", "Health Service Area", "Permanent Facility Id"])   # ~0.2%: redacted records
df = df[df["APR Severity of Illness Description"] != "Undetermined"]                          # 456 rows
df = df[df["APR Risk of Mortality"] != "Undetermined"]
df = df[df["Gender"] != "U"]                                                                 # 385 rows

# 4. Numbers stored as text -> numbers.
df["length_of_stay"] = df["Length of Stay"].replace("120+", "120").astype(int)   # "120+" means 120 or more
df["total_charges"] = df["Total Charges"].astype(float)
df["total_costs"] = df["Total Costs"].astype(float)
df = df[(df["total_costs"] > 0) & (df["total_charges"] > 0)]                     # 2 rows with zero cost

# 5. Missing values that really mean "none".
for col in ["CCSR Procedure Code", "Payment Typology 2", "Payment Typology 3"]:
    df[col] = df[col].fillna("None")           # no procedure / no second or third payer
df["Zip Code"] = df["Zip Code"].fillna("Unknown")

# 6. Drop columns we do not need.
df = df.drop(columns=[
    "Length of Stay", "Total Charges", "Total Costs",       # replaced by the numeric versions above
    "CCSR Diagnosis Description", "CCSR Procedure Description",
    "APR DRG Description", "APR MDC Description",
    "Operating Certificate Number", "Facility Name",         # repeat Permanent Facility Id
    "Discharge Year",                                        # always 2024
    "Birth Weight",                                          # 90% empty, only filled for newborns
    "APR Severity of Illness Description"])                  # repeats the severity code

# 7. Target columns (the group picks which to use).
df["log_total_costs"] = df["total_costs"].apply(math.log)   # costs are very skewed
cut = df["total_costs"].quantile(0.90)
df["high_cost"] = (df["total_costs"] >= cut).astype(int)   # 1 = in the most expensive 10% of stays
print(f"high_cost cutoff: ${cut:,.0f}")

# 8. Random sample, then a fixed train/test label shared by everyone.
df = df.sample(n=SAMPLE_N, random_state=SEED).reset_index(drop=True)
df["split"] = "train"
df.loc[df.sample(frac=TEST_SHARE, random_state=SEED).index, "split"] = "test"

# 9. Tidy names and save.
df.columns = [c.lower().replace(" ", "_").replace("/", "_") for c in df.columns]
df.to_csv(OUT, index=False)
print("clean sample rows:", len(df), "| columns:", df.shape[1])
print(df["split"].value_counts().to_dict(), "| high_cost share:", round(df["high_cost"].mean(), 3))
