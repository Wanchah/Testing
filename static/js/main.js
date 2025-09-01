/**
 * EduMorph - Main JavaScript
 * Supporting SDG 4: Quality Education with accessible, interactive features
 */

// Global variables
let currentTheme = 'default';
let accessibilitySettings = {
    highContrast: false,
    largeText: false,
    reducedMotion: false
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadUserPreferences();
    setupAccessibility();
});

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('🚀 EduMorph - AI-Powered Educational Platform');
    console.log('📚 Supporting SDG 4: Quality Education for All Ages');
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize modals
    initializeModals();
    
    // Initialize dropdowns
    initializeDropdowns();
    
    // Initialize mobile menu
    initializeMobileMenu();
    
    // Initialize flash messages
    initializeFlashMessages();
    
    // Initialize progress bars
    initializeProgressBars();
    
    // Setup keyboard navigation
    setupKeyboardNavigation();
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Theme switching
    document.addEventListener('click', function(e) {
        if (e.target.matches('[data-theme]')) {
            switchTheme(e.target.dataset.theme);
        }
    });
    
    // Accessibility toggles
    document.addEventListener('change', function(e) {
        if (e.target.matches('[data-accessibility]')) {
            toggleAccessibility(e.target.dataset.accessibility, e.target.checked);
        }
    });
    
    // Form validation
    document.addEventListener('input', function(e) {
        if (e.target.matches('.form-input')) {
            validateInput(e.target);
        }
    });
    
    // Window resize
    window.addEventListener('resize', debounce(handleResize, 250));
    
    // Scroll events
    window.addEventListener('scroll', throttle(handleScroll, 100));
}

/**
 * Load user preferences from localStorage
 */
function loadUserPreferences() {
    const savedTheme = localStorage.getItem('edumorph-theme');
    const savedAccessibility = localStorage.getItem('edumorph-accessibility');
    
    if (savedTheme) {
        switchTheme(savedTheme);
    }
    
    if (savedAccessibility) {
        try {
            accessibilitySettings = JSON.parse(savedAccessibility);
            applyAccessibilitySettings();
        } catch (e) {
            console.warn('Failed to parse accessibility settings:', e);
        }
    }
}

/**
 * Switch theme
 */
function switchTheme(theme) {
    // Remove existing theme classes
    document.body.classList.remove('children-theme', 'teens-theme', 'young-adults-theme', 'adults-theme');
    
    // Add new theme class
    if (theme !== 'default') {
        document.body.classList.add(`${theme}-theme`);
    }
    
    currentTheme = theme;
    localStorage.setItem('edumorph-theme', theme);
    
    // Update theme selector if exists
    const themeSelectors = document.querySelectorAll('[data-theme]');
    themeSelectors.forEach(selector => {
        selector.classList.toggle('active', selector.dataset.theme === theme);
    });
    
    // Announce theme change to screen readers
    announceToScreenReader(`Theme changed to ${theme}`);
}

/**
 * Toggle accessibility feature
 */
function toggleAccessibility(feature, enabled) {
    accessibilitySettings[feature] = enabled;
    localStorage.setItem('edumorph-accessibility', JSON.stringify(accessibilitySettings));
    applyAccessibilitySettings();
    
    // Announce change to screen readers
    announceToScreenReader(`${feature} ${enabled ? 'enabled' : 'disabled'}`);
}

/**
 * Apply accessibility settings
 */
function applyAccessibilitySettings() {
    const body = document.body;
    
    // High contrast
    body.classList.toggle('high-contrast', accessibilitySettings.highContrast);
    
    // Large text
    body.classList.toggle('large-text', accessibilitySettings.largeText);
    
    // Reduced motion
    body.classList.toggle('reduced-motion', accessibilitySettings.reducedMotion);
    
    // Update form controls
    const highContrastToggle = document.querySelector('[data-accessibility="highContrast"]');
    const largeTextToggle = document.querySelector('[data-accessibility="largeText"]');
    const reducedMotionToggle = document.querySelector('[data-accessibility="reducedMotion"]');
    
    if (highContrastToggle) highContrastToggle.checked = accessibilitySettings.highContrast;
    if (largeTextToggle) largeTextToggle.checked = accessibilitySettings.largeText;
    if (reducedMotionToggle) reducedMotionToggle.checked = accessibilitySettings.reducedMotion;
}

/**
 * Setup accessibility features
 */
function setupAccessibility() {
    // Add ARIA labels to interactive elements
    addAriaLabels();
    
    // Setup focus management
    setupFocusManagement();
    
    // Setup screen reader announcements
    setupScreenReaderAnnouncements();
    
    // Setup keyboard shortcuts
    setupKeyboardShortcuts();
}

/**
 * Add ARIA labels to interactive elements
 */
