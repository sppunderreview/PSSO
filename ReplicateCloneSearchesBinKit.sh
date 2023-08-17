# Replicate clone searches, without the preprocssing step, for the BinKit Dataset

echo 'BinKiT dataset clone searches'
echo 'Takes around 3150 hours roughly divided by the number of cores used (40), thus between 140 hours and 240 hours'

cd BinKit/

echo 'Normal part'
cd Normal/
mkdir R
unzip EMBEDS.zip
cd EMBEDS/
7z x MUTANTX2.7z
cd ../
python3 Run.py
rm -r EMBEDS
python3 Read.py > NORMAL.txt
python3 ReadElapsed.py
cp NORMAL.txt ../Redaction/
cp ELAPSED_SCs_NORMAL ../Redaction/
cd ../

echo 'Obfuscation part'
cd Obfus/
mkdir R
unzip NORMAL_EMBEDS_2.zip
unzip OBFUS_EMBEDS.zip
python3 Run.py
rm -r NORMAL_EMBEDS_2
rm -r OBFUS_EMBEDS
python3 Read.py > OBFS.txt
python3 ReadElapsed.py
cp OBFS.txt ../Redaction/
cp ELAPSED_SCs_OBF ../Redaction/
cd ../

cd Redaction/
cat NORMAL.txt <( echo) OBFS.txt > RESULTS_2.txt
