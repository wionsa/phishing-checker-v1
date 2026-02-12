function createCheckButton() {
  if (document.getElementById("phishing-check-button")) return;

  const btn = document.createElement("button");
  btn.textContent = "🔍 Перевірити на фішинг";
  btn.id = "phishing-check-button";

  // Новий стиль
  btn.style.position = "fixed";
  btn.style.top = "80px";
  btn.style.right = "20px";
  btn.style.zIndex = 1000;
  btn.style.padding = "12px 20px";
  btn.style.background = "linear-gradient(135deg, #4CAF50, #2E7D32)";
  btn.style.border = "none";
  btn.style.borderRadius = "8px";
  btn.style.color = "white";
  btn.style.fontSize = "16px";
  btn.style.fontWeight = "bold";
  btn.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.2)";
  btn.style.cursor = "pointer";
  btn.style.transition = "transform 0.2s, box-shadow 0.2s";

  btn.onmouseover = () => {
    btn.style.transform = "scale(1.05)";
    btn.style.boxShadow = "0 6px 12px rgba(0, 0, 0, 0.3)";
  };

  btn.onmouseout = () => {
    btn.style.transform = "scale(1)";
    btn.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.2)";
  };

  btn.onclick = () => {
    const emailElement = document.querySelector('.gD');
    const senderEmail = emailElement ? emailElement.getAttribute('email') : 'not_found@example.com';

    const bodyElement = document.querySelector('.a3s');
    const textContent = bodyElement ? bodyElement.innerText : '';

    const urls = [...textContent.matchAll(/https?:\/\/[^\s]+/g)].map(m => m[0]);
    const firstUrl = urls.length > 0 ? urls[0] : '';

    const resultWin = window.open("", "_blank");
    resultWin.document.write(`
      <html>
      <head><title>Phishing Checker - Зчитування даних</title></head>
      <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Отримано дані:</h2>
        <p><strong>Email:</strong> ${senderEmail}</p>
        <p><strong>URL:</strong> ${firstUrl || 'немає'}</p>
        <p><strong>Текст:</strong><br><pre style="background-color:#f4f4f4;padding:10px;border-radius:5px;">${textContent}</pre></p>
        <hr>
        <p><em>Виконується перевірка, зачекайте...</em></p>
      </body>
      </html>
    `);

    const formData = new FormData();
    formData.append('email', senderEmail);
    formData.append('text', textContent);
    if (firstUrl) formData.append('url', firstUrl);

    fetch("https://127.0.0.1:5555/analyze", {
      method: "POST",
      body: formData
    })
    .then(res => res.text())
    .then(html => {
      resultWin.document.open();
      resultWin.document.write(html);
      resultWin.document.close();
    });
  };

  document.body.appendChild(btn);
}

setInterval(createCheckButton, 3000);
