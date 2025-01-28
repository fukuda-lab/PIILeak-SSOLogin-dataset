# Investigating PII Leakage through SSO Logins

## Overview

This repository contains data and resources associated with the paper titled "I never willingly consented to this! Investigate PII leakage via SSO logins". The study aims to analyze the potential leakage of Personally Identifiable Information (PII) through Single Sign-On (SSO) mechanisms, specifically focusing on two Identity Providers (IdPs): Login with Google and Login with Facebook.

## Data Description

The dataset includes data extracted from web traffic during the SSO login process. It consists of the following:

- **Raw Dataset:** 
  - Format: `*.sqlite`
  - Contains complete web traffic data during SSO logins.

- **Input Data:**
  - Format: `*.CSV`
  - Contains only requests that include leakage entities.

- **Output Data:**
  - Analysis results derived from the input data.

## Getting Started

### Prerequisites

To analyze the data, you will need the following:

- Python 3.x
- Necessary python libraries: pandas, sqlite3, tldextract, adblockparser

### Data Analysis
**Step 1: Load the Raw Dataset**

Please download raw dataset in /raw_dataset

**Step 2: Identify Leakage Entities and Detect for Leakage**

PII Entities are defined in `DetectPIILeak.py`, included Email, Username, SSO ID.

Run: `python DetectPIILeak.py`

Output: Adhoc file with format `*.csv.gz`, contains only requests that include leakage entities _(adhoc dataset)_.

Notes: This proccess include the detection of third-party tracking requests.

**Step 3: Exclude third-party domains belongs Google and Meta**

Run: `python _get_3rd.py` to export the list receivers from Adhoc files.

Run: `./ghostery.sh` to identify Organization and Category of these receivers that exported. The output is stored at \input\Ghostery\

Run: `python _exclude_ecosystem.py' to filter and exclude the requests send to third-party domains belongs Google and Meta. The out is stored at \input\Japan\ _(excluded dataset)_

**Step 4: Data analysis**

Following these scripts to analysis:

**Using the _excluded dataset_**

4.1 `_breakdown_3rd_domains.py`: Breakdown of third-party domains involved. The output is the number of first-party domains sending PII to each listed third-party domain.

4.2 `_breakdown_pii_leak.py`: Breakdown of PII leakage to third-party domains. Percentages are given out of a total of unique senders (first-party domains) and unique receivers (third-party domains) for each SSO login.

4.3 `_breakdown_combine.py`: Breakdown of the number of first-party domains that share PII to third-party domain by combining. Notes that the inputs of 4.3 are the outputs of 4.2.

**Using the _adhoc dataset_**

4.4 `_breakdown_3rdOfGG_Meta.py`: Breakdown of the number of first-party that send PII to third-party domains belonging to Google and Meta.

4.5 `_breakdown_blocklist`: Breakdown of Ads/tracking entities receiving PII from first-party domains for Google logins and Facebook logins.

4.6 `_breakdown_chain`: Analysis the chains of PII leakage requests. Outputs are visualized in HTML files.

4.7 `_breakdown_countries`: Breakdown of PII leakage in Japan, Germany, and the United States.
