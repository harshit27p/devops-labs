# Isolation Forest

Isolation Forest is an unsupervised anomaly-detection algorithm. It isolates observations using random feature splits; unusual points tend to be isolated with shorter paths.

```python
import pandas as pd
from sklearn.ensemble import IsolationForest

data = pd.DataFrame({
    "errors": [1, 2, 1, 3, 2, 1, 45, 2, 1, 3],
    "warnings": [4, 5, 3, 4, 6, 4, 30, 5, 4, 3],
    "latency_ms": [120, 130, 115, 140, 135, 125, 1800, 128, 122, 138],
})

model = IsolationForest(
    n_estimators=200,
    contamination=0.1,
    random_state=42,
)
labels = model.fit_predict(data)
data["anomaly"] = labels == -1
print(data)
```

`contamination` is an estimate of the proportion of outliers in the training data and influences the decision threshold. It is not a universal “accuracy” setting. Tune and evaluate it for the data and use case.

The tiny dataset is illustrative only. Real models need more observations, representative operating periods and evaluation.
