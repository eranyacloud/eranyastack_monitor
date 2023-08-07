## How to Run test?

```
clone project
cd tests
pip install pytest
pytest test_main.py -vv

```

## Correct Output
```
==================================================================================== test session starts ====================================================================================
platform linux -- Python 3.8.10, pytest-7.1.2, pluggy-1.0.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /opt/greenmonitor/tests
plugins: anyio-3.6.1
collected 7 items

test_main.py::test_health_check PASSED                                                                                                                                                [ 14%]
test_main.py::test_getalerts_valid PASSED                                                                                                                                             [ 28%]
test_main.py::test_getalerts_invalid PASSED                                                                                                                                           [ 42%]
test_main.py::test_create_alerts_valid PASSED                                                                                                                                         [ 57%]
test_main.py::test_create_alerts_invalid PASSED                                                                                                                                       [ 71%]
test_main.py::test_get_metrics_valid PASSED                                                                                                                                           [ 85%]
test_main.py::test_get_metrics_invalid PASSED                                                                                                                                         [100%]

===================================================================================== 7 passed in 0.42s =====================================================================================
```
