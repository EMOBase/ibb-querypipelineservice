curl -X 'POST' \
  'localhost:5000/pipeline' \
  -H 'accept: text/csv' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@fbgn.txt' \
  -F 'steps=[{
  "input": "a",
  "output": "b"
},{
  "input": "b",
  "output": "c"
}]'
