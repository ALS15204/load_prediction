<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- INTRODUCTION -->
## Introduction

This repo is prepared to share my forecasting code that predicts the hourly charge load in 2008 based on the historical 
load data and weather information. There are two sets of data that are used in the training:

* [`amperon_ds_data 2/load_hist_data.csv`](https://github.com/ALS15204/load_prediction/blob/28e8ce61ecef660e5d0ff9e3f728a2c8e2fbb2c2/amperon_ds_data%202/load_hist_data.csv): this file records hourly load data from 2005 to 2007
* [`amperon_ds_data 2/weather_data.csv`](https://github.com/ALS15204/load_prediction/blob/28e8ce61ecef660e5d0ff9e3f728a2c8e2fbb2c2/amperon_ds_data%202/weather_data.csv): this file records hourly temperature data from 2005 to 2007

The final answer is recorded in [`amperon_ds_data 2/output/probability_estimates.csv`](https://github.com/ALS15204/load_prediction/blob/28e8ce61ecef660e5d0ff9e3f728a2c8e2fbb2c2/amperon_ds_data%202/output/probability_estimates.csv)

I describe the steps I took in [the Jupyter notebook](https://github.com/ALS15204/load_prediction/blob/28e8ce61ecef660e5d0ff9e3f728a2c8e2fbb2c2/notebook/load_prediction.ipynb)

<!-- INSTALLATION -->
## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ALS15204/load_prediction.git
   ```
2. Build venv: under the repo root
   ```sh
   python3 -m venv ./
   ```
3. Install requirements
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE -->
## Usage

### Running Jupyter notebook
1.  To use Jupyter note book under the newly built venv
    ```shell
    python -m ipykernel install --user --name=venv
    ```
2. Go to the Jupyter notebook to run it

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- REFERENCES -->
## References

I used the following references when building the model 
1. [US Federal Holidays](https://www.timeanddate.com/holidays/us/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Ronin Wu, PhD - [@RoninWu](https://twitter.com/RoninWu) - ronin@ronin-wu.com

Project Link: [https://github.com/ALS15204/load_prediction](https://github.com/ALS15204/load_prediction)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

I sincerely thank Dr. Abe Stanway, the CTO of Amperon for sharing the data with me. It has been a fun exercise :)