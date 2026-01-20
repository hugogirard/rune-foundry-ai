#### CMD
```
set PYTHONPATH=%cd%
```

#### PS
```
$env:PYTHONPATH = (Get-Location).Path
```

#### BASH
```
export PYTHONPATH=$(pwd)
```