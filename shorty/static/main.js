function get_a(text, href) {
    let a = document.createElement('a');
    a.innerText = text;
    a.href = href;

    return a;
}

function get_button(text, href) {
    let button = document.createElement('button');
    button.classList.add("rounded-full", "p-1", "ml-2", "w-50", "bg-sky-600", "text-xs", "text-white");
    if (href !== null) {
        button.appendChild(get_a(text, href));
    } else {
        button.innerText = text;
    }

    return button;
}

function embed(url, stem) {
    let copy_button = get_button("Copy", null);
    copy_button.onclick = function() {
        navigator.clipboard.writeText(url);
        button.innerText = "Copied!";
        setTimeout(function() { button.innerText = "Copy"; }, 650);
    };

    let p = document.createElement('p');
    p.appendChild(get_a(url, url));
    p.appendChild(copy_button);
    p.appendChild(get_button('svg', `qr/${stem}.svg`));
    p.appendChild(get_button('png', `qr/${stem}.png`));

    return p;
}

function validate(url) {
    try {
        let obj = new URL(url);
        return obj.protocol == "http:" || obj.protocol == "https:";
    } catch (_) {}

    return false;
}

async function shorten() {
    let url = document.getElementById('url').value;
    if (!validate(url)) {
        document.getElementById('process').innerHTML = "Invalid URL!";
        return;
    }

    document.getElementById('process').innerHTML = "Shortening...";
    fetch('shorten', {
        method: 'POST',
        body: JSON.stringify({
            'url': url
        }),
        headers: {
            'Accept': 'application/json',
        },
    })
    .then(response => response.json())
    .then(response => {
        let p = embed(response.url, response.stem);
        document.getElementById('process').innerHTML = "";
        document.getElementById('output').appendChild(p);
    });
}
