# mc973-proj1

## Run locally

The test path is set by `TESTS_PATH` environment variable, so you can change if needed. The default path is `./test`.

To run the simulator on all tests on test folder and generate the output files, run:

```
python3 main.py
```

Then check the output files on the test folder. Example: `.test/01/saida0.csv`

## Run with docker

First build the docker image:

```
docker build . -t simulator 
```

Then run the container mounting the local test folder on the container:

```
docker run  -v $(pwd)/test:/app/test simulator
```

* $(pwd)/test -> local folder
* /app/test -> container folder

Then check the output files on the given local folder. Example: `test/01/saida0.csv`

## Checking results

To compare the output with the expected rusult, you can run this bash command:

```
for d in test/*/ ; do
    echo "${d} - delay 0" 
    diff  "${d}esperado0.csv" "${d}saida0.csv"
    echo "${d} - delay 1" 
    diff  "${d}esperado1.csv" "${d}saida1.csv"
done
```