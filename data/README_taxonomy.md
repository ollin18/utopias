# Utopias Facility Taxonomy -- Methodology

## Objective

Create a harmonized and infrastructure-sensitive taxonomy of facilities
offered in Utopias, correcting inconsistent naming and pluralization.

## Step 1 -- Text Normalization

-   Lowercase conversion
-   Accent removal
-   Whitespace standardization

## Step 2 -- Semantic Harmonization

Regular expression rules grouped semantically equivalent items:
Example: - "alberca semiolimpica", "alberca semi-olimpica", "albercas
semiolimpicas" → "Semi-Olympic Swimming Pool" - "huerto urbano", "huerto
sostenible" → "Urban Garden" - "gimnasio de box", "gimnasio de box al
aire libre" → "Boxing Gym"

All categories translated into English.

## Step 3 -- Empirical Rarity

Rarity = 1 − (# of Utopias offering category / Total Utopias)

## Step 4 -- Infrastructure Intensity

Categories classified as: - High (3): Rare, capital-intensive
infrastructure (e.g., Planetarium, Climbing Wall) - Medium (2):
Specialized facilities (e.g., Boxing Gym, Skatepark) - Low (1): Basic or
replicable services (e.g., Arts Workshops)

## Step 5 -- Distinctiveness Weight

Distinctiveness Weight = Rarity × Infrastructure Score

## Step 6 -- Utopia-Level Index

Distinctiveness Index = Sum(Distinctiveness Weight) / Number of
Facilities

This index captures both uniqueness and infrastructural intensity of
each Utopia.

Outputs: - utopias_clean_items_long.csv -
utopias_clean_category_scores.csv -
utopias_clean_distinctiveness_scores.csv
