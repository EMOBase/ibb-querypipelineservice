curl -X 'POST' \
  'localhost:5000/pipelines' \
  -H 'accept: text/csv' \
  -H 'Content-Type: multipart/form-data' \
  -F 'data=iB_07402' \
  -F 'steps=[{
  "input": "iB",
  "output": "TC"
}]'
