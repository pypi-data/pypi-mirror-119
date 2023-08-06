# orangepipes

A python library to read pipeline environment variables from orange.yml file and apply to OS.

````
orange.yml

... 

pipelines:
  global:
    env:
      APP_NAME: sample
      APP_PORT: 8080    
  app_example:
    env:
      APP_PORT: 3000
...
````

## How to use
Follow [AWS Codeartifact](https://docs.aws.amazon.com/pt_br/codeartifact/latest/ug/using-python.html) steps to configure pip
```
pip install orangepipes
```

```
from orangepipes import pipeline

pipeline.apply_orange_envs()
```