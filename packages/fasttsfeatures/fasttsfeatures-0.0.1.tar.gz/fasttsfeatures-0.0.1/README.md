# FastTSFeatures
> Scale the computation of static or temporal time-series.


## Install

`pip install fasttsfeatures`

## How to use

For the moment you need to upload your dataset to s3.
The response will be written in s3 as well.

```python
from fasttsfeatures.core import TSFeatures
```

```python
tsfeatures = TSFeatures()
```

```python
resp = tsfeatures.calculate_features_from_url(url=f's3://tsfeatures-api-public/train.csv', freq=7, kind='static')
```