function addAriaLabels() {
    // Add labels to buttons without text
    const iconButtons = document.querySelectorAll('button:not([aria-label]):not([aria-labelledby])');
    iconButtons.forEach(button => {
        const icon = button.querySelector('i');
        if (icon) {
            const iconClass = icon.className;
            let label = 'Button';
            
            if (iconClass.includes('search')) label = 'Search';
            else if (iconClass.includes('menu')) label = 'Menu';
            else if (iconClass.includes('close')) label = 'Close';
            else if (iconClass.includes('edit')) label = 'Edit';
            else if (iconClass.includes('delete')) label = 'Delete';
            else if (iconClass.includes('save')) label = 'Save';
            else if (iconClass.includes('cancel')) label = 'Cancel';
            
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
    
    // Return focus after closing modals
    let lastFocusedElement = null;
    
    document.addEventListener('click', function(e) {
        if (e.target.matches('[data-modal-open]')) {
            lastFocusedElement = document.activeElement;
        }
    });
    
    document.addEventListener('click', function(e) {
        if (e.target.matches('[data-modal-close]') || e.target.matches('.modal-overlay')) {
            if (lastFocusedElement) {
                lastFocusedElement.focus();
                lastFocusedElement = null;
            }
        }
    });
}

/**
 * Trap focus within an element
 */
function trapFocus(e, element) {
    const focusableElements = element.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    if (e.shiftKey) {
        if (document.activeElement === firstElement) {
            lastElement.focus();
            e.preventDefault();
        }
    } else {
        if (document.activeElement === lastElement) {
            firstElement.focus();
            e.preventDefault();
        }
    }
}

/**
 * Setup screen reader announcements
 */
function setupScreenReaderAnnouncements() {
    // Create live region for announcements
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    liveRegion.id = 'live-region';
    document.body.appendChild(liveRegion);
}

/**
 * Announce message to screen readers
 */
function announceToScreenReader(message) {
    const liveRegion = document.getElementById('live-region');
    if (liveRegion) {
        liveRegion.textContent = message;
        setTimeout(() => {
            liveRegion.textContent = '';
        }, 1000);
    }
}

/**
 * Setup keyboard shortcuts
 */
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Alt + S: Focus search
        if (e.altKey && e.key === 's') {
            e.preventDefault();
            const searchInput = document.querySelector('.search-input');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Alt + M: Toggle mobile menu
        if (e.altKey && e.key === 'm') {
            e.preventDefault();
            const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
            if (mobileMenuToggle) {
                mobileMenuToggle.click();
            }
        }
        
        // Alt + H: Go to home
        if (e.altKey && e.key === 'h') {
            e.preventDefault();
            window.location.href = '/';
        }
        
        // Escape: Close modals/dropdowns
        if (e.key === 'Escape') {
            closeAllModals();
            closeAllDropdowns();
        }
    });
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        const tooltipText = element.dataset.tooltip;
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip-text';
        tooltip.textContent = tooltipText;
        tooltip.setAttribute('role', 'tooltip');
        element.appendChild(tooltip);
        element.classList.add('tooltip');
    });
}

/**
 * Initialize modals
 */
function initializeModals() {
    // Modal open buttons
    document.addEventListener('click', function(e) {
        if (e.target.matches('[data-modal-open]')) {
            const modalId = e.target.dataset.modalOpen;
            const modal = document.getElementById(modalId);
            if (modal) {
                openModal(modal);
            }
        }
    });
    
    // Modal close buttons
    document.addEventListener('click', function(e) {
        if (e.target.matches('[data-modal-close]') || e.target.matches('.modal-overlay')) {
            closeModal(e.target.closest('.modal'));
        }
    });
}

/**
 * Open modal
 */
function openModal(modal) {
    modal.classList.add('show');
    modal.setAttribute('aria-hidden', 'false');
    
    // Focus first focusable element
    const firstFocusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (firstFocusable) {
        firstFocusable.focus();
    }
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
    
    // Announce to screen readers
    announceToScreenReader('Modal opened');
}

/**
 * Close modal
 */
function closeModal(modal) {
    modal.classList.remove('show');
    modal.setAttribute('aria-hidden', 'true');
    
    // Restore body scroll
    document.body.style.overflow = '';
    
    // Announce to screen readers
    announceToScreenReader('Modal closed');
}

/**
 * Close all modals
 */
function closeAllModals() {
    const modals = document.querySelectorAll('.modal.show');
    modals.forEach(modal => closeModal(modal));
}

/**
 * Initialize dropdowns
 */
