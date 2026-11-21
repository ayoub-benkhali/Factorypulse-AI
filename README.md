# \# FactoryPulse AI

# 

# FactoryPulse AI is an industrial predictive maintenance prototype. It explores two questions: \*\*under which operating conditions are machine failures more frequent, and how well can a model detect them?\*\*

# 

# The project follows 10,000 synthetic machine observations from a source CSV through a PostgreSQL data warehouse to an interactive Power BI dashboard. A Python classification model and a Streamlit app let users inspect prediction errors and test individual operating conditions.

# 

# !\[FactoryPulse AI maintenance dashboard showing failure KPIs and operating conditions](docs/dashboard-overview.png)

# 

# \[Open the Power BI report](powerbi/FactoryPulse.pbix)

# 

# \## Dashboard and KPIs

# 

# | KPI | DAX measure | Full dataset |

# | --- | --- | ---: |

# | Observations | `COUNTROWS('dw fact\_machine\_observation')` | 10,000 |

# | Observed failures | `SUM('dw fact\_machine\_observation'\[machine\_failure])` | 339 |

# | Failure rate | `DIVIDE(\[Pannes observées], \[Nombre d'observations])` | 3.39% |

# 

# The product type filter updates all three KPIs. The dashboard also includes a speed × torque matrix, a breakdown of failures by tool wear, and failure-rate comparisons by temperature gap and product type.

# 

# Two findings illustrate how to read the report:

# 

# \- \*\*Temperature gap.\*\* Observations with a process-to-air temperature gap below 9 K had a 10.24% failure rate, compared with 3.39% overall.

# \- \*\*Product type.\*\* Type L had a 3.92% observed failure rate, compared with 2.09% for type H. These figures describe the synthetic dataset.

# 

# The tool-wear donut shows how the 339 failures are distributed across wear bands. The matrix answers a different question: among observations in a given speed and torque band, what percentage experienced a failure? Observation counts alongside the rates show how much data supports each comparison.

# 

# \## Data pipeline

# 

# 1\. \*\*Extract.\*\* Read the AI4I 2020 source CSV and retain the original file in `data/raw`.

# 2\. \*\*Load.\*\* Import the 10,000 source observations into PostgreSQL.

# 3\. \*\*Transform.\*\* Use SQL to calculate the difference between process and air temperature, group measurements into operating bands, populate five dimensions, and link each observation to its dimension keys.

# 4\. \*\*Validate.\*\* Reconcile the CSV, warehouse, and unfiltered Power BI report against the same totals: 10,000 distinct observations, 339 failures, and a 3.39% failure rate.

# 

# The warehouse pipeline uses an \*\*ELT\*\* sequence because the SQL transformations run in PostgreSQL after the source data is loaded.

# 

# \[Browse the SQL scripts](sql)

# 

# \## Data warehouse model

# 

# The PostgreSQL `dw` schema uses a \*\*star schema with one fact table and five dimensions\*\*. The grain of `dw.fact\_machine\_observation` is \*\*one row per source observation\*\*. Each row contains operating measurements, a binary failure flag, and five foreign keys.

# 

# | Dimension | Foreign key in the fact table | Used to analyze |

# | --- | --- | --- |

# | `dw.dim\_product` | `product\_key` | Product types L, M, and H |

# | `dw.dim\_tool\_wear\_band` | `wear\_band\_key` | Tool wear in minutes |

# | `dw.dim\_temperature\_gap\_band` | `temperature\_gap\_band\_key` | Process-to-air temperature gap in kelvin |

# | `dw.dim\_speed\_band` | `speed\_band\_key` | Rotational speed in rpm |

# | `dw.dim\_torque\_band` | `torque\_band\_key` | Torque in Nm |

# 

# Power BI uses five active one-to-many relationships. For example, selecting product type L filters the related fact rows. Both the failure count and the observation count are then calculated for that selection.

# 

# \## Predictive model and Streamlit app

# 

# A scikit-learn logistic regression classifier uses operating measurements to predict the binary `Machine failure` label.

# 

# | Split | Observations | Failures |

# | --- | ---: | ---: |

# | Training | 8,000 | 271 |

# | Test | 2,000 | 68 |

# 

# Because failures are rare, a model that predicted normal operation for every test observation would achieve \*\*96.6% accuracy while missing all 68 failures\*\*. The Streamlit app displays the confusion matrix so users can inspect detected failures, missed failures, and false alarms. A prediction form lets users enter operating values and see the model’s decision.

# 

# The model predicts the failure label for an individual observation. The dataset is synthetic and does not establish how far in advance a real machine failure could be predicted.

# 

# \## Tools

# 

# | Tool | Role |

# | --- | --- |

# | Python and pandas | Explore the source data and prepare model inputs |

# | scikit-learn | Split the data, train the classifier, and evaluate predictions |

# | PostgreSQL and SQL | Store source data, transform measurements, and build the warehouse |

# | pgAdmin | Run SQL and inspect tables, foreign keys, and validation totals |

# | Power BI Desktop and DAX | Model relationships, calculate KPIs, and build the dashboard |

# | Streamlit | Explore results, inspect the confusion matrix, and test predictions |

# | Git and GitHub | Track project milestones and publish the code, report, and preview |

# 

# \## Explore the project

# 

# \- \*\*Power BI:\*\* Open `powerbi/FactoryPulse.pbix` in Power BI Desktop and select a product type to explore the report.

# \- \*\*Warehouse:\*\* Follow the numbered scripts in `sql` to inspect how the source observations become a fact table and five dimensions.

# \- \*\*Streamlit:\*\* From the project root, activate the project’s Python environment and run `python -m streamlit run app.py`.

# 

# \## Data source

# 

# FactoryPulse AI uses the \*\*AI4I 2020 Predictive Maintenance Dataset\*\* from the UCI Machine Learning Repository, licensed under CC BY 4.0.

# 

# \[Dataset and citation](https://doi.org/10.24432/C5HS5C) · \[Dataset license](https://creativecommons.org/licenses/by/4.0/)

