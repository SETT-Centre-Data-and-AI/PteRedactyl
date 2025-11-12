<p align="center">
  <img src="docs/images/pteredactyl.png" alt="PteRedactyl", width=300>
</p>


# PteRedactyl

_**PteRedactyl utilizes advanced natural language processing techniques to identify and anonymise personal information in clinical free text.**_

Developed by the **Data & AI Research (DAIR) Unit** at University Hospital Southampton NHSFT for use in clinical research, PteRedactyl wraps around swappable NER models to redact or hide PII in strings or DataFrames.

**Features**

- **Anonymisation** of various entities such as names, locations, and phone numbers.
- Support for processing both **strings** and pandas **DataFrames**.
- **Text highlighting** for easy identification of anonymised sections.
- Hide in plain site (**HIPS**) replacement

## ⚙️ Installation
### Via PyPI
Execute:
```
pip install pteredactyl
```

### Via GitHub (`uv`)
To install in development mode, we recommend using uv.

1) Install uv from the [Astral website](https://docs.astral.sh/uv/getting-started/installation/), or install via PyPI with `pip install uv`

2) Clone the PteRedactyl repo:
```
git clone https://github.com/SETT-Centre-Data-and-AI/pteredactyl.git
```

3) Navigate to the repositry (`cd ...\pteredactyl\`) and execute:
```
uv sync --group dev
```

## 📚 Guides

* [User Guide](./docs/user-guide.md)


# 🤝 Contributing
Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

# ⚖️ License
This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].
[![CC BY-NC 4.0][cc-by-nc-shield]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg
[SETT]: https://github.com/SETT-Centre-Data-and-AI

# 🧑‍🔬 Authors
Valediction was developed by Cai Davis and Michael George at University Hospital Southampton NHSFT's Data & AI Research Unit (DAIR) - part of the [Southampton Emerging Therapies and Technology (SETT) Centre][SETT].
<p align="center">
  <a href="https://github.com/SETT-Centre-Data-and-AI">
    <img src="docs/images/SETT Header.png" alt="NHS UHS SETT Centre">
  </a>
</p>"# PteRedactyl_development" 
