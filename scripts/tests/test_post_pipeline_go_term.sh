curl -X 'POST' \
  'localhost:5000/pipelines' \
  -H 'accept: text/csv' \
  -H 'Content-Type: multipart/form-data' \
  -F 'data=FBgn0001319
FBgn0001168' \
  -F 'steps=[{
  "input": "FBgn",
  "output": "GO ID"
},{
  "input": "GO ID",
  "output": "GO term"
},{
  "input": "GO ID",
  "output": "GO aspect"
}]'