function initializeDropdowns() {
    document.addEventListener('click', function(e) {
        if (e.target.matches('[data-dropdown-toggle]')) {
            const dropdown = e.target.closest('.dropdown');
            const menu = dropdown.querySelector('.dropdown-menu');
            
            // Close other dropdowns
            closeAllDropdowns();
            
            // Toggle current dropdown
            menu.classList.toggle('show');
            e.target.setAttribute('aria-expanded', menu.classList.contains('show'));
        }
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            closeAllDropdowns();
        }
    });
}

/**
 * Close all dropdowns
 */
function closeAllDropdowns() {
    const dropdowns = document.querySelectorAll('.dropdown-menu.show');
    dropdowns.forEach(menu => {
        menu.classList.remove('show');
        const toggle = menu.closest('.dropdown').querySelector('[data-dropdown-toggle]');
        if (toggle) {
            toggle.setAttribute('aria-expanded', 'false');
        }
    });
}

/**
 * Initialize mobile menu
 */
function initializeMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const nav = document.querySelector('.main-nav');
    
    if (mobileToggle && nav) {
        mobileToggle.addEventListener('click', function() {
            const isOpen = nav.classList.contains('show');
            
            if (isOpen) {
                nav.classList.remove('show');
                mobileToggle.setAttribute('aria-expanded', 'false');
                mobileToggle.setAttribute('aria-label', 'Open mobile menu');
            } else {
                nav.classList.add('show');
                mobileToggle.setAttribute('aria-expanded', 'true');
                mobileToggle.setAttribute('aria-label', 'Close mobile menu');
            }
        });
    }
}

/**
 * Initialize flash messages
 */
function initializeFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        const closeBtn = message.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (message.parentNode) {
                message.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => {
                    message.remove();
                }, 300);
            }
        }, 5000);
    });
}

/**
 * Initialize progress bars
 */
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const fill = bar.querySelector('.progress-fill');
        const percentage = bar.dataset.percentage || 0;
        
        // Animate progress bar
        setTimeout(() => {
            fill.style.width = `${percentage}%`;
        }, 100);
    });
}

/**
 * Setup keyboard navigation
 */
function setupKeyboardNavigation() {
    // Tab navigation for custom elements
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            if (e.target.matches('[role="button"]') || e.target.matches('[data-clickable]')) {
                e.preventDefault();
                e.target.click();
            }
        }
    });
}

/**
 * Validate form input
 */
function validateInput(input) {
    const value = input.value.trim();
    const type = input.type;
    const required = input.hasAttribute('required');
    const minLength = input.getAttribute('minlength');
    const maxLength = input.getAttribute('maxlength');
    const pattern = input.getAttribute('pattern');
    
    let isValid = true;
    let errorMessage = '';
    
    // Required validation
    if (required && !value) {
        isValid = false;
        errorMessage = 'This field is required.';
    }
    
    // Length validation
    if (value && minLength && value.length < parseInt(minLength)) {
        isValid = false;
        errorMessage = `Minimum length is ${minLength} characters.`;
    }
    
    if (value && maxLength && value.length > parseInt(maxLength)) {
        isValid = false;
        errorMessage = `Maximum length is ${maxLength} characters.`;
    }
    
    // Pattern validation
    if (value && pattern && !new RegExp(pattern).test(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid format.';
    }
    
    // Email validation
    if (type === 'email' && value && !isValidEmail(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid email address.';
    }
    
    // Update input state
    updateInputState(input, isValid, errorMessage);
}

/**
 * Update input validation state
 */
function updateInputState(input, isValid, errorMessage) {
    const formGroup = input.closest('.form-group');
    const errorElement = formGroup?.querySelector('.form-error');
    
    // Remove existing error classes
    input.classList.remove('is-valid', 'is-invalid');
    
    if (isValid) {
        input.classList.add('is-valid');
        if (errorElement) {
            errorElement.textContent = '';
        }
    } else {
        input.classList.add('is-invalid');
        if (errorElement) {
            errorElement.textContent = errorMessage;
        }
    }
}

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Handle window resize
 */
function handleResize() {
    // Close mobile menu on desktop
    if (window.innerWidth > 768) {
        const nav = document.querySelector('.main-nav');
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        
        if (nav && nav.classList.contains('show')) {
            nav.classList.remove('show');
            if (mobileToggle) {
                mobileToggle.setAttribute('aria-expanded', 'false');
            }
        }
    }
}

/**
 * Handle scroll events
 */
function handleScroll() {
    const header = document.querySelector('.header');
    if (header) {
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
}

/**
 * Utility: Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Utility: Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Utility: Format date
 */
function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

/**
 * Utility: Format time
 */
function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

/**
 * Utility: Generate unique ID
 */
function generateId() {
    return Math.random().toString(36).substr(2, 9);
}

// Export functions for use in other scripts
window.EduMorph = {
    switchTheme,
    toggleAccessibility,
    announceToScreenReader,
    openModal,
    closeModal,
    formatDate,
    formatTime,
    generateId
};
