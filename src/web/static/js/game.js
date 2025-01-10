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
        this.apiBaseUrl = '/api/game';
    }

    async startNewGame() {
        ui.disableGameControls();
        try {
            const response = await fetch(`${this.apiBaseUrl}/new`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) throw new Error('Failed to start game');

            // Clear existing state
            this.state = {
                currentLocation: null,
                locationHistory: [],
                activeQuests: [],
                party: [],
                gameStarted: true
            };

            chat.clearChat();
            ui.clearAll();

            // Add initial game master message
            chat.addMessage('Game Master',
                'Welcome to your D&D adventure! I will be your Game Master.' +
                '\n\nFirst, let\'s create your character. What class would you like to play?' +
                '\n\nAvailable classes are: Barbarian, Bard, Cleric, Druid, Fighter, Monk, ' +
                'Paladin, Ranger, Rogue, Sorcerer, Warlock, and Wizard.'
            );

            // Show class options as clickable choices
            const classOptions = [
                'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk',
                'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard'
            ].map(className => ({
                text: className,
                class: className
            }));

            chat.addQuestOptions(classOptions);

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
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${this.apiBaseUrl}/load`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const gameState = await response.json();
                this.initializeGame(gameState);
                ui.updateGameState(this.state);
                ui.showSuccess('Game loaded successfully');
            } else {
                throw new Error('Load failed');
            }
        } catch (error) {
            ui.showError('Failed to load game');
        }
    }

    async handlePlayerInput(input) {
        if (!this.state.gameStarted) return;

        chat.addMessage('You', input);

        try {
            const response = await fetch(`${this.apiBaseUrl}/action`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: input })
            });

            const result = await response.json();
            this.processGameResponse(result);
        } catch (error) {
            ui.showError('Failed to process action');
        }
    }

    async selectQuestOption(optionIndex) {
        if (!this.state.pendingOptions) return;

        const selectedOption = this.state.pendingOptions[optionIndex];
        this.state.pendingOptions = null;

        try {
            const response = await fetch(`${this.apiBaseUrl}/select-option`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ optionIndex, option: selectedOption })
            });

            const result = await response.json();
            this.processGameResponse(result);
        } catch (error) {
            ui.showError('Failed to process option selection');
        }
    }

    processGameResponse(response) {
        if (response.stateUpdate) {
            Object.assign(this.state, response.stateUpdate);
            ui.updateGameState(this.state);
        }

        if (response.messages) {
            response.messages.forEach(msg => {
                chat.addMessage(msg.sender, msg.content, msg.type);
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
}

const game = new Game();
window.game = game;