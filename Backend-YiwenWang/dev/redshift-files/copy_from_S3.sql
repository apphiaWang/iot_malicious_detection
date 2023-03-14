copy emulate_data from 's3://iot23emulation/emulationdata/connlog34.csv' 
iam_role 'arn:aws:iam::374296686743:role/RedshiftS3Full'
ignoreheader as 1 
maxerror 10
csv;