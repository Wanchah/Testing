/**
 * EduMorph - Accessibility Features
 * Supporting inclusive education for all learners
 */

// Accessibility state
let accessibilityState = {
    highContrast: false,
    largeText: false,
    reducedMotion: false,
    screenReader: false,
    keyboardNavigation: false,
    voiceControl: false
};

// Initialize accessibility features
document.addEventListener('DOMContentLoaded', function() {
    initializeAccessibility();
    setupAccessibilityListeners();
    detectAccessibilityPreferences();
});

/**
 * Initialize accessibility features
 */
function initializeAccessibility() {
    console.log('♿ Accessibility features initialized');
    
    // Load saved preferences
    loadAccessibilityPreferences();
    
    // Apply initial settings
    applyAccessibilitySettings();
    
    // Setup keyboard navigation
    setupKeyboardNavigation();
    
    // Setup screen reader support
    setupScreenReaderSupport();
    
    // Setup voice control
    setupVoiceControl();
    
    // Setup focus management
    setupFocusManagement();
    
    // Setup ARIA live regions
    setupAriaLiveRegions();
}

/**
 * Setup accessibility event listeners
 */
function setupAccessibilityListeners() {
    // Listen for accessibility preference changes
    document.addEventListener('change', function(e) {
        if (e.target.matches('[data-accessibility-toggle]')) {
            const feature = e.target.dataset.accessibilityToggle;
            const enabled = e.target.checked;
            toggleAccessibilityFeature(feature, enabled);
        }
    });
    
    // Listen for keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        handleAccessibilityShortcuts(e);
    });
    
    // Listen for system preference changes
    window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', function(e) {
        accessibilityState.reducedMotion = e.matches;
        applyAccessibilitySettings();
    });
    
    window.matchMedia('(prefers-contrast: high)').addEventListener('change', function(e) {
        accessibilityState.highContrast = e.matches;
        applyAccessibilitySettings();
    });
}

/**
 * Detect system accessibility preferences
 */
function detectAccessibilityPreferences() {
    // Detect reduced motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        accessibilityState.reducedMotion = true;
    }
    
    // Detect high contrast preference
    if (window.matchMedia('(prefers-contrast: high)').matches) {
        accessibilityState.highContrast = true;
    }
    
    // Detect screen reader
    if (window.speechSynthesis || window.webkitSpeechSynthesis) {
        accessibilityState.screenReader = true;
    }
    
    // Apply detected preferences
    applyAccessibilitySettings();
}

/**
 * Load accessibility preferences from localStorage
 */
function loadAccessibilityPreferences() {
    const saved = localStorage.getItem('edumorph-accessibility');
    if (saved) {
        try {
            const preferences = JSON.parse(saved);
            Object.assign(accessibilityState, preferences);
        } catch (e) {
            console.warn('Failed to load accessibility preferences:', e);
        }
    }
}

/**
 * Save accessibility preferences to localStorage
 */
function saveAccessibilityPreferences() {
    localStorage.setItem('edumorph-accessibility', JSON.stringify(accessibilityState));
}

/**
 * Toggle accessibility feature
 */
function toggleAccessibilityFeature(feature, enabled) {
    accessibilityState[feature] = enabled;
    applyAccessibilitySettings();
    saveAccessibilityPreferences();
    
    // Announce change to screen readers
    announceToScreenReader(`${feature} ${enabled ? 'enabled' : 'disabled'}`);
    
    // Show confirmation
    showAccessibilityNotification(`${feature} ${enabled ? 'enabled' : 'disabled'}`);
}

/**
 * Apply accessibility settings
 */
function applyAccessibilitySettings() {
    const body = document.body;
    
    // High contrast
    body.classList.toggle('high-contrast', accessibilityState.highContrast);
    
    // Large text
    body.classList.toggle('large-text', accessibilityState.largeText);
    
    // Reduced motion
    body.classList.toggle('reduced-motion', accessibilityState.reducedMotion);
    
    // Screen reader optimizations
    body.classList.toggle('screen-reader', accessibilityState.screenReader);
    
    // Keyboard navigation
    body.classList.toggle('keyboard-nav', accessibilityState.keyboardNavigation);
    
    // Voice control
    body.classList.toggle('voice-control', accessibilityState.voiceControl);
    
    // Update form controls
    updateAccessibilityControls();
}

/**
 * Update accessibility control states
 */
