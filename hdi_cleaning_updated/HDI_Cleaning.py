import pandas as pd
import numpy as np
import statsmodels.formula.api as smf


# =========================================================
# CONFIG
# =========================================================

COL_JME_COUNTRY = "Country"
COL_HDI_COUNTRY = "country"
COL_JME_REGION = "UN Region"   # change here if needed

HDI_YEARS = [
    "hdi_1990",
    "hdi_2000",
    "hdi_2010",
    "hdi_2015",
    "hdi_2019",
    "hdi_2020",
    "hdi_2021",
    "hdi_2022"
]

COLS_TO_DROP = [
    "rank_change_2015_2022",
    "avg_growth_1990_2000",
    "avg_growth_2000_2010",
    "avg_growth_2010_2022",
    "tier_hdi",
    "iso3c"
]

COUNTRY_RENAME_MAP = {
    "Türkiye": "Turkey",
    "Eswatini (Kingdom of)": "Swaziland",
    "Moldova (Republic of)": "Republic of Moldova",
    "Tanzania (United Republic of)": "United Republic of Tanzania",
    "Congo (Democratic Republic of the)": "Democratic Republic of the Congo",
    "Palestine, State of": "State of Palestine",
    "Korea (Republic of)": "Republic of Korea",
    "Korea (Democratic People's Rep. of)": "Democratic People's Republic of Korea",
    "North Macedonia": "The former Yugoslav Republic of Macedonia"
}

NON_COUNTRY_VALUES = {
    "Very high human development",
    "High human development",
    "Medium human development",
    "Low human development",
    "World",
    "Developing countries",
    "Least developed countries",
    "Small island developing states",
    "Organisation for Economic Co-operation and Development",
    "Sub-Saharan Africa",
    "South Asia",
    "East Asia and the Pacific",
    "Europe and Central Asia",
    "Latin America and the Caribbean",
    "Arab States",
    "Hong Kong, China (SAR)"
}


# =========================================================
# HELPERS
# =========================================================

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names by stripping leading/trailing spaces.
    """
    df = df.copy()
    df.columns = df.columns.str.strip()
    return df


def standardize_text_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Standardize a text column by converting to string, stripping spaces,
    replacing textual 'nan', and restoring real missing values.
    """
    df = df.copy()
    df[col] = df[col].astype("string").str.strip()
    df[col] = df[col].replace("nan", pd.NA)
    return df


def drop_unwanted_hdi_columns(df_hdi: pd.DataFrame) -> pd.DataFrame:
    """
    Remove HDI columns that are not required for the analysis.
    """
    df_hdi = df_hdi.copy()
    existing_cols = [c for c in COLS_TO_DROP if c in df_hdi.columns]
    return df_hdi.drop(columns=existing_cols)


def harmonize_hdi_country_names(df_hdi: pd.DataFrame) -> pd.DataFrame:
    """
    Harmonize HDI country names to match the names used in the JME dataset.
    """
    df_hdi = df_hdi.copy()
    df_hdi[COL_HDI_COUNTRY] = df_hdi[COL_HDI_COUNTRY].replace(COUNTRY_RENAME_MAP)
    return df_hdi


