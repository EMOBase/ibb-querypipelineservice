curl -X 'POST' \
  'localhost:5000/pipeline' \
  -H 'accept: text/csv' \
  -H 'Content-Type: multipart/form-data' \
  -F 'data=string' \
  -F 'steps=[{
  "input": "a",
  "output": "b"
},{
  "input": "b",
  "output": "c"
}]'
