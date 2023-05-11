const requestOptions = {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: 'https://www.youtube.com/watch?v=BlGyAH5NSKQ',
};

fetch('/summarize', requestOptions)
  .then((response) => response.json())
  .then((data) => console.log(data.summary))
  .catch((error) => console.log(error));
