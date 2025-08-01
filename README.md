# Project: The "Moneyball" Successor - Finding a Replacement for Matheus Cunha

**Author:** Chadrick Clarke
**Date:** July, 2025
**Contact:** [www.linkedin.com/in/chadrickclarke](https://www.linkedin.com/in/chadrickclarke/)

---

## 1. Business Problem

In the summer of 2025, Wolverhampton Wanderers sold their key forward, Matheus Cunha, to Manchester United for a reported fee £62.5 million. This project simulates a real-world task for the Wolves recruitment team: **to identify a statistically similar, high-potential, and undervalued replacement for Cunha using a data-driven approach.**

The primary goal is to generate a shortlist of 3-5 players who can replicate Cunha's unique role as a ball-progressing, creative, and hard-pressing forward, all while operating under the tight financial constraints typical of a club like Wolves.

## 2. Data Sources

*   **Player Performance Data:** To be scraped from [FBRef](https://fbref.com/) for the 2023-24 season across Europe's top 7 leagues.
*   **Market Value & Contract Data:** To be scraped from [Transfermarkt](https://www.transfermarkt.com/).

## 3. Methodology

This project will follow a three-phase approach:

1.  **Data Pipeline & Feature Engineering:**
    *   Design Database Schema
    *   Construct database in Docker, Postgres SQL
    *   Develop Python scripts to scrape, clean player data and populate database
    *   Engineer key performance metrics, normalizing stats on a per-90-minute basis and applying Possession Adjustment (PAdj) to defensive actions for fair comparison.
    *   Establish a multi-faceted benchmark profile for Matheus Cunha based on 15 key metrics (e.g., npxG+xAG, Shot-Creating Actions, Progressive Carries, Pressures in Attacking Third).

2.  **Similarity Modeling:**
    *   Use **Cosine Similarity** to measure the statistical likeness of every player in the dataset to Cunha's benchmark profile. This will provide a ranked list of potential replacements based purely on playing style and output.
    *   Utilize **Principal Component Analysis (PCA)** for dimensionality reduction to visualize player profiles and validate the similarity model's findings.

3.  **Shortlisting & Reporting:**
    *   Filter the similarity rankings based on realistic constraints for Wolves [eg. Age (< 25 years) and Market Value (< €15m)]
    *   The top candidates form the final shortlist, will be presented in a mock scouting report.


## 4. Key Findings & Results

The final analysis to be produced will deliver a shortlist of three high-potential players who represent excellent value. 