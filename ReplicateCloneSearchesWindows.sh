# Replicate clone searches, without the preprocessing step, for the Windows Dataset

echo 'Windows dataset clone searches, without the preprocssing step'
echo 'Takes around 600 hours roughly divided by the number of cores used (40, 40 and 6), thus between 55 hours and 140 hours'


cd Windows/

echo 'PSSO'
echo 'Takes around 30 hours roughly divided by the number of cores used (40)'
cd PSSO/
unzip EMBEDS.zip
python3 Run.py
rm -r EMBEDS/
cd ../

echo 'LibDX, Shape, Bsize, Dsize, MutantX-S, PSS, ASCG, FunctionSet'
echo 'Takes around 310 hours roughly divided by the number of cores used (40)'
cd XP/
unzip EMBEDS.zip
cd EMBEDS
unzip PSS.zip
unzip GSA.zip
unzip MUTANTX.zip
cd ../
python3 Run.py
rm -r EMBEDS/
cd ../

echo 'StringSet'
echo 'Takes around 260 hours roughly divided by the number of cores used (6)'
cd StringSet
python3 MakeStringSetEmbeds.py
python3 RunNew.py
rm -r A_STRINGS
rm -r EMBEDS
cd ../
