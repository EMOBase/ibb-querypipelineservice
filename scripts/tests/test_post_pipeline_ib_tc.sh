curl -X 'POST' \
  'localhost:5000/pipelines' \
  -H 'accept: text/csv' \
  -H 'Content-Type: multipart/form-data' \
  -F 'data=iB_07402
iB_00002
iB_00045' \
  -F 'steps=[{
  "input": "iB",
  "output": "TC"
},{
  "input": "iB",
  "output": "larval lethality day 11"
}]'
