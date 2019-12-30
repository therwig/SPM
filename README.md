# SPM
ScanPlotMaker
TODO -- add a brief description of the package functionality here

# Running instructions

## Importing data cards

One can run on top of the data cards produced with the SUSY-Interface via the command
```
cd <SPM directory>
python run.py <model> -i <data card directory>
```
where `<model>` denotes the name of the model defined in `<SPM directory>/env/models` and `<data card directory>` the path to the scan directory produced by the SUSY- Interface containing the data cards.
The expected format of the directory is 
`<importPath>/<region>/<lumi>/<model>/<point>/sig_<model>_<point>/<SRname>.card.txt`

## Computing limits

Limits are computed using the [HiggsCombine](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/) tool.

