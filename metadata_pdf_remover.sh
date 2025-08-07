if [ -z "$1" ]; then
  echo "[ERROR]: You should indicate the file to treat."
  echo "Usage: $0 file.ext"
  exit 1
fi

if [ ! -f "$1" ]; then
  echo "[ERROR]: File doesn't exist."
  exit 1
fi

if [[ "${1,,}" != *.pdf ]]; then
  echo "[ERROR]: File must be .pdf"
  exit 1
fi

clear
echo "--- PDF METADATA REMOVER ---"
echo "File in input: '$1'"

UUID=$(uuidgen)

echo "Running qpdf sanitizer..."
qpdf --linearize --object-streams=generate --stream-data=compress --remove-unreferenced-resources=auto "$1" "$UUID.pdf"

echo "Sanitized"

echo "Deleting metadata with mat2..."

mat2 --lightweight "$UUID.pdf"

mv "$UUID.cleaned.pdf" "$1"
rm "$UUID.pdf"

echo "Metadata removed..."
echo "Reading metadata of cleaned file:"

mat2 --show "$1"
