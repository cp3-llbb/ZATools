To create postFit plots:

cd postFitShapes
./mkdir_inputs.sh (put the path containing your files with the histograms from ZAStatAnalysis)

cd ../postFitPlots
./mkdir_outputs.sh

cd ..
./producePostFitPlots.sh

./moveToSameFolder.sh
