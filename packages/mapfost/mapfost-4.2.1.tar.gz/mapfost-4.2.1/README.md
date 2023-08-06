## mapfost

mapfost is a python implementation of the autofocus method MAPFoST introduced in the publication Binding J, Mikula S, Denk W. Low-dosage Maximum-A-Posteriori Focusing and Stigmation. Microsc Microanal. 2013

## Installation

Use the package manager pip to install mapfost

```bash
pip install mapfost
```

## Usage

```python
from src.mapfost import mapfost as mf

res = mf.est_aberr([test_im1, test_im2])
```
## Example

run the script <em>run_sample.py</em>
```python
python <PATH TO SRC>/src/example/run_sample.py
```

Expected output is a scipy.optimize.minimize object (as shown below).\
The <b>x</b> key in the following object is the estimated aberration vector.
```python
fun: -18822048750862.973
hess_inv: <3x3 LbfgsInvHessProduct with dtype=float64>
jac: array([ 3906250.02374012, -5468749.9990838 , -1171875.00061682])
message: 'CONVERGENCE: REL_REDUCTION_OF_F_<=_FACTR*EPSMCH'
nfev: 80
nit: 12
njev: 20
status: 0
success: True
x: array([2.11, 0.05, 0.16])
```


## License
[MIT](https://choosealicense.com/licenses/mit/)