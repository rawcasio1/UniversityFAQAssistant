// =====================================
// CHATBOT LOGIC (index.html)
// =====================================

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const inputField = document.getElementById('user-input');
    const message = inputField.value.trim();
    if (!message) return;

    appendMessage('User', message, 'user-message');
    inputField.value = '';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();
        
        let botReply = '';

        if (data.matched) {
            botReply = `
                <div class="response-card">
                    <strong>${data.policy_section} - ${data.title}</strong><br><br>
                    ${data.answer}
                    <div class="meta-info">
                        <strong>Extracted Keywords:</strong> ${data.matched_keywords} <br>
                        <strong>Confidence:</strong> ${data.confidence}
                    </div>
                </div>
            `;
        } else {
            botReply = `Sorry, I could not find an exact answer. <br><br> You may try asking about: <br><ul>`;
            data.suggestions.forEach(s => botReply += `<li>${s}</li>`);
            botReply += `</ul>`;
        }

        appendMessage('Bot', botReply, 'bot-message');

    } catch (error) {
        appendMessage('Bot', 'Error connecting to the server.', 'bot-message');
    }
}

function appendMessage(sender, htmlContent, className) {
    const chatBox = document.getElementById('chat-box');
    if (!chatBox) return; // Skip if not on index.html

    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${className}`;
    
    // Add prefix for user, omit for bot since bot content is rich HTML
    if (sender === 'User') {
        msgDiv.innerHTML = `<strong>${sender}:</strong> ${htmlContent}`;
    } else {
        msgDiv.innerHTML = htmlContent;
    }

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// =====================================
// ADMIN LOGIC (admin.html)
// =====================================

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById('faq-table-body')) {
        loadFAQs();
    }
});

async function loadFAQs() {
    const response = await fetch('/api/faqs');
    const faqs = await response.json();
    const tbody = document.getElementById('faq-table-body');
    tbody.innerHTML = '';

    faqs.forEach(faq => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${faq.id}</td>
            <td><strong>${faq.title}</strong><br><small>${faq.policy_section}</small></td>
            <td>${faq.keywords}</td>
            <td>
                <button class="action-btn edit-btn" onclick='editFAQ(${JSON.stringify(faq).replace(/'/g, "&#39;")})'>Edit</button>
                <button class="action-btn del-btn" onclick="deleteFAQ(${faq.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function editFAQ(faq) {
    document.getElementById('faq-id').value = faq.id;
    document.getElementById('faq-title').value = faq.title;
    document.getElementById('faq-section').value = faq.policy_section;
    document.getElementById('faq-keywords').value = faq.keywords;
    document.getElementById('faq-question').value = faq.question;
    document.getElementById('faq-answer').value = faq.answer;
}

function clearForm() {
    document.getElementById('faq-id').value = '';
    document.getElementById('faq-title').value = '';
    document.getElementById('faq-section').value = '';
    document.getElementById('faq-keywords').value = '';
    document.getElementById('faq-question').value = '';
    document.getElementById('faq-answer').value = '';
}

async function saveFAQ() {
    const id = document.getElementById('faq-id').value;
    const payload = {
        title: document.getElementById('faq-title').value,
        policy_section: document.getElementById('faq-section').value,
        keywords: document.getElementById('faq-keywords').value,
        question: document.getElementById('faq-question').value,
        answer: document.getElementById('faq-answer').value
    };

    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/faqs/${id}` : '/api/faqs';

    await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    clearForm();
    loadFAQs();
}

async function deleteFAQ(id) {
    if (confirm('Are you sure you want to delete this FAQ?')) {
        await fetch(`/api/faqs/${id}`, { method: 'DELETE' });
        loadFAQs();
    }
}
