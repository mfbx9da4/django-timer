#Django Timer
Lightweight profiling timer for django projects can be installed [via pypi](https://pypi.python.org/pypi?name=django-timer&version=0.1&:action=display)

    pip install django-timer

#Examples

Simplest usage 
```python
with Timer() as timer:
    import time; time.sleep(1) # do something slow
print 'Sleep for 1 second took %.03f secs' % timer.delta
```
```
STDOUT: Sleep for 1 second took 1.003 secs
```

If you provide a message the timer will log the message via the logger with a log level of `INFO`

```python
with Timer('sleep 1') as timer:
    import time; time.sleep(1) # do something slow
```    
```
django.log: [INFO] sleep 1 :: 1.003 secs
```

Print the message to STDOUT as well as log file with `print_message=True`
```python
with Timer('sleep 1', print_message=True) as timer:
    import time; time.sleep(1) # do something slow
```
```
STDOUT: sleep 1 :: 1.003 secs
django.log: [INFO] sleep 1 :: 1.003 secs
```

You can also use the timer as a decorator:
```python
@Timer('my_function')
def my_function(self):
    ....
```

#For contributors
## Build and Upload to Pip

    python setup.py sdist upload -r pypi

## Run tests 

    nosetests 

## Todo:
- Set logging to info by default as an option in settings.py
- config for showing path