function updateAccessibilityControls() {
    const toggles = document.querySelectorAll('[data-accessibility-toggle]');
    toggles.forEach(toggle => {
        const feature = toggle.dataset.accessibilityToggle;
        toggle.checked = accessibilityState[feature] || false;
    });
}

/**
 * Setup keyboard navigation
 */
function setupKeyboardNavigation() {
    // Enable keyboard navigation by default
    accessibilityState.keyboardNavigation = true;
    
    // Add keyboard navigation indicators
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-nav');
        }
    });
    
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-nav');
    });
    
    // Setup skip links
    setupSkipLinks();
    
    // Setup focus indicators
    setupFocusIndicators();
}

/**
 * Setup skip links
 */
function setupSkipLinks() {
    // Create skip links if they don't exist
    const skipLink = document.querySelector('.skip-link');
    if (!skipLink) {
        const link = document.createElement('a');
        link.href = '#main-content';
        link.className = 'skip-link';
        link.textContent = 'Skip to main content';
        document.body.insertBefore(link, document.body.firstChild);
    }
    
    // Add skip links for other important sections
    const sections = ['navigation', 'search', 'content', 'footer'];
    sections.forEach(section => {
        const element = document.querySelector(`#${section}, .${section}`);
        if (element && !document.querySelector(`.skip-link[href="#${section}"]`)) {
            const link = document.createElement('a');
            link.href = `#${section}`;
            link.className = 'skip-link';
            link.textContent = `Skip to ${section}`;
            link.style.top = `${sections.indexOf(section) * 40 + 6}px`;
            document.body.appendChild(link);
        }
    });
}

/**
 * Setup focus indicators
 */
function setupFocusIndicators() {
    // Add focus indicators to interactive elements
    const interactiveElements = document.querySelectorAll(
        'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    interactiveElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.classList.add('focus-visible');
        });
        
        element.addEventListener('blur', function() {
            this.classList.remove('focus-visible');
        });
    });
}

/**
 * Setup screen reader support
 */
function setupScreenReaderSupport() {
    // Create live region for announcements
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    liveRegion.id = 'live-region';
    document.body.appendChild(liveRegion);
    
    // Add ARIA labels to interactive elements
    addAriaLabels();
    
    // Setup landmark navigation
    setupLandmarkNavigation();
}

/**
 * Add ARIA labels to elements
 */
function addAriaLabels() {
    // Add labels to buttons without text
    const iconButtons = document.querySelectorAll('button:not([aria-label]):not([aria-labelledby])');
    iconButtons.forEach(button => {
        const icon = button.querySelector('i');
        if (icon) {
            const label = getIconLabel(icon.className);
            button.setAttribute('aria-label', label);
        }
    });
    
    // Add labels to form inputs
    const inputs = document.querySelectorAll('input:not([aria-label]):not([aria-labelledby])');
    inputs.forEach(input => {
        const label = document.querySelector(`label[for="${input.id}"]`);
        if (label) {
            input.setAttribute('aria-labelledby', label.id || `label-${input.id}`);
        }
    });
    
    // Add descriptions to complex elements
    addElementDescriptions();
}

/**
 * Get label for icon
 */
function getIconLabel(iconClass) {
    const iconLabels = {
        'fa-search': 'Search',
        'fa-menu': 'Menu',
        'fa-close': 'Close',
        'fa-edit': 'Edit',
        'fa-delete': 'Delete',
        'fa-save': 'Save',
        'fa-cancel': 'Cancel',
        'fa-user': 'User',
        'fa-settings': 'Settings',
        'fa-help': 'Help',
        'fa-info': 'Information',
        'fa-warning': 'Warning',
        'fa-error': 'Error',
        'fa-success': 'Success',
        'fa-play': 'Play',
        'fa-pause': 'Pause',
        'fa-stop': 'Stop',
        'fa-download': 'Download',
        'fa-upload': 'Upload',
        'fa-share': 'Share',
        'fa-like': 'Like',
        'fa-dislike': 'Dislike',
        'fa-favorite': 'Favorite',
        'fa-bookmark': 'Bookmark'
    };
    
    for (const [icon, label] of Object.entries(iconLabels)) {
        if (iconClass.includes(icon)) {
            return label;
        }
    }
    
    return 'Button';
}

/**
 * Add descriptions to complex elements
 */
