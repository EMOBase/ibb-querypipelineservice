curl -X 'POST' \
  'localhost:5000/pipelines' \
  -H 'accept: text/csv' \
  -H 'Content-Type: multipart/form-data' \
  -F 'data=TC007020' \
  -F 'steps=[{
  "input": "TC",
  "output": "iB"
}]'
