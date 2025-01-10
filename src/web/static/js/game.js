/**
 * Game state management and core functionality
 */
class Game {
    constructor() {
        this.state = {
            currentLocation: null,
            locationHistory: [],
            activeQuests: [],
            party: [],
            gameStarted: false,
            pendingOptions: null
        };
        this.apiBaseUrl = '/api/game';   // For new/load/save
        this.chatApiUrl = '/api/chat';   // For chat-based actions
    }

    async startNewGame() {
        ui.disableGameControls();
        try {
            const response = await fetch(`${this.apiBaseUrl}/new`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) throw new Error('Failed to start game');

            const data = await response.json();

            // Clear existing chat and UI state
            chat.clearChat();
            ui.clearAll();

            // Show messages from server response
            if (data.messages) {
                data.messages.forEach(msg => {
                    chat.addMessage(msg.sender, msg.content, msg.type || 'normal');
                });
            }

            // Merge any stateUpdate from server into local state
            if (data.stateUpdate) {
                Object.assign(this.state, data.stateUpdate);
                ui.updateGameState(this.state);
            }

            this.state.gameStarted = true;
            ui.enableGameControls();
        } catch (error) {
            ui.showError('Failed to start new game');
            ui.enableGameControls();
        }
    }

    async saveGame() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/save`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.state)
            });

            if (response.ok) {
                ui.showSuccess('Game saved successfully');
            } else {
                throw new Error('Save failed');
            }
        } catch (error) {
            ui.showError('Failed to save game');
        }
    }

    async loadGame(file) {
        try {
            const fileData = await file.text();
            const savedState = JSON.parse(fileData);

            const response = await fetch(`${this.apiBaseUrl}/load`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(savedState)
            });

            if (!response.ok) {
                throw new Error('Load failed');
            }

            const gameState = await response.json();
            this.initializeGame(gameState);
            ui.updateGameState(this.state);
            ui.showSuccess('Game loaded successfully');
        } catch (error) {
            ui.showError('Failed to load game');
        }
    }

    async handlePlayerInput(input) {
        if (!this.state.gameStarted) return;

        chat.addMessage('You', input);

        try {
            const response = await fetch(this.chatApiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userMessage: input })
            });

            if (!response.ok) {
                ui.showError('Server returned an error while processing your action');
                return;
            }

            const result = await response.json();
            this.processChatResponse(result);
        } catch (error) {
            ui.showError('Failed to process action');
        }
    }

    async selectQuestOption(optionIndex) {
        if (!this.state.pendingOptions) return;

        const selectedOption = this.state.pendingOptions[optionIndex];
        this.state.pendingOptions = null;

        chat.addMessage('You', `I choose: ${selectedOption.text}`);

        try {
            const response = await fetch(`${this.apiBaseUrl}/select-option`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ optionIndex, option: selectedOption })
            });

            if (!response.ok) {
                ui.showError('Server returned an error while processing your option choice');
                return;
            }

            const result = await response.json();
            this.processGameResponse(result);
        } catch (error) {
            ui.showError('Failed to process option selection');
        }
    }

    processChatResponse(response) {
        if (response.stateUpdate) {
            Object.assign(this.state, response.stateUpdate);
            ui.updateGameState(this.state);
        }

        if (response.messages) {
            response.messages.forEach(msg => {
                chat.addMessage(msg.sender, msg.content, 'normal');
            });
        }

        if (response.diceRolls) {
            response.diceRolls.forEach(roll => {
                chat.addSystemMessage(`🎲 ${roll.description}: ${roll.result}`, 'info');
            });
        }

        if (response.questUpdates) {
            this.updateQuests(response.questUpdates);
        }

        if (response.locationUpdate) {
            this.updateLocation(response.locationUpdate);
        }
    }

    processGameResponse(response) {
        if (response.stateUpdate) {
            Object.assign(this.state, response.stateUpdate);
            ui.updateGameState(this.state);
        }

        if (response.messages) {
            response.messages.forEach(msg => {
                chat.addMessage(msg.sender, msg.content, msg.type || 'normal');
            });
        }

        if (response.diceRolls) {
            response.diceRolls.forEach(roll => {
                chat.addSystemMessage(`🎲 ${roll.description}: ${roll.result}`, 'info');
            });
        }

        if (response.options) {
            this.state.pendingOptions = response.options;
            chat.addQuestOptions(response.options);
        }

        if (response.questUpdates) {
            this.updateQuests(response.questUpdates);
        }

        if (response.locationUpdate) {
            this.updateLocation(response.locationUpdate);
        }
    }

    updateQuests(questUpdates) {
        questUpdates.forEach(update => {
            if (update.type === 'add') {
                this.state.activeQuests.push(update.quest);
            } else if (update.type === 'complete') {
                const index = this.state.activeQuests.findIndex(q => q.id === update.questId);
                if (index !== -1) {
                    this.state.activeQuests.splice(index, 1);
                }
            } else if (update.type === 'update') {
                const quest = this.state.activeQuests.find(q => q.id === update.quest.id);
                if (quest) {
                    Object.assign(quest, update.quest);
                }
            }
        });

        ui.updateQuestList(this.state.activeQuests);
    }

    updateLocation(locationUpdate) {
        this.state.currentLocation = locationUpdate.current;
        if (locationUpdate.addToHistory) {
            this.state.locationHistory.push(locationUpdate.current);
        }
        ui.updateLocation(this.state.currentLocation, this.state.locationHistory);
    }

    initializeGame(gameState) {
        this.state = {
            ...gameState,
            gameStarted: true
        };
        if (gameState.party) {
            chat.initializeParty(gameState.party);
        }
    }

    quitGame() {
        this.state.gameStarted = false;
        chat.addSystemMessage('You have quit the game.', 'warning');
        ui.disableGameControls();
    }
}

const game = new Game();
window.game = game;
