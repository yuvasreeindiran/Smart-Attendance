function updateAttendance() {
  fetch('/get_attendance')
    .then(res => res.json())
    .then(data => {
      const table = document.getElementById("attendanceTable");
      table.innerHTML = "<tr><th>Name</th><th>Time</th></tr>";
      data.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${row.name}</td><td>${row.time}</td>`;
        table.appendChild(tr);
      });
    });
}

function startRecognizer() {
  fetch('/start', { method: 'POST' })
    .then(res => res.json())
    .then(data => alert("Recognizer: " + data.status));
}

function stopRecognizer() {
  fetch('/stop', { method: 'POST' })
    .then(res => res.json())
    .then(data => alert("Recognizer: " + data.status));
}
