async function findProfessor() {
  const name = document.getElementById('profName').value;
  if (!name) return alert('Type a name');
  const res = await fetch(`http://127.0.0.1:8000/api/find_professor?name=${encodeURIComponent(name)}`);
  const data = await res.json();
  document.getElementById('result').innerText = JSON.stringify(data, null, 2);
}

async function askChat() {
  const q = document.getElementById('chatQuery').value;
  if (!q) return alert('Type a question');
  const res = await fetch('http://127.0.0.1:8000/api/chat', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({query: q})
  });
  const data = await res.json();
  document.getElementById('chatResult').innerText = JSON.stringify(data, null, 2);
}
