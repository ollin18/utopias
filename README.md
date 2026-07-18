# Evaluating the Reach and Equity of Public Spaces in Mexico City Using Mobility Data: The Case of the Utopías in Iztapalapa

## Abstract

Public space is a vital lever for redistributing urban well-being, yet its success depends entirely on who actually reaches it. Traditional accessibility metrics based on physical proximity or sparse surveys are poorly suited to measure real-world use. By contrast, high-resolution human mobility data from Location-Based Services (LBS) enable direct observation of who actually visits a place, with unmatched spatial and temporal detail. We apply this approach to the Utopías, a network of thirteen community centers offering free recreation, culture, and care, built in Iztapalapa, an underserved periphery of Mexico City, to evaluate whom the network reaches and what distinguishes high-performing sites from those that primarily serve nearby residents. Integrating LBS traces with public transit feeds (GTFS), crime registries, and a comprehensive activity catalog, we show that transport access, service distinctiveness, and safety each act on a distinct dimension of reach. Public transport supply is the strongest correlate of overall visitor volume. Specialized signature attractions do not increase daily footfall but substantially expand geographic catchments, appearing as a pronounced weekend distance premium. The share of violent crime in the surrounding area tracks the socioeconomic composition of visitors rather than their quantity, with vulnerable residents relying on local sites in high-crime areas while wealthier visitors travel to safer, better-connected destinations. Together, these findings establish a baseline for municipal planners to evaluate prospective public spaces.

## Overview

This repository contains the data and analysis for the Utopías paper, a study of who reaches thirteen free recreation, culture and care facilities built by the borough of Iztapalapa on the eastern periphery of Mexico City.

## Study Area

The thirteen Utopías sit within a single borough of about 1.8 million people, which holds the broad urban context roughly constant and lets the variation between sites do the work:

- Olini, Meyehualco, Teotongo, Tezontli, La Cascada, Quetzalcoatl, Libertad, Atzintli, Ixtapalcalli, Cuauhtlicalli, Papalotl, Tecoloxtitlan and Barco.

## Requirements

- Python 3.9+
- See `requirements.txt` for package dependencies

## Key Results

### The network and who it reaches

![The network and who it reaches](figs/network_map.png)

Two flagship sites, Olini and Meyehualco, hold most of the traffic, roughly 2,700 and 1,200 unique visitors out of 4,704 across the network over six months. About fifty-five percent of visitors come from outside Iztapalapa and roughly one in five from the neighbouring municipalities of the State of Mexico, but that metropolitan catchment sits almost entirely at the two largest hubs. The smallest sites draw over ninety percent of their visitors from their immediate surroundings.

### Visits build over the season, not week to week

![Seasonal decomposition of daily visits](figs/ts_stl_decomposition.png)

The trend rises from about twenty unique daily visitors in October to a smoothed peak near sixty in early February before easing. The weekly cycle stays under one visitor per day between weekend and weekday averages, so the sites read as steady everyday hubs rather than weekend destinations.

### Wider catchments come with a more even wealth mix

![Segregation against distance](figs/Sa_vs_distance.png)

Place-level wealth segregation falls as the mean home-to-site distance grows (r = -0.60, p = 0.030). Sites that draw from farther attract a more even mix across the four metropolitan wealth quartiles, while localized sites inherit the narrower socioeconomic profile of their immediate surroundings.

### The service offer tracks travel distance, not volume

![Distinctiveness against the weekend distance premium](figs/distinct_vs_premium.png)

The distinctiveness of a site's offer is unrelated to how many people come (r = 0.05) but tracks how much farther weekend visitors travel (r = 0.68, p = 0.015). Resolving the catalog into service domains, the landmark attractions carry this the hardest (r = 0.91, p < 0.001), while everyday facilities such as fitness and team sports are the ones that track volume.

![Service domains against visit outcomes](figs/heat_domains.png)

### Transit supply is what tracks volume

![Transit score against unique visitors](figs/axis_transit_vs_visitors.png)

Public transport supply is the strongest single correlate of visitor volume (r = 0.64, p = 0.019), while a conventional distance-weighted accessibility index shows no relationship (r = -0.12). The link holds after controlling for services and crime (partial r = 0.65), and a standardized regression of log visits on the three axes gives transit 0.65, services 0.15 and crime -0.02 (R² = 0.44).

### Violence tracks who comes, not how many

![Violent share against visitor wealth](figs/violent_vs_wealth.png)

The volume of surrounding crime is unrelated to visits (r = -0.01). The violent share is what matters, tracking the wealth of who comes (r = -0.75, p = 0.004) and how far they travel (r = -0.64, p = 0.019): poorer and more local visitors at the high-violence sites, wealthier and more mobile ones at the safer, better-connected destinations.

### A typology from the two policy levers

![Access typology](figs/access_typology.png)

Transit access and service distinctiveness are the two levers a planner controls directly. Crossing them splits the network into flagship destinations, connected neighborhood hubs, under-connected attractions and neighborhood spaces.
