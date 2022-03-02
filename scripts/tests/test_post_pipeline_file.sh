curl -X 'POST' \
  'localhost:5000/pipelines' \
  -H 'accept: text/csv' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@fbgn.txt' \
  -F 'steps=[{
  "input": "FBgn",
  "output": "FB symbol"
},{
  "input": "FBgn",
  "output": "FB name"
}]'
