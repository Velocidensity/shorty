function getLink (text, href) {
  const a = document.createElement('a');
  a.innerText = text;
  a.href = href;

  return a;
}

function getButton (text, href) {
  const button = document.createElement('button');
  button.classList.add('rounded-full', 'p-1', 'ml-2', 'w-50', 'bg-sky-600', 'text-xs', 'text-white');
  if (href !== null) {
    button.appendChild(getLink(text, href));
  } else {
    button.innerText = text;
  }

  return button;
}

function embed (url, stem) {
  const copyButton = getButton('Copy', null);
  copyButton.onclick = function () {
    navigator.clipboard.writeText(url);
    copyButton.innerText = 'Copied!';
    setTimeout(function () { copyButton.innerText = 'Copy'; }, 650);
  };

  const p = document.createElement('p');
  p.appendChild(getLink(url, url));
  p.appendChild(copyButton);
  p.appendChild(getButton('svg', `qr/${stem}.svg`));
  p.appendChild(getButton('png', `qr/${stem}.png`));
  p.appendChild(getButton('Stats', `${stem}+`));

  return p;
}

function validate (url) {
  try {
    const obj = new URL(url);
    return obj.protocol === 'http:' || obj.protocol === 'https:';
  } catch (_) {}

  return false;
}

async function shorten () {
  const url = document.getElementById('url').value;
  const force = document.getElementById('force').checked;
  if (!validate(url)) {
    document.getElementById('process').innerHTML = 'Invalid URL!';
    return;
  }

  document.getElementById('process').innerHTML = 'Shortening...';
  fetch('api/shorten', {
    method: 'POST',
    body: JSON.stringify({
      url, force
    }),
    headers: {
      Accept: 'application/json'
    }
  })
    .then(response => response.json())
    .then(response => {
      const p = embed(response.url, response.stem);
      document.getElementById('process').innerHTML = '';
      document.getElementById('output').appendChild(p);
    });
}
