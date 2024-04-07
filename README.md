<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
[![LinkedIn][linkedin-shield]][linkedin-url]
<!-- PROJECT LOGO -->
<br />
<div align="center">
<h1 align="center">@profile</h1>
  <p align="center">
    Simplifies Method Profiling
  </p>
</div>

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The profile decorator is designed for easy profiling of Python functions, 
leveraging the built-in cProfile and pstats modules for performance analysis.
It provides a flexible way to output profiling information either to the
standard output, logger or to a file and allows for sorting of profiling data
based on various criteria.

The decorator is designed to be a "no frills" implementation of CProfile that saves you time. Just add
it to a method, call your endpoint or run your script, and see the output.

## Features
Features
Seamless Integration: Just decorate functions you wish to profile without altering their implementation.
- Flexible Output Options: Choose to print the profiling results to stdout, a logger or save them to a file for further analysis.
- Customizable Sorting: Sort profiling results by criteria like 'cumulative time', 'number of calls', and more, to focus on the most relevant performance metrics.
- Adjustable Detail Level: Control the amount of information displayed through optional parameters, tailoring the output to your needs.
## Prerequisites

There are no external dependancies, profiling is done using the standard library
package `CProfile`.

## Installation

Install the package
   ```sh
   pip install profiling-decorator
   ```

<!-- USAGE EXAMPLES -->
## Usage

Import the profile decorator:

```python
from profiling_decorator import profile
```

#### Basic Usage

Basic Usage
To use the decorator without any customization, simply decorate your function.
By default, it profiles the function, sorts the results by cumulative time, 
and prints the results to standard output.
```python
@profile
def example_function():
    # Function code to profile
    pass

example_function()
```

### Limiting Output
Limit the profiling output to a specific number of rows to focus on the top time-consuming operations.
```python
@profile(n_rows=10)
def example_function():
    # Function code to profile
    pass

example_function()
```
### Changing Sort Criteria
Customize the sorting criteria of the profiling report (e.g., by number of calls).
```python
@profile(sort_by="calls")
def example_function():
    # Function code to profile
    pass

example_function()
```
#### Valid Sort Options
The valid options for the sort_by parameter align with the SortKey attributes in the pstats module and include:

- 'cumulative' - Total time spent in the function and all sub-functions (default).
- 'time' - Internal time spent in the function (excluding sub-functions).
- 'calls' - Number of calls to the function.
- 'ncalls' - Same as calls, but distinguishes between direct and indirect calls.

See the pstats module for a complete up to date list.

### Output to File
To save the profiling results to a file, specify the output and filename parameters.
```python
@profile(output='file', filename='profile_stats.txt')
def example_function():
    # Function code to profile
    pass

example_function()
```
#### Output Options
- 'stdout' - Print the profiling results to standard output (default).
- 'file' - Write the profiling results to a file. Requires specifying the filename parameter.
- 'log' - Log the profiling results using the configured logging system. This is useful for integrating profiling results into application logs. 

#### Configuring Logging
Before using the log output option, ensure the logging system is configured to handle messages at the INFO level or lower. Here's a basic configuration example:
```python
import logging

logging.basicConfig(level=logging.INFO)

@profile(output='log')
def example_function():
    # Function code to profile
    pass

example_function()
```
### Async Support
The profile decorator is enhanced to support profiling of both synchronous and asynchronous 
functions. This feature allows developers to gain insights into the performance characteristics 
of their code, whether it operates synchronously or leverages Python's asyncio for 
asynchronous execution.

Usage is identical:
```python
@profile
async def async_function():
    # Async function code to profile
    await some_async_operation()

await async_function()
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the Apache Software License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Joshua Brumpton - ja.brumpton@gmail.com

Project Link: [github repo](https://github.com/CTPassion/profiling-decorator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/joshua-brumpton-8a6bb619b/
