// Main JavaScript file for WhatsFlow Automation

document.addEventListener('DOMContentLoaded', function () {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add scroll animation for elements
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card, .step').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Add visible class styles dynamically
    const style = document.createElement('style');
    style.textContent = `
        .visible {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);

    // WhatsApp Demo Logic
    const demoBtn = document.getElementById('watch-demo-btn');
    const modal = document.getElementById('demo-modal');
    const closeBtn = document.querySelector('.close-modal');
    const chatBody = document.getElementById('chat-body');
    let demoStarted = false;

    if (demoBtn && modal) {
        demoBtn.addEventListener('click', function () {
            modal.classList.add('show');
            modal.style.display = 'flex'; // Ensure flex display
            if (!demoStarted) {
                startDemoConversation();
                demoStarted = true;
            }
        });

        closeBtn.addEventListener('click', function () {
            modal.classList.remove('show');
            setTimeout(() => {
                modal.style.display = 'none';
            }, 300);
        });

        window.addEventListener('click', function (e) {
            if (e.target === modal) {
                modal.classList.remove('show');
                setTimeout(() => {
                    modal.style.display = 'none';
                }, 300);
            }
        });
    }

    function startDemoConversation() {
        const conversation = [
            { type: 'received', text: 'Hello! 👋 Welcome to WhatsFlow Automation.', delay: 1000 },
            { type: 'received', text: 'I am your AI assistant. How can I help you grow your business today?', delay: 2000 },
            { type: 'sent', text: 'Hi! I want to automate my customer support.', delay: 4000 },
            { type: 'received', text: 'Great choice! 🚀 I can handle 24/7 support, answer FAQs, and even book appointments.', delay: 6000 },
            { type: 'received', text: 'Would you like to see our pricing plans?', delay: 8000 },
            { type: 'sent', text: 'Yes, please.', delay: 10000 },
            { type: 'received', text: 'We have plans starting at just $62/mo. Check them out here: <a href="/pricing" style="color: #075E54; font-weight: bold;">View Pricing</a>', delay: 12000 },
            { type: 'received', text: 'Ready to get started? 😎', delay: 14000 }
        ];

        let currentTime = 0;

        conversation.forEach((msg) => {
            setTimeout(() => {
                if (msg.type === 'received') {
                    showTyping();
                    setTimeout(() => {
                        removeTyping();
                        addMessage(msg.type, msg.text);
                    }, 1500); // Typing duration
                } else {
                    addMessage(msg.type, msg.text);
                }
            }, msg.delay);
        });
    }

    function addMessage(type, text) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', type);

        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        msgDiv.innerHTML = `
            ${text}
            <div class="message-time">${time}</div>
        `;

        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('typing-indicator');
        typingDiv.id = 'typing';
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        chatBody.appendChild(typingDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function removeTyping() {
        const typing = document.getElementById('typing');
        if (typing) typing.remove();
    }
});
