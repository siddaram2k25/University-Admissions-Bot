// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatContainer = document.getElementById('chatContainer');
    const resetBtn = document.getElementById('resetBtn');
    const checkEligibilityBtn = document.getElementById('checkEligibilityBtn');
    const eligibilityForm = document.getElementById('eligibilityForm');
    
    // Send message on button click
    sendBtn.addEventListener('click', sendMessage);
    
    // Send message on Enter key
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Reset conversation
    resetBtn.addEventListener('click', resetConversation);
    
    // Check eligibility
    if (checkEligibilityBtn) {
        checkEligibilityBtn.addEventListener('click', checkEligibility);
    }
    
    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});

function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (message === '') return;
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    userInput.value = '';
    userInput.style.height = 'auto';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Send to backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add bot response
        addMessage(data.response, 'bot');
        
        // Show eligibility form if needed
        if (data.show_eligibility_form) {
            showEligibilityForm();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        removeTypingIndicator();
        addMessage('Sorry, I encountered an error. Please try again.', 'bot');
    });
}

function addMessage(content, sender) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    
    if (sender === 'bot') {
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
    } else {
        avatar.innerHTML = '<i class="fas fa-user"></i>';
    }
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    // Convert newlines to <br> and URLs to links
    content = content.replace(/\n/g, '<br>');
    content = content.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
    
    messageContent.innerHTML = `<p>${content}</p>`;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showTypingIndicator() {
    const chatContainer = document.getElementById('chatContainer');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.id = 'typingIndicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerHTML = '<i class="fas fa-robot"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML = '<div class="loading"><span></span><span></span><span></span></div>';
    
    typingDiv.appendChild(avatar);
    typingDiv.appendChild(messageContent);
    
    chatContainer.appendChild(typingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function showEligibilityForm() {
    const form = document.getElementById('eligibilityForm');
    form.style.display = 'block';
    
    // Smooth scroll to form
    form.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function hideEligibilityForm() {
    const form = document.getElementById('eligibilityForm');
    form.style.display = 'none';
    
    // Clear form fields
    document.getElementById('educationLevel').value = '';
    document.getElementById('gpa').value = '';
    document.getElementById('testType').value = '';
    document.getElementById('testScore').value = '';
    document.getElementById('eligibilityResult').innerHTML = '';
}

function checkEligibility() {
    const level = document.getElementById('educationLevel').value;
    const gpa = document.getElementById('gpa').value;
    const testType = document.getElementById('testType').value;
    const testScore = document.getElementById('testScore').value;
    
    // Validate form
    if (!level || !gpa || !testType || !testScore) {
        alert('Please fill in all fields');
        return;
    }
    
    const resultDiv = document.getElementById('eligibilityResult');
    resultDiv.innerHTML = '<div class="loading"><span></span><span></span><span></span></div>';
    
    fetch('/check-eligibility', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            level: level,
            gpa: gpa,
            test_type: testType,
            test_score: testScore
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            resultDiv.innerHTML = `<div style="color: ${data.eligible ? '#28a745' : '#856404'}">
                ${data.message}
            </div>`;
            
            // Also add to chat
            addMessage(`📊 Eligibility Check Result: ${data.message}`, 'bot');
        } else {
            resultDiv.innerHTML = `<div style="color: #dc3545">Error: ${data.message}</div>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        resultDiv.innerHTML = '<div style="color: #dc3545">Error checking eligibility. Please try again.</div>';
    });
}

function resetConversation() {
    fetch('/reset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(() => {
        // Clear chat container
        const chatContainer = document.getElementById('chatContainer');
        chatContainer.innerHTML = `
            <div class="message bot-message">
                <div class="avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>🎓 Welcome back! I'm the University Admissions Bot.</p>
                    <p>How can I help you today? 😊</p>
                </div>
            </div>
        `;
        
        // Hide eligibility form
        hideEligibilityForm();
    })
    .catch(error => console.error('Error:', error));
}

function sendQuickMessage(message) {
    const userInput = document.getElementById('userInput');
    userInput.value = message;
    sendMessage();
}