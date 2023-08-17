# Replicate clone searches, without the preprocessing step, for the Ablation Study

echo 'Ablation study clone searches, without the preprocessing step'
echo 'Takes around 285 hours roughly divided by the number of cores used (40), thus between 7 hours and 18 hours'



echo 'Basic dataset'
echo 'Takes 1 minute'

cd PSS/
python3 RunMakeMD3.py
python3 RunMakeMD.py
cd ../

echo 'BinKit dataset'
echo 'Takes around 220 hours roughly divided by the number of cores used (40)'

cd BinKit/Normal/Ablation
bash ExtractCopyEMBEDS.sh
python3 Run.py
rm -r EMBEDS
python3 Read.py > NORMAL_RESULTS_ABLATION.txt
python3 ReadElapsed.py
cp NORMAL_RESULTS_ABLATION.txt ../../Redaction/Ablation
cp ELAPSED_SCs_Ablation_NORMAL ../../Redaction/Ablation
cd ../../../


cd BinKit/Obfus/Ablation
bash ExtractCopyEMBEDS.sh
python3 Run.py
rm -r NORMAL_EMBEDS_2
rm -r OBFUS_EMBEDS
python3 Read.py > OFBUS_RESULT_ABLATION.txt
python3 ReadElapsed.py
cp OFBUS_RESULT_ABLATION.txt ../../Redaction/Ablation
cp ELAPSED_SCs_Ablation_OBF ../../Redaction/Ablation
cd ../../

cd Redaction/Ablation
cat NORMAL_RESULTS_ABLATION.txt <( echo) OFBUS_RESULT_ABLATION.txt > RESULTS.txt
cd ../../../

echo 'IoT dataset'
echo 'Takes around 4 hours roughly divided by the number of cores used (40)'

cd IoT/XP_Ablation
bash ExtractCopyEMBEDS.sh
python3 Run.py
rm -r EMBEDS
cd ../../

echo 'Windows dataset'
echo 'Takes around 60 hours roughly divided by the number of cores used (40)'

cd Windows/XP_Ablation
bash ExtractCopyEMBEDS.sh
python3 Run.py
rm -r EMBEDS
cd ../../

