curl -X 'POST' \
  'localhost:5000/pipelines' \
  -H 'accept: text/csv' \
  -H 'Content-Type: multipart/form-data' \
  -F 'data=GO:0035290' \
  -F 'steps=[{
  "input": "GO ID",
  "output": "FBgn"
},{
  "input": "GO ID",
  "output": "TC"
}]'
