# Algo Crawler

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Usage

* Install Package

    ```sh
    pip install algo_crawler
    ```

* Crawl Solution

    ```sh
    python3 -m algo_crawler -s BJ -u koosaga
    # {'user_id': 'koosaga', 'problem_codes': ['1000', '1001' ...]
    ```

* Crawl Problem

    ```sh
    python3 -m algo_crawler -s BJ -p 1000
    # {'code': 'LC_1', 'level': '1', 'link': 'https://leetcode.com/problems/two-sum', 'title': 'Two Sum'}
    ```

## Developer Setting

* Developer setting

    ```sh
    pip install -r requirements.txt
    pre-commit install
    ```

* Test

    ```sh
    python3 -m algo_crawler.test
    ```
