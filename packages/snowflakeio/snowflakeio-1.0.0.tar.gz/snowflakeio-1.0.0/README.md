# snowflakeio

<div align="center">

[![Build status](https://github.com/bradleycm/snowflakeio/workflows/build/badge.svg?branch=master&event=push)](https://github.com/bradleycm/snowflakeio/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/snowflakeio.svg)](https://pypi.org/project/snowflakeio/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/bradleycm/snowflakeio/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/bradleycm/snowflakeio/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/bradleycm/snowflakeio/releases)
[![License](https://img.shields.io/github/license/bradleycm/snowflakeio)](https://github.com/bradleycm/snowflakeio/blob/master/LICENSE)

Snowflake IO, a Pythonic Algorithmic Trading Library

</div>


## Installation

```bash
pip install -U snowflakeio
```

or install with `Poetry`

```bash
poetry add snowflakeio
```

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/bradleycm/snowflakeio/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/bradleycm/snowflakeio/blob/master/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/bradleycm/snowflakeio)](https://github.com/bradleycm/snowflakeio/blob/master/LICENSE)

This project is licensed under the terms of the `GNU GPL v3.0` license. See [LICENSE](https://github.com/bradleycm/snowflakeio/blob/master/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{snowflakeio,
  author = {bradleycm},
  title = {Snowflake IO, a Pythonic Algorithmic Trading Library},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/bradleycm/snowflakeio}}
}
```
