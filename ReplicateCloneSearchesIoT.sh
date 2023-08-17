# Replicate clone searches, without the preprocessing step, for the IoT Dataset

echo 'IoT dataset clone searches, without the preprocessing step'
echo 'Takes around 31 hours roughly divided by the number of cores used (40), thus between 1 hours and 3 hours'

cd IoT/

echo 'MutantX-S and PSSO'
echo 'Takes around 6 hours roughly divided by the number of cores used (40)'
cd MutantXSV2_PSSO/
cd EMBEDS/
unzip MUTANTX2.zip
cd ../
python3 RunV2.py
rm EMBEDS/MUTANTX2
cd ../

echo 'Bsize, Dsize, Shape, ASCG, PSS, LibDX, StringSet, FunctionSet'
echo 'Takes around 25 hours roughly divided by the number of cores used (40)'
cd XP/
7z x EMBEDS.7z
python3 Run.py
rm -r EMBEDS
