chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "analyzeEmail") {
        fetch("https://172.20.10.5:5555/analyze", {
            method: "POST",
            body: new URLSearchParams({
                text: message.text,
                email: "",  // можна вбудувати логіку визначення email-адреси
                url: ""     // парсити URL із тексту, якщо потрібно
            })
        })
        .then(res => res.text())
        .then(html => {
            console.log("Analysis complete.");
        })
        .catch(err => console.error("Error:", err));
    }
});