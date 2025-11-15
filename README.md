# RealEstateMiner

RealEstateMiner is a Python-based web crawler for collecting real estate advertisements from [realestate.com.au](https://www.realestate.com.au/buy/). It allows users to fetch advertising URLs, retrieve content, check for dead links, and save the data efficiently.

---

## Features

* Fetch all advertising URLs.
* Retrieve advertising content.
* Save links or contents locally.
* Check and save URLs returning 404 (dead links).
* Update existing URLs or content.
* Support for multiple countries.
* Verbose mode for detailed logs.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/JafaDsX/RealEstateMiner.git
cd RealEstateMiner
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Project Structure

```
RealEstateMiner
├── README.md
├── RealEstateMiner
│   ├── app
│   │   └── app.py
│   ├── data
│   │   ├── processed
│   │   └── raw
│   │       ├── CR-advertise-urls.csv
│   │       ├── CR-advertise-urls.txt
│   │       ├── US-advertise-urls.csv
│   │       └── US-advertise-urls.txt
│   ├── data-crawler
│   │   ├── base.py
│   │   ├── get_content.py
│   │   ├── get_urls.py
│   │   ├── main.py
│   │   ├── __pycache__
│   │   └── storage.py
│   └── notebooks
│       ├── 01-data-understanding.ipynb
│       ├── 02-data-preprocessing.ipynb
│       ├── 03-modeling.ipynb
│       ├── 04-evaluation.ipynb
│       └── 05-text-mining.ipynb
└── requirements.txt
```

---

## Usage

Navigate to the `data-crawler` directory and run the main script:

```bash
cd RealEstateMiner/data-crawler
python main.py --help
```

### Available Options

| Option                                    | Description                                                     |
| ----------------------------------------- | --------------------------------------------------------------- |
| `-h, --help`                              | Show help message and exit                                      |
| `-fu, --fetch-urls`                       | Get all advertising URLs                                        |
| `-fc, --fetch-contents`                   | Get all advertising contents                                    |
| `-c COUNTRY, --country COUNTRY`           | Specify country (e.g., US, CR)                                  |
| `-s, --storage`                           | Save links or contents                                          |
| `-v, --verbose`                           | Enable verbose mode for detailed logs                           |
| `-dl DEAD_LINKS, --dead-links DEAD_LINKS` | Check all URLs and save those that return a 404 (dead) response |
| `-uu, --update-urls`                      | Update existing URLs                                            |
| `-uc, --update-contents`                  | Update existing content                                         |

---

## Example Commands

Fetch all URLs for Australia and save them:

```bash
python main.py --fetch-urls --country AU --storage
```

Fetch all content and update existing data:

```bash
python main.py --fetch-contents --update-contents
```

Check dead links and save them:

```bash
python main.py --dead-links dead-links.txt
```

Enable verbose mode for detailed logs:

```bash
python main.py --fetch-urls --verbose
```

---

## Data Storage

* Raw URLs are saved in `data/raw/` per country.
* Processed data can be saved in `data/processed/`.
* Dead links are stored in `dead-links.txt`.

---

## Notes

* Make sure to respect website's robots.txt rules and rate limits when crawling.
* Use the country option to organize and separate data.

---

## License

MIT License
