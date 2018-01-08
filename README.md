Data about the EU emission trading system (ETS). The EU emission trading system (ETS) is one of the main measures introduced by the EU to achieve cost-efficient reductions of greenhouse gas emissions and reach its targets under the Kyoto Protocol and other commitments. The data mainly comes from the EU Transaction Log (EUTL).

## Data

Aggregated data on greenhouse gas emissions and allowances. 

### Geographic coverage

Austria, Belgium, Bulgaria, Croatia, Cyprus, Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, Ireland, Italy, Latvia, Liechtenstein, Lithuania, Luxembourg, Malta, Netherlands, Norway, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden, United Kingdom

### Temporal coverage

2005-2014

### Sources

1. 
  * Name: European Union Emissions Trading System data from EUTL
  * Web: http://www.eea.europa.eu/data-and-maps/data/european-union-emissions-trading-scheme-eu-ets-data-from-citl-7

## Preparation

### Requirements

Python 2 together with modules urllib and zipfile are required in order to process the data. 

### Processing

Run the following script from this directory to download and process the data:

```bash
make
```

### Resources

The raw data are output to `./tmp`. The processed data are output to `./data`.

## License

### Data

Data are sourced from European Environment Agency and no copyright restrictions are applied. More specifically:
> EEA aspires to promote the sharing of environmental data. In agreeing to share, data providers need to have assurance that their data are properly handled, disseminated and acknowledged following similar principles and rules across countries and stakeholders.[*][permissions]

### Additional work

All the additional work done to build this Data Package is made available under the Public Domain Dedication and License v1.0 whose full text can be found at: http://www.opendatacommons.org/licenses/pddl/1.0/


### Citations

1. EEA standard re-use policy: unless otherwise indicated, re-use of content on the EEA website for commercial or non-commercial purposes is permitted free of charge, provided that the source is acknowledged (http://www.eea.europa.eu/legal/copyright). Copyright holder: Directorate-General for Climate Action (DG-CLIMA).

[permissions]: http://www.eea.europa.eu/legal/eea-data-policy
