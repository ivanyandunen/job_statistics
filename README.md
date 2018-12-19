# Programming vacancies compare

This script allows to get vacancies information for the last month about the most popular programming languages(Number and average salary) from sites [Headhunter](https://hh.ru/) and [SuperJob](https://www.superjob.ru/) in Saint-Petersburg.

## How to install

Python 3 has to be installed. You might have to run python3 instead of python depending on system if there is a conflict with Python2. Then use pip (or pip3) to install dependencies:

```commandline
pip install -r requirements.txt
```

To use SuperJob API it is necessary to [register](https://api.superjob.ru/register/) and get Secret Key

like: `v2.r.11083112.46dc036c279f861230b0607af8233d0235c309bc60072cdbde348f9aae16cce9.303351.1547294661.144e4e65b9ebd7f9fa3ec2ff68188fb8f5088f2a`

Save it to file .env in the same directory with the script.
`TOKEN=v2.r.11083112.46dc036c279f861230b0607af8233d0235c309bc60072cdbde348f9aae16cce9.303351.1547294661.144e4e65b9ebd7f9fa3ec2ff68188fb8f5088f2a`.

Then run `python job_statistics.py`

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org).