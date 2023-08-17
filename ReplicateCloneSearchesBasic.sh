# Replicate clone searches, without the preprocessing step, for the Basic Dataset
echo 'Basic dataset clone searches, without the preprocessing step'
echo 'Takes around 5650 hours roughly divided by the number of cores used (usually 40), thus between 140 hours and 350 hours'

echo 'Alpha Diff'
echo '650 hours roughly divided by the number of cores (40)'
cd AlphaDiff/AD_gDist/
python3 Run.py
cp BO/*_* ../makeResults/BO/
cp BV/*_* ../makeResults/BV/
cp UO/*_* ../makeResults/UO/
cp UV/*_* ../makeResults/UV/
cp CO/*_* ../makeResults/CO/
cp CV/*_* ../makeResults/CV/
cd ../AD_gDistC/
python3 Run.py
cp BOC/* ../makeResults/BOC/
cd ../makeResults/
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../../

echo 'ASCFG'
echo '1 minute'
cd ASCFG/
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'ASCG'
echo '1 minute'
cd ASCG/
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'Asm2Vec'
echo '150 hours roughly divided by the number of cores (40)'
cd Asm2vec/gDist/
cd ASM_BO_gDist/
unzip vecByIds.zip
python3 Run.py
cd ../ASM_BV_gDist/
python3 Run.py
cd ../ASM_UO_gDist/
python3 Run.py
cd ../ASM_UV_gDist/
python3 Run.py
cd ../ASM_CO_gDist/
python3 Run.py
cd ../ASM_CV_gDist/
python3 Run.py
cd ../
python3 makeFinalMatrix.py
python3 makeFinalMatrixElapsed.py
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../../

echo 'CGC'
echo '170 hours roughly divided by the number of cores (30)'
cd CGC/
python3 Run.py
python3 RunCorrect.py
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'Function Set'
echo '5 minutes'
cd FunctionSet/
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'GED-0'
echo '80 hours divied by the number of cores (40)'
cd GED-0/
python3 Run.py
python3 RunCorrect.py
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'GED-L'
echo '50 hours divied by the number of cores (40)'
cd GED-L/
python3 Run.py
python3 RunCorrect.py
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'Gemini'
echo '100 hours divied by the number of cores (40)'
cd Gemini/gDist/
mkdir BO/
mkdir BV/
mkdir UO/
mkdir UV/
mkdir CO/
mkdir CV/
cp ../cleanEmbbeds/BO_vecByIdC BO/vecById
cp ../cleanEmbbeds/BV_vecByIdC BV/vecById
cp ../cleanEmbbeds/UO_vecByIdC UO/vecById
cp ../cleanEmbbeds/UV_vecByIdC UV/vecById
cp ../cleanEmbbeds/CO_vecByIdC CO/vecById
cp ../cleanEmbbeds/CV_vecByIdC CV/vecById
python3 Run.py
cp BO/*_* ../makeResults/BO/
cp BV/*_* ../makeResults/BV/
cp UO/*_* ../makeResults/UO/
cp UV/*_* ../makeResults/UV/
cp CO/*_* ../makeResults/CO/
cp CV/*_* ../makeResults/CV/
cd ../makeResults/
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'Heuristics'
echo '1 minute'
cd heuristics/
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'LibDB'
echo '16 hours roughly divided by the number of cores (default : 40)'
cd LibDB/
python3 RunMakeMD.py
cd ../

echo 'LibDB (specific computations for RQ3 robustness)'
echo '16 hours roughly divided by the number of cores (default : 40)'
cd LibDB_Robustness/
python3 RunMakeMD.py
cd ../

echo 'LibDX'
echo '5  minutes'
cd LibDX/
python3 RunMakeMD.py
cd ../

echo 'MutantX-S'
echo '1  minute'
cd MutantX-S/
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'PSS'
echo '1  minute'
cd PSS/
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../


echo 'PSSO'
echo '1  minute'
cd PSSO/
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'SAFE'
echo '700 hours roughly divided by the number of cores (40)'
cd SAFE/S_gDist/
python3 Run.py
cp BO/*_* ../makeResults/BO/
cp BV/*_* ../makeResults/BV/
cp UO/*_* ../makeResults/UO/
cp UV/*_* ../makeResults/UV/
cp CO/*_* ../makeResults/CO/
cp CV/*_* ../makeResults/CV/
cd ../S_gDistC/
python3 Run.py
cp BOC/*_* ../makeResults/BOC/
cd ../makeResults
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'Shape'
echo '5  minutes'
cd Shape/
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'SMIT'
echo '3700 hours roughly divided by the number of cores (40)'
cd SMIT/
cd NBHA/
gcc main.c -O3 -o ../NBHAE
cd ../
python3 Run.py
python3 RunMakeMD3_NewComputations.py
python3 RunMakeMD.py
cd ../

echo 'StringSet'
echo '1 minute'
cd StringSet/
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

