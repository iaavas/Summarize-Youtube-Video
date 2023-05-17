const content = document.getElementById('summary');

const smry = document.getElementById('getSmry');

smry.addEventListener('click', () => {
  const my_link = document.getElementById('my_link').value;

  const data = { link: my_link };

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  };
  let summary;

  const summarizeIt = async () => {
    const res = await fetch('http://127.0.0.1:5000/', requestOptions);

    const summaryJSON = await res.json();

    summary = summaryJSON.summary;

    content.innerText = summary;
    subtitle.innerText = subtitles;
    my_link.value = '';
  };

  summarizeIt();
});
