# fetch-patents

## About

This utility downloads patents for a given assignee name. It extracts the "brief" (without claims) patent content in HTML and DOCX formats.

## Usage

```
./download-index.sh

./fetch-patents.py Microsoft
```

Replace `Microsoft` with any other assignee name of interest.

## Appendix

To upload the data to an Azure storage account, create two containers named `docx` and `html`, and run:

```
for type in html docx; do az storage blob sync -c $type --account-name $STORAGE_ACCOUNT -s $type; done
```