function addElementDescriptions() {
    // Add descriptions to progress bars
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const percentage = bar.dataset.percentage || 0;
        const label = bar.getAttribute('aria-label') || 'Progress';
        bar.setAttribute('aria-label', `${label}: ${percentage}% complete`);
    });
    
    // Add descriptions to charts
    const charts = document.querySelectorAll('.chart');
    charts.forEach(chart => {
        if (!chart.getAttribute('aria-label')) {
            chart.setAttribute('aria-label', 'Data visualization');
        }
    });
    
    // Add descriptions to images
    const images = document.querySelectorAll('img:not([alt])');
    images.forEach(img => {
        img.setAttribute('alt', 'Image');
        img.setAttribute('role', 'img');
    });
}

/**
 * Setup landmark navigation
 */
function setupLandmarkNavigation() {
    // Add landmark roles
    const header = document.querySelector('header');
    if (header) {
        header.setAttribute('role', 'banner');
    }
    
    const nav = document.querySelector('nav');
    if (nav) {
        nav.setAttribute('role', 'navigation');
    }
    
    const main = document.querySelector('main');
    if (main) {
        main.setAttribute('role', 'main');
    }
    
    const footer = document.querySelector('footer');
    if (footer) {
        footer.setAttribute('role', 'contentinfo');
    }
    
    // Add region roles to sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        if (!section.getAttribute('role')) {
            section.setAttribute('role', 'region');
        }
    });
}

/**
 * Setup voice control
 */
function setupVoiceControl() {
    // Check if speech recognition is available
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        accessibilityState.voiceControl = true;
        
        // Add voice control indicators
        document.addEventListener('keydown', function(e) {
            if (e.key === 'v' && e.ctrlKey) {
                e.preventDefault();
                startVoiceControl();
            }
        });
    }
}

/**
 * Start voice control
 */
function startVoiceControl() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    // Show voice control indicator
    showVoiceControlIndicator();
    
    recognition.onresult = function(event) {
        const command = event.results[event.results.length - 1][0].transcript.toLowerCase();
        executeVoiceCommand(command);
    };
    
    recognition.onerror = function(event) {
        console.error('Voice recognition error:', event.error);
        hideVoiceControlIndicator();
    };
    
    recognition.onend = function() {
        hideVoiceControlIndicator();
    };
    
    recognition.start();
}

/**
 * Execute voice command
 */
function executeVoiceCommand(command) {
    const commands = {
        'go home': () => window.location.href = '/',
        'go to lessons': () => window.location.href = '/lessons',
        'go to dashboard': () => window.location.href = '/dashboard',
        'search': () => document.querySelector('.search-input')?.focus(),
        'help': () => showHelp(),
        'close': () => closeAllModals(),
        'next': () => navigateNext(),
        'previous': () => navigatePrevious(),
        'scroll up': () => window.scrollBy(0, -100),
        'scroll down': () => window.scrollBy(0, 100)
    };
    
    for (const [cmd, action] of Object.entries(commands)) {
        if (command.includes(cmd)) {
            action();
            announceToScreenReader(`Executed: ${cmd}`);
            break;
        }
    }
}

/**
 * Show voice control indicator
 */
function showVoiceControlIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'voice-control-indicator';
    indicator.className = 'voice-control-indicator';
    indicator.innerHTML = '<i class="fas fa-microphone"></i> Listening...';
    document.body.appendChild(indicator);
}

/**
 * Hide voice control indicator
 */
function hideVoiceControlIndicator() {
    const indicator = document.getElementById('voice-control-indicator');
    if (indicator) {
        indicator.remove();
    }
}

/**
 * Setup focus management
 */
function setupFocusManagement() {
    // Trap focus in modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            const modal = document.querySelector('.modal.show');
            if (modal) {
                trapFocus(e, modal);
            }
        }
    });
    
    // Manage focus for dynamic content
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        addAriaLabelsToElement(node);
                    }
                });
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

/**
 * Add ARIA labels to a specific element
 */
function addAriaLabelsToElement(element) {
    const iconButtons = element.querySelectorAll('button:not([aria-label]):not([aria-labelledby])');
    iconButtons.forEach(button => {
        const icon = button.querySelector('i');
        if (icon) {
            const label = getIconLabel(icon.className);
            button.setAttribute('aria-label', label);
        }
    });
}

/**
 * Setup ARIA live regions
 */
