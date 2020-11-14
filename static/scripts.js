document.getElementById('files').addEventListener('change', (e) => {
  document.getElementById('form-text').innerText = document.getElementById('files').files.length + " file(s) selected";
})