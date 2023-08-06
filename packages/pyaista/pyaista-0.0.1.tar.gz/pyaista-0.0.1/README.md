# PyAista

PyAista is a Python package that provides API developers the ability to validate their machine learning models prior to deployment.

## Installation

### Python Compatibility

PyAista is currently compatible with Python 3.6, 3.7, 3.8, and 3.9.

### Using Pip

Install the latest version from PyPI (Windows, Linux, and macOS):

```
pip install pyaista
```

## Introduction

PyAista provides a `BaseDeployment` class for checking if a machine learning model class can be deployment on AISTA. Here is how you would do it:

```python
from pyaista import BaseDeployment
from statistics import mean
from typing import List

class Model(BaseDeployment):
  '''
  A simple machine learning model
  '''

  def main(self, array: List[float]):
    '''
    Main function used by AISTA for model consumption
    '''
    return mean(numeric_input)
```

If you are able to create the `Model` class without any errors, your class is compatible with AISTA and ready to be deployed. Furthermore, you will also be able to add logging locally with `Model.aista_log()`.

```python
from pyaista import BaseDeployment
from statistics import mean
from typing import List

class Model(BaseDeployment):
  '''
  A simple machine learning model
  '''

  def main(self, array: List[float]):
    '''
    Main function used by AISTA for model consumption
    '''
    Model.aista_log(f'Input: {array}')
    return mean(numeric_input)
```
```
>>> Model().main([0, 1])
Input: [0, 1]
0.5
```

Since AISTA relies on the main function for serving your machine learning model, it is required that you implement it. You will get an `AistaError` if you forgot to do so.

```python
from pyaista import BaseDeployment
from statistics import mean
from typing import List

class Model(BaseDeployment):
  '''
  A simple machine learning model
  '''
  def other():
    pass
```
```
pyaista.AistaError: Cannot create class Model. Please implement the main method.
```