function setupAriaLiveRegions() {
    // Create live region for status updates
    const statusRegion = document.createElement('div');
    statusRegion.setAttribute('aria-live', 'polite');
    statusRegion.setAttribute('aria-atomic', 'true');
    statusRegion.className = 'sr-only';
    statusRegion.id = 'status-region';
    document.body.appendChild(statusRegion);
    
    // Create live region for alerts
    const alertRegion = document.createElement('div');
    alertRegion.setAttribute('aria-live', 'assertive');
    alertRegion.setAttribute('aria-atomic', 'true');
    alertRegion.className = 'sr-only';
    alertRegion.id = 'alert-region';
    document.body.appendChild(alertRegion);
}

/**
 * Announce message to screen readers
 */
function announceToScreenReader(message, priority = 'polite') {
    const region = priority === 'assertive' ? 
        document.getElementById('alert-region') : 
        document.getElementById('live-region');
    
    if (region) {
        region.textContent = message;
        setTimeout(() => {
            region.textContent = '';
        }, 1000);
    }
}

/**
 * Show accessibility notification
 */
function showAccessibilityNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'accessibility-notification';
    notification.innerHTML = `
        <i class="fas fa-universal-access"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

/**
 * Handle accessibility keyboard shortcuts
 */
function handleAccessibilityShortcuts(e) {
    // Alt + A: Toggle accessibility menu
    if (e.altKey && e.key === 'a') {
        e.preventDefault();
        toggleAccessibilityMenu();
    }
    
    // Alt + H: Toggle high contrast
    if (e.altKey && e.key === 'h') {
        e.preventDefault();
        toggleAccessibilityFeature('highContrast', !accessibilityState.highContrast);
    }
    
    // Alt + L: Toggle large text
    if (e.altKey && e.key === 'l') {
        e.preventDefault();
        toggleAccessibilityFeature('largeText', !accessibilityState.largeText);
    }
    
    // Alt + R: Toggle reduced motion
    if (e.altKey && e.key === 'r') {
        e.preventDefault();
        toggleAccessibilityFeature('reducedMotion', !accessibilityState.reducedMotion);
    }
}

/**
 * Toggle accessibility menu
 */
function toggleAccessibilityMenu() {
    const menu = document.querySelector('.accessibility-menu');
    if (menu) {
        menu.classList.toggle('show');
    } else {
        createAccessibilityMenu();
    }
}

/**
 * Create accessibility menu
 */
function createAccessibilityMenu() {
    const menu = document.createElement('div');
    menu.className = 'accessibility-menu show';
    menu.innerHTML = `
        <div class="accessibility-menu-header">
            <h3>Accessibility Settings</h3>
            <button class="close-button" aria-label="Close accessibility menu">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="accessibility-menu-content">
            <div class="accessibility-option">
                <label>
                    <input type="checkbox" data-accessibility-toggle="highContrast">
                    High Contrast
                </label>
            </div>
            <div class="accessibility-option">
                <label>
                    <input type="checkbox" data-accessibility-toggle="largeText">
                    Large Text
                </label>
            </div>
            <div class="accessibility-option">
                <label>
                    <input type="checkbox" data-accessibility-toggle="reducedMotion">
                    Reduced Motion
                </label>
            </div>
            <div class="accessibility-option">
                <label>
                    <input type="checkbox" data-accessibility-toggle="screenReader">
                    Screen Reader Optimized
                </label>
            </div>
        </div>
        <div class="accessibility-menu-footer">
            <button class="btn btn-primary" onclick="resetAccessibilitySettings()">
                Reset to Defaults
            </button>
        </div>
    `;
    
    document.body.appendChild(menu);
    
    // Update control states
    updateAccessibilityControls();
    
    // Add close functionality
    const closeButton = menu.querySelector('.close-button');
    closeButton.addEventListener('click', () => {
        menu.remove();
    });
    
    // Close on escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            menu.remove();
        }
    }, { once: true });
}

/**
 * Reset accessibility settings
 */
function resetAccessibilitySettings() {
    accessibilityState = {
        highContrast: false,
        largeText: false,
        reducedMotion: false,
        screenReader: false,
        keyboardNavigation: true,
        voiceControl: false
    };
    
    applyAccessibilitySettings();
    saveAccessibilityPreferences();
    
    announceToScreenReader('Accessibility settings reset to defaults');
    showAccessibilityNotification('Settings reset to defaults');
}

// Export accessibility functions
window.EduMorphAccessibility = {
    toggleAccessibilityFeature,
    announceToScreenReader,
    showAccessibilityNotification,
    resetAccessibilitySettings
};
