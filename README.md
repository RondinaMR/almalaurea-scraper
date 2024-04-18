# almalaurea-scraper

## Description

This project is a scraper for the italian almalaurea website. It allows you to extract data from the website and store it in a structured format.

## Installation

To install the project, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/almalaurea-scraper.git`
2. Navigate to the project directory: `cd almalaurea-scraper`
3. Install the dependencies (e.g. using Conda): `conda env create -f environment.yml`

## Usage

To use the scraper, follow these steps:

1. Configure the scraper by editing the `scraper.py` file.
2. Run the scraper: `python3 scraper.py`
3. The scraped data will be saved in the `results` directory.

### Main functions

`disaggregation_all(anni, filename=None, ateneo="tutti")`

 * Performs disaggregation for all years.

 * @param {Array} anni - An array of years to perform disaggregation for.
 * @param {string} [filename] - Optional filename to save the disaggregated data.
 * @param {string} [ateneo="tutti"] - Optional parameter to specify the university. Defaults to "tutti" (all universities).


`disaggregazione_genere(anni, filename=None, ateneo="tutti")`

Performs disaggregation for genders.

 * @param {Array} anni - An array of years to perform disaggregation for.
 * @param {string} [filename] - Optional filename to save the disaggregated data.
 * @param {string} [ateneo="tutti"] - Optional parameter to specify the university. Defaults to "tutti" (all universities).

`disaggregazione_dipartimenti(anni, filename=None, ateneo='tutti')`
Performs disaggregation for departments.

> [!WARNING]
> The department list is based on the ones for Politecnico di Torino. Modify the list based on the departments of the university of your interest.

* @param {Array} anni - An array of years to perform disaggregation for.
* @param {string} [filename] - Optional filename to save the disaggregated data.
* @param {string} [ateneo="tutti"] - Optional parameter to specify the university. Defaults to "tutti" (all universities).


 `disaggregazione_lavoro(anni, filename=None, ateneo='tutti')`

 * Performs disaggregation for work conditions.

 * @param {Array} anni - An array of years to perform disaggregation for.
 * @param {string} [filename] - Optional filename to save the disaggregated data.
 * @param {string} [ateneo="tutti"] - Optional parameter to specify the university. Defaults to "tutti" (all universities).


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the [LICENSE](LICENSE) file for more information.