# halfspace

Simple wrapper around `matplotlib.pyplot` intended support a unified visual language across the organisation.

To build: 
```bash
$ python3 -m build
```

To publish with twine (see guide [here](https://packaging.python.org/tutorials/packaging-projects/)):
```bash
$ python3 -m twine upload --repository testpypi dist/*
```

To build locally:
```bash
$ git clone https://halfspace@dev.azure.com/halfspace/Halfspace/_git/Halfspace
$ pip install -e Halfspace/python/halfspace
```

To use:
```python
import halfspace
f = halfspace.figure()
f.errorbar(x, y, ey, ls='none', marker='.', label='Data')
f.plot(x, fit(x), '-', label='Fit')
f.title('This is an example plot')
f.xlabel("Independent variable", "A bit of context, or some details")
f.ylabel("Dependent variable", "Some description here")
f.legend()
f.logo()
f.savefig('figure.pdf') 
```

Example outputs:
![](./images/light.png)
![](./images/dark.png) 
