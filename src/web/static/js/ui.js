/**
 * UI components and interactions management
 */
class UI {
    constructor() {
        this.questList = document.getElementById('quest-list');
        this.currentLocation = document.getElementById('current-location');
        this.locationHistory = document.getElementById('location-history');
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.addEventListener('keydown', this.handleKeyboardShortcuts.bind(this));
        document.getElementById('chat-input').addEventListener('keypress', this.handleEnterKey.bind(this));
        window.addEventListener('resize', () => this.scrollChatToBottom());
    }

    updateGameState(state) {
        requestAnimationFrame(() => {
            this.updateQuestList(state.activeQuests);
            this.updateLocation(state.currentLocation, state.locationHistory);
        });
    }

    updateQuestList(quests = []) {
        this.questList.innerHTML = '';

        quests.forEach(quest => {
            const questElement = document.createElement('div');
            questElement.className = `quest-item ${quest.active ? 'quest-active' : ''} fade-in`;

            questElement.innerHTML = `
                <div class="p-4 rounded-lg border ${quest.active ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}">
                    <h3 class="font-bold text-lg mb-2">${quest.title}</h3>
                    <p class="text-gray-600 mb-3">${quest.description}</p>
                    ${this.renderQuestProgress(quest)}
                    ${this.renderQuestObjectives(quest)}
                </div>
            `;

            this.questList.appendChild(questElement);
        });
    }

    renderQuestProgress(quest) {
        if (!quest.progress) return '';

        return `
            <div class="flex items-center space-x-2 mb-2">
                <div class="flex-1 h-2 bg-gray-200 rounded">
                    <div class="h-full bg-blue-500 rounded" style="width: ${quest.progress}%"></div>
                </div>
                <span class="text-sm text-gray-600">${quest.progress}%</span>
            </div>
        `;
    }

    renderQuestObjectives(quest) {
        if (!quest.objectives?.length) return '';

        return `
            <div class="mt-3">
                <h4 class="font-semibold mb-2">Objectives:</h4>
                <ul class="space-y-1">
                    ${quest.objectives.map(obj => `
                        <li class="flex items-center space-x-2">
                            <span class="text-sm ${obj.completed ? 'line-through text-gray-400' : ''}">${obj.description}</span>
                            ${obj.completed ? '<span class="text-green-500">✓</span>' : ''}
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
    }

    updateLocation(current, history) {
        if (current) {
            this.currentLocation.innerHTML = `
                <div class="p-3 bg-blue-50 rounded-lg">
                    <h3 class="font-bold text-lg mb-1">${current.name}</h3>
                    <p class="text-gray-600">${current.description}</p>
                </div>
            `;
        }

        this.locationHistory.innerHTML = '';
        (history || []).slice().reverse().forEach(location => {
            const locationElement = document.createElement('div');
            locationElement.className = `location-item ${location.name === current?.name ? 'location-current' : ''} fade-in`;
            locationElement.textContent = location.name;
            this.locationHistory.appendChild(locationElement);
        });
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');

        const styles = {
            info: 'bg-blue-500',
            success: 'bg-green-500',
            error: 'bg-red-500',
            warning: 'bg-yellow-500'
        };

        notification.className = `fixed top-4 right-4 p-4 rounded-lg text-white ${styles[type]}
                                shadow-lg z-50 transform transition-all duration-300 fade-in`;

        notification.innerHTML = `
            <div class="flex items-center space-x-3">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()"
                        class="hover:text-gray-200">✕</button>
            </div>
        `;

        document.body.appendChild(notification);
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    scrollChatToBottom() {
        const chat = document.getElementById('chat-messages');
        chat.scrollTop = chat.scrollHeight;
    }

    handleKeyboardShortcuts(e) {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 's':
                    e.preventDefault();
                    game.saveGame();
                    break;
                case 'o':
                    e.preventDefault();
                    document.getElementById('loadGameFile').click();
                    break;
            }
        }
    }

    handleEnterKey(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    }

    clearAll() {
        this.questList.innerHTML = '';
        this.currentLocation.innerHTML = '';
        this.locationHistory.innerHTML = '';
    }

    disableGameControls() {
        document.querySelectorAll('button').forEach(btn => btn.disabled = true);
    }

    enableGameControls() {
        document.querySelectorAll('button').forEach(btn => btn.disabled = false);
    }

    showError(message) { this.showNotification(message, 'error'); }
    showSuccess(message) { this.showNotification(message, 'success'); }
    showWarning(message) { this.showNotification(message, 'warning'); }
    showInfo(message) { this.showNotification(message, 'info'); }
}

const ui = new UI();

// Global event handlers
document.addEventListener('DOMContentLoaded', () => {
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case 's':
                    e.preventDefault();
                    game.saveGame();
                    break;
                case 'o':
                    e.preventDefault();
                    document.getElementById('loadGameFile').click();
                    break;
                case 'n':
                    e.preventDefault();
                    if (confirm('Start new game? Current progress will be lost.')) {
                        game.startNewGame();
                    }
                    break;
            }
        }
    });

    // Chat input focus
    const chatInput = document.getElementById('chat-input');
    chatInput.focus();
    document.addEventListener('click', () => chatInput.focus());
});

// Responsive design handlers
window.addEventListener('resize', () => {
    const chat = document.getElementById('chat-messages');
    chat.scrollTop = chat.scrollHeight;
});