

# setup

```python
from setuptools import setup, find_packages
setup(
    name="sentiment-analysis-with-llm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas==1.1.3",
        "streamlit",
        # Add other dependencies as needed
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'run-app=sentiment_analysis_with_llm.app:main',
        ],
    },
)
```


# .toml
```python

[tool.poetry]
name = "sentiment-analysis-with-llm"
version = "0.1.0"
description = "A Streamlit app for analyzing Amazon product reviews."
authors = ["Your Name <you@example.com>"]
license = "MIT"

[tool.poetry.dependencies]
python = "^3.8"
pandas = "1.1.3"
streamlit = "^1.0.0" # Use the latest version compatible with your code

[build-system]
requires = ["poetry>=0.12"]
build-backend = "poetry.masonry.api"
```




