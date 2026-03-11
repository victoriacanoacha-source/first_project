# Project overview
Religion has undoubtedly played a crucial role in societies and their development, but in recent years with regional conflicts rising and economic insecurity looming the role and importance of religion is changing. Thus, we want to analyse how conflict, economic development and societal factors (HDI) affect religious affiliation between countries and regions. Understanding the factors associated with these differences can provide insights into broader social and economic patterns.



*Research Question*: How do economic development, conflict, and societal factors influence levels of religious affiliation across regions overtime?

- *Hypothesis 1*: Countries with higher GDP per capita tend to have lower levels of religious affiliation.

- *Hypothesis 2*: Regions experiencing higher levels of conflict tend to show stronger religious affiliation.


To address this question and test our hypothesis, multiple global datasets were combined and analysed, including data on religious populations, economic indicators, human development, and the socio-economic impacts of war.

The project integrates data from several sources:

1. Religious Populations Worldwide dataset, which provides information on the distribution of major religious groups by country.

2. World Bank GDP dataset, which includes economic indicators such as GDP per capita.

3. Human Development Index (HDI) data from the United Nations Development Programme, capturing broader measures of societal development including education and life expectancy.

4. War Economic & Livelihood Impact dataset, which captures the economic and social effects of major conflicts, including GDP changes and food insecurity rates.

## Variables 

1. Country: The name of the country for which the data is recorded. Each observation corresponds to a specific country.

2. Year: The year in which the data was recorded. The dataset includes observations for the years 1990, 1995, 2000, 2005, and 2010, allowing analysis of trends over time.

3. Religions (christianity, judaism, islam, buddhism, hindu, shinto, confus_tao): These variables represent the population counts of the seven largest global religions within each country for a given year. They indicate how many people in a country identify with each religion at that time.

4. GDP: Gross Domestic Product per capita for each country and year. This measures the average economic output per person, providing an indicator of a country's level of economic development.

5. UN Region: The regional classification of countries according to the United Nations geographic grouping system. Examples include Africa, Asia, Europe, Latin America and the Caribbean, Northern America, and Oceania.

6. Conflict Present: A binary variable indicating whether a country is involved in an armed conflict in a given year. A conflict is defined as a situation where a specified number of people have died due to organized violence, and it includes the country where the conflict is occurring.

7. HDI (Human Development Index): A composite index measuring a country’s level of human development based on life expectancy, education, and income. It provides a broader indicator of societal development beyond economic measures alone.

8. Population: The total population of a country in a given year. This variable represents the total number of people living in the country and is used to contextualize the size of religious populations and calculate religious share.


## Data Cleaning, Transformation, Integration

1. Data Cleaning

Each dataset was cleaned individually before integration. The main cleaning steps included:

Standardizing column names to ensure consistency across datasets.

Converting variables to appropriate data types (e.g., numeric, categorical).

Removing duplicate records where necessary.

Handling missing values in key variables.

Standardizing country names to ensure compatibility across datasets.

Filtering datasets to include relevant observations.

The cleaned datasets were saved in the data/processed directory.

2. Data Transformation

Additional transformations were performed to prepare the datasets for merging:

Conflict data was structured to align with country-based analysis.

Relevant variables were selected from each dataset to reduce unnecessary complexity.

Inconsistent formats (e.g., percentages, numeric values) were standardized.

Used UN's region/country classification to ensure all countries and their respective regions followed the same format


3. Data Integration

The cleaned datasets were merged into a unified dataset using common identifiers:

Country

Year

The merging process followed a stepwise approach:

The religious population dataset was used as the base dataset.

GDP data was merged using country and year as keys.

HDI data was added to incorporate societal development indicators.

Conflict data was merged to include information on war-related economic impacts.

Left joins were used during the merging process to ensure that all observations from the base dataset were preserved while incorporating additional variables where available.

## Main dataset issues and solutions

Dataset Challenges and Solutions

*Challenge 1*: Limited time coverage in the religious population dataset
The religious population dataset only contained observed data up to 2010, while the project analyzes relationships between religion, economic development, and societal factors in more recent years.

*Solution 1*: Additional datasets were explored to identify sources that contained non-projected religious population data for years beyond 2010. Preference was given to datasets with observed values rather than projections, as projected values could introduce additional uncertainty into the analysis.


*Challenge 2*: Mismatched time ranges between datasets
The Human Development Index (HDI) dataset only contains data up to 2022, while the conflict dataset includes conflicts extending to 2025. Ideally, all datasets would cover the same time range for direct comparison.

*Solution 2*: Instead of restricting all datasets to the same time range, the full conflict dataset was preserved in order to retain broader regional and country coverage. Limiting the conflict dataset to 2022 would have removed several conflicts affecting multiple countries and regions, which would significantly reduce the dataset’s analytical value.


*Challenge 3*: Inconsistent temporal coverage across variables
Because the datasets were collected from different sources and updated at different intervals, some variables are not available for every country-year combination, particularly for years beyond 2022 where HDI data is not available.

*Solution 3*:The datasets were merged while preserving all available observations, allowing the analysis to use the maximum amount of available information. Missing values were handled carefully during analysis to avoid introducing bias into the results.


*Challenge 4*: Differences in dataset structure and variable naming
The datasets originated from different sources and used different column names, formats, and country naming conventions, which can create issues during merging.

*Solution 4*: Data cleaning and preprocessing steps were performed to standardize column names, harmonize country identifiers, and ensure consistent formatting across all datasets before merging.


## Exploratory Data Analysis

After the datasets were merged, exploratory analysis was conducted to identify patterns and relationships between variables. This included:

Comparing religious affiliation across regions and countries

Examining relationships between GDP per capita and religious composition

Exploring the impact of conflict-related variables on societal conditions

Visualizing trends and distributions using Python data visualization libraries

## Visualisations














# Installation

1. **Clone the repository**:

```bash
git clone https://github.com/YourUsername/repository_name.git
```

2. **Install UV**

If you're a MacOS/Linux user type:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If you're a Windows user open an Anaconda Powershell Prompt and type :

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. **Create an environment**

```bash
uv venv 
```

3. **Activate the environment**

If you're a MacOS/Linux user type (if you're using a bash shell):

```bash
source ./venv/bin/activate
```

If you're a MacOS/Linux user type (if you're using a csh/tcsh shell):

```bash
source ./venv/bin/activate.csh
```

If you're a Windows user type:

```bash
.\venv\Scripts\activate
```

4. **Install dependencies**:

```bash
uv pip install -r requirements.txt
```

# Questions 
...

# Dataset 
...

## Main dataset issues

- ...
- ...
- ...

## Solutions for the dataset issues
...

# Conclussions
...

# Next steps
...
