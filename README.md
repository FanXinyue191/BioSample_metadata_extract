# BioSample_metadata_extract
a pipeline that extract infomation of interest from NCBI BioSample database
# web
NCBI BioSample website：https://www.ncbi.nlm.nih.gov/biosample/?term=

BioSample XML download website：https://ftp.ncbi.nlm.nih.gov/biosample/biosample_set.xml.gz

# Usage
Download the biosample_set.xml.gz (~2.6G)
```
wget https://ftp.ncbi.nlm.nih.gov/biosample/biosample_set.xml.gz
```
Gunzip the .gz file (~95G)
```
gunzip biosample_set.xml.gz
```
Run biosample_extractV4.0.py
```
python biosample_extractV4.0.py --input biosample_set.xml --output biosample_extractV4.0.tsv
```
