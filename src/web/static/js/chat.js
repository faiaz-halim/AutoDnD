/**
 * Chat interface handling for D&D game
 */
class ChatInterface {
    constructor() {
        this.chatMessages = document.getElementById('chat-messages');
        this.chatInput = document.getElementById('chat-input');
        this.messageHistory = [];
        this.partyMembers = new Map();
        this.avatarBaseUrl = '/static/images/avatars/';
    }

    initializeParty(members) {
        this.partyMembers.clear();
        members.forEach(member => {
            this.partyMembers.set(member.name, {
                avatar: this.getClassAvatar(member.class),
                class: member.class
            });
        });
    }

    getClassAvatar(className) {
        const validClasses = [
            'barbarian', 'bard', 'cleric', 'druid', 'fighter',
            'monk', 'paladin', 'ranger', 'rogue', 'sorcerer',
            'warlock', 'wizard'
        ];

        const class_name = className?.toLowerCase() || 'default';
        if (validClasses.includes(class_name)) {
            return `${this.avatarBaseUrl}${class_name}.png`;
        }
        return `${this.avatarBaseUrl}default.png`;
    }

    addMessage(sender, content, type = 'normal') {
        const messageDiv = document.createElement('div');
        const messageClass = this._getMessageClass(sender);
        messageDiv.className = `message fade-in ${messageClass}`;

        messageDiv.innerHTML = `
            <div class="message-wrapper">
                <div class="message-inner">
                    <img src="${this._getAvatar(sender)}"
                        alt="${sender}"
                        class="avatar ${messageClass}-avatar">
                    <div class="message-content">
                        <div class="font-bold text-gray-900">${sender}</div>
                        <div class="${this._getTextClass(type)}">${this._formatContent(content)}</div>
                    </div>
                </div>
            </div>
        `;

        this.chatMessages.appendChild(messageDiv);
        this._scrollToBottom();
        this.messageHistory.push({ sender, content, type });
    }

    addQuestOptions(options) {
        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'quest-options fade-in space-y-2 p-4';

        options.forEach((option, index) => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'quest-option';
            optionDiv.innerHTML = `
                <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100">
                    <span class="flex-1">${option.text}</span>
                    <button onclick="game.selectQuestOption(${index})"
                            class="ml-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                        Choose
                    </button>
                </div>
            `;
            optionsDiv.appendChild(optionDiv);
        });

        this.chatMessages.appendChild(optionsDiv);
        this._scrollToBottom();
    }

    addSystemMessage(content, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `system-message fade-in my-2 px-4 py-2 rounded ${this._getSystemClass(type)}`;
        messageDiv.innerHTML = `
            <div class="flex items-center space-x-2">
                <span class="text-sm font-medium">${content}</span>
            </div>
        `;
        this.chatMessages.appendChild(messageDiv);
        this._scrollToBottom();
    }

    _getAvatar(sender) {
        if (sender === 'Game Master') return `${this.avatarBaseUrl}gm.png`;
        if (sender === 'You') return `${this.avatarBaseUrl}default.png`;
        const member = this.partyMembers.get(sender);
        return member ? member.avatar : `${this.avatarBaseUrl}default.png`;
    }

    _getMessageClass(sender) {
        if (sender === 'Game Master') return 'message-gm';
        if (sender === 'You') return 'message-player';
        return 'message-companion';
    }

    _getSystemClass(type) {
        const classes = {
            'info': 'bg-blue-100 text-blue-800',
            'warning': 'bg-yellow-100 text-yellow-800',
            'error': 'bg-red-100 text-red-800',
            'success': 'bg-green-100 text-green-800'
        };
        return classes[type] || classes.info;
    }

    _getTextClass(type) {
        switch(type) {
            case 'danger': return 'text-red-600';
            case 'warning': return 'text-yellow-600';
            case 'info': return 'text-blue-600';
            default: return 'text-gray-700';
        }
    }

    _formatContent(content) {
        marked.setOptions({
            breaks: true,
            gfm: true,
            headerIds: false,
            mangle: false
        });

        // Custom tokens
        content = content
            .replace(/\*\*danger:(.*?)\*\*/g, '<span class="text-red-600 font-bold">$1</span>')
            .replace(/\*\*warning:(.*?)\*\*/g, '<span class="text-yellow-600 font-bold">$1</span>')
            .replace(/\*\*info:(.*?)\*\*/g, '<span class="text-blue-600 font-bold">$1</span>');

        // Parse markdown
        return marked.parse(content);
    }

    _scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    clearChat() {
        this.chatMessages.innerHTML = '';
        this.messageHistory = [];
    }

    clearInput() {
        this.chatInput.value = '';
    }

    getInput() {
        return this.chatInput.value.trim();
    }
}

const chat = new ChatInterface();

function sendMessage() {
    const input = chat.getInput();
    if (input) {
        game.handlePlayerInput(input);
        chat.clearInput();
    }
}