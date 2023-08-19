# Replicate clone searches, without the preprocessing step, for the PSSO Study on the Windows dataset

echo 'PSSO study clone searches, without the preprocessing step'
echo 'Takes around 160 hours roughly divided by the number of cores used (40), thus between 4 hours and 10 hours'


cd Windows/XP_PSSO_Study
7z x EMBEDS.7z
python3 Run.py
rm -r EMBEDS