def remove_non_country_rows(df_hdi: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows that correspond to regions, aggregates, or non-country entities.
    """
    df_hdi = df_hdi.copy()
    return df_hdi[~df_hdi[COL_HDI_COUNTRY].isin(NON_COUNTRY_VALUES)]


def filter_hdi_by_jme_countries(df_hdi: pd.DataFrame, df_jme: pd.DataFrame) -> pd.DataFrame:
    """
    Keep only countries in the HDI dataset that exist in the JME dataset.
    JME is used as the reference list of countries.
    """
    df_hdi = df_hdi.copy()
    countries_ref = set(df_jme[COL_JME_COUNTRY].dropna())
    return df_hdi[df_hdi[COL_HDI_COUNTRY].isin(countries_ref)]


def add_un_region(df_hdi: pd.DataFrame, df_jme: pd.DataFrame) -> pd.DataFrame:
    """
    Add the UN region column from JME to the HDI dataset.
    """
    df_hdi = df_hdi.copy()

    df_hdi = df_hdi.merge(
        df_jme[[COL_JME_COUNTRY, COL_JME_REGION]],
        left_on=COL_HDI_COUNTRY,
        right_on=COL_JME_COUNTRY,
        how="left"
    )

    df_hdi = df_hdi.drop(columns=[COL_JME_COUNTRY])
    df_hdi = df_hdi.rename(columns={COL_JME_REGION: "un_region"})

    return df_hdi


def missing_summary(df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
    """
    Produce a summary table of missing values, including counts and percentages.
    """
    if columns is None:
        columns = df.columns.tolist()

    miss = df[columns].isna().sum()
    pct = (miss / len(df)) * 100

    out = pd.DataFrame({
        "missing_values": miss,
        "percent": pct.round(2)
    }).sort_values(["percent", "missing_values"], ascending=False)

    return out


def compare_country_sets(df_jme: pd.DataFrame, df_hdi: pd.DataFrame) -> tuple[set, set]:
    """
    Compare country sets between JME and HDI.
    Returns:
    - countries present in JME but missing in HDI
    - countries present in HDI but missing in JME
    """
    jme_countries = set(df_jme[COL_JME_COUNTRY].dropna())
    hdi_countries = set(df_hdi[COL_HDI_COUNTRY].dropna())

    in_jme_not_hdi = jme_countries - hdi_countries
    in_hdi_not_jme = hdi_countries - jme_countries

    return in_jme_not_hdi, in_hdi_not_jme


def to_long_format(df_hdi_wide: pd.DataFrame) -> pd.DataFrame:
    """
    Convert the HDI dataset from wide format to long format.
    Output columns:
    - year
    - country
    - un_region
    - hdi
    """
    df_hdi_wide = df_hdi_wide.copy()

    hdi_cols = df_hdi_wide.filter(regex=r"^hdi_\d{4}$").columns.tolist()

    df_long = df_hdi_wide.melt(
        id_vars=["country", "un_region"],
        value_vars=hdi_cols,
        var_name="year",
        value_name="hdi"
    )

    df_long["year"] = df_long["year"].str.replace("hdi_", "", regex=False).astype(int)

    df_long = df_long[["year", "country", "un_region", "hdi"]]
    df_long = df_long.sort_values(["year", "country"]).reset_index(drop=True)

    return df_long


# =========================================================
# CLEANING PIPELINE
# =========================================================

def clean_hdi_with_jme_reference(df_jme: pd.DataFrame, df_hdi: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Main cleaning pipeline:
    1) clean column names
    2) standardize country text columns
    3) remove missing country rows
    4) remove unwanted HDI columns
    5) harmonize HDI country names
    6) remove non-country rows
    7) filter HDI using JME countries as reference
    8) add un_region from JME
    9) return cleaned dataframe + diagnostics
    """
    df_jme = df_jme.copy()
    df_hdi = df_hdi.copy()

    # Clean column names
    df_jme = clean_column_names(df_jme)
    df_hdi = clean_column_names(df_hdi)

    # Standardize key text columns
    df_jme = standardize_text_column(df_jme, COL_JME_COUNTRY)
    df_hdi = standardize_text_column(df_hdi, COL_HDI_COUNTRY)

    # Drop rows with missing country names
    df_jme = df_jme.dropna(subset=[COL_JME_COUNTRY])
    df_hdi = df_hdi.dropna(subset=[COL_HDI_COUNTRY])

    # Clean HDI dataset
    df_hdi = drop_unwanted_hdi_columns(df_hdi)
    df_hdi = harmonize_hdi_country_names(df_hdi)
    df_hdi = remove_non_country_rows(df_hdi)

    # Diagnostics before final filter
    missing_before_filter = compare_country_sets(df_jme, df_hdi)

    # Filter HDI using JME as country reference
    df_hdi_clean = filter_hdi_by_jme_countries(df_hdi, df_jme)

    # Add UN region from JME
    df_hdi_clean = add_un_region(df_hdi_clean, df_jme)

    # Reorder columns: country, un_region, then the rest
    ordered_cols = ["country", "un_region"] + [
        c for c in df_hdi_clean.columns if c not in ["country", "un_region"]
    ]
    df_hdi_clean = df_hdi_clean[ordered_cols]

    # Diagnostics after final filter
    missing_after_filter = compare_country_sets(df_jme, df_hdi_clean)

    diagnostic_cols = [c for c in HDI_YEARS if c in df_hdi_clean.columns]
    if "hdi_rank" in df_hdi_clean.columns:
        diagnostic_cols.append("hdi_rank")
    if "avg_growth_1990_2022" in df_hdi_clean.columns:
        diagnostic_cols.append("avg_growth_1990_2022")

    diagnostics = {
        "jme_shape": df_jme.shape,
        "hdi_shape_after_cleaning": df_hdi_clean.shape,
        "missing_summary": missing_summary(df_hdi_clean, columns=diagnostic_cols),
        "countries_in_jme_not_in_hdi_before_filter": missing_before_filter[0],
        "countries_in_hdi_not_in_jme_before_filter": missing_before_filter[1],
        "countries_in_jme_not_in_hdi_after_filter": missing_after_filter[0],
        "countries_in_hdi_not_in_jme_after_filter": missing_after_filter[1],
        "countries_without_region": df_hdi_clean[df_hdi_clean["un_region"].isna()][["country"]].drop_duplicates()
    }

    return df_hdi_clean.reset_index(drop=True), diagnostics


# =========================================================
# IMPUTATION PIPELINE
# =========================================================

def impute_hdi(df_hdi_clean: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Hierarchical imputation pipeline:
    1) temporal interpolation / extrapolation by country
    2) panel regression
    3) regional-temporal smoothing
    4) regional mean fallback

    Returns:
    - df_hdi_imputed (wide format)
    - df_long_imputed (long format, with audit columns)
    - imputation_audit (only imputed rows)
    """
    df_hdi_clean = df_hdi_clean.copy()

    # Identify HDI columns
    hdi_cols = df_hdi_clean.filter(regex=r"^hdi_\d{4}$").columns.tolist()

    # Convert to long format
    df_long = df_hdi_clean.melt(
        id_vars=["country", "un_region"],
        value_vars=hdi_cols,
        var_name="year",
        value_name="hdi"
    )

    df_long["year"] = df_long["year"].str.extract(r"(\d{4})").astype(int)
    df_long = df_long.sort_values(["country", "year"]).reset_index(drop=True)

    # Keep audit fields
    df_long["hdi_original"] = df_long["hdi"]
    df_long["imputed_flag"] = 0
    df_long["imputation_method"] = pd.NA

    # =====================================================
    # METHOD 1 — TEMPORAL INTERPOLATION / EXTRAPOLATION
    # =====================================================

    df_long["hdi_temp"] = (
        df_long.groupby("country")["hdi"]
        .transform(lambda x: x.interpolate(limit_direction="both"))
    )

    mask_temp = df_long["hdi"].isna() & df_long["hdi_temp"].notna()

    df_long.loc[mask_temp, "hdi"] = df_long.loc[mask_temp, "hdi_temp"]
    df_long.loc[mask_temp, "imputed_flag"] = 1
    df_long.loc[mask_temp, "imputation_method"] = "temporal_interpolation"

    # =====================================================
    # METHOD 2 — PANEL REGRESSION
    # =====================================================

    df_model = df_long.dropna(subset=["hdi"]).copy()

    # Countries with all original HDI values missing
    all_missing_countries = (
        df_long.groupby("country")["hdi_original"]
        .apply(lambda x: x.isna().all())
    )
    all_missing_countries = set(all_missing_countries[all_missing_countries].index)

    model = smf.ols(
        "hdi ~ C(country) + C(un_region) + year",
        data=df_model
    ).fit()

    mask_panel = df_long["hdi"].isna() & ~df_long["country"].isin(all_missing_countries)

    if mask_panel.sum() > 0:
        df_long.loc[mask_panel, "hdi"] = model.predict(df_long.loc[mask_panel])
        df_long.loc[mask_panel, "imputed_flag"] = 1
        df_long.loc[mask_panel, "imputation_method"] = "panel_regression"

    # =====================================================
    # METHOD 3 — REGIONAL-TEMPORAL SMOOTHING
    # =====================================================

    regional_mean = (
        df_long.groupby(["un_region", "year"])["hdi"]
        .mean()
        .rename("regional_mean")
    )

    tmp = df_long.merge(
        regional_mean.reset_index(),
        on=["un_region", "year"],
        how="left"
    )

    tmp["offset"] = tmp["hdi"] - tmp["regional_mean"]

    country_offset = (
        tmp.groupby("country")["offset"]
        .mean()
        .rename("country_offset")
    )

    tmp = tmp.merge(
        country_offset.reset_index(),
        on="country",
        how="left"
    )

    mask_rts = tmp["hdi"].isna()

    tmp.loc[mask_rts, "hdi_fill_rts"] = (
        tmp.loc[mask_rts, "regional_mean"] + tmp.loc[mask_rts, "country_offset"].fillna(0)
    )

    mask_rts_valid = tmp["hdi"].isna() & tmp["hdi_fill_rts"].notna()

    tmp.loc[mask_rts_valid, "hdi"] = tmp.loc[mask_rts_valid, "hdi_fill_rts"]
    tmp.loc[mask_rts_valid, "imputed_flag"] = 1
    tmp.loc[mask_rts_valid, "imputation_method"] = "regional_temporal_smoothing"

    df_long = tmp.copy()

    # =====================================================
    # METHOD 4 — REGIONAL MEAN FALLBACK
    # =====================================================

    regional_mean_fallback = (
        df_long.groupby(["un_region", "year"])["hdi"]
        .mean()
        .rename("regional_mean_fallback")
    )

    df_long = df_long.merge(
        regional_mean_fallback.reset_index(),
        on=["un_region", "year"],
        how="left"
    )

    mask_regional = df_long["hdi"].isna() & df_long["regional_mean_fallback"].notna()

    df_long.loc[mask_regional, "hdi"] = df_long.loc[mask_regional, "regional_mean_fallback"]
    df_long.loc[mask_regional, "imputed_flag"] = 1
    df_long.loc[mask_regional, "imputation_method"] = "regional_mean_fallback"

    # Mark still-missing rows
    mask_still_missing = df_long["hdi"].isna()
    df_long.loc[mask_still_missing, "imputation_method"] = "not_imputed"

    # Restrict HDI to valid range
    df_long["hdi"] = df_long["hdi"].clip(lower=0, upper=1)

    # Create imputation audit table
    imputation_audit = df_long.loc[df_long["imputed_flag"] == 1, [
        "country", "un_region", "year", "hdi_original", "hdi", "imputation_method"
    ]].copy()

    imputation_audit = imputation_audit.rename(columns={"hdi": "hdi_filled"})
    imputation_audit = imputation_audit.sort_values(["country", "year"]).reset_index(drop=True)

    # Convert back to wide format
    df_hdi_imputed = df_long.pivot(
        index=["country", "un_region"],
        columns="year",
        values="hdi"
    ).reset_index()

    df_hdi_imputed.columns = [
        f"hdi_{col}" if isinstance(col, int) else col
        for col in df_hdi_imputed.columns
    ]

    # Order columns
    ordered_cols = ["country", "un_region"] + [
        c for c in HDI_YEARS if c in df_hdi_imputed.columns
    ]
    remaining_cols = [c for c in df_hdi_imputed.columns if c not in ordered_cols]
    df_hdi_imputed = df_hdi_imputed[ordered_cols + remaining_cols]

    return df_hdi_imputed, df_long, imputation_audit


# =========================================================
# USAGE
# =========================================================

# Load raw datasets
df_jme = pd.read_excel("JME.xlsx")
df_hdi = pd.read_excel("worldhdi.xlsx")

# Run cleaning pipeline
df_hdi_clean, diag = clean_hdi_with_jme_reference(df_jme, df_hdi)

# Save cleaned wide dataset
df_hdi_clean.to_csv("hdi_clean.csv", index=False)

# Run imputation pipeline
df_hdi_imputed, df_long_imputed, imputation_audit = impute_hdi(df_hdi_clean)

# Save imputed wide dataset
df_hdi_imputed.to_csv("hdi_imputed.csv", index=False)

# Convert imputed wide dataset to final long format
df_hdi_long = to_long_format(df_hdi_imputed)

# Save long-format dataset
df_hdi_long.to_csv("hdi_long.csv", index=False)

# Save audit file
imputation_audit.to_csv("hdi_imputation_audit.csv", index=False)

# Diagnostics
print("Final cleaned HDI shape:", df_hdi_clean.shape)
print("\nMissing values summary before imputation:")
print(diag["missing_summary"])

print("\nCountries present in JME but missing in HDI after filtering:")
print(sorted(diag["countries_in_jme_not_in_hdi_after_filter"]))

print("\nCountries without UN region:")
print(diag["countries_without_region"])

print("\nImputed HDI shape:", df_hdi_imputed.shape)
print("Remaining missing values after imputation:", df_long_imputed["hdi"].isna().sum())

print("\nImputation method counts:")
print(df_long_imputed["imputation_method"].value_counts(dropna=False))

print("\nLong-format HDI shape:", df_hdi_long.shape)
print("\nPreview of hdi_long:")
print(df_hdi_long.head())


