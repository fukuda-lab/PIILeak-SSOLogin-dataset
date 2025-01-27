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

Output: Adhoc file with format `*.csv.gz`, contains only requests that include leakage entities.

Notes: This proccess include the detection of third-party tracking requests.

**Step 3:**
