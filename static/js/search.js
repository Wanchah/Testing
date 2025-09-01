/**
 * EduMorph - Search Functionality
 * Smart search with autocomplete and instant results
 */

// Search state
let searchState = {
    isSearching: false,
    currentQuery: '',
    suggestions: [],
    results: [],
    debounceTimer: null
};

// Initialize search when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
});

/**
 * Initialize search functionality
 */
function initializeSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchForm = document.querySelector('.search-form');
    const suggestionsContainer = document.querySelector('.search-suggestions');
    
    if (!searchInput || !searchForm) return;
    
    // Input event for autocomplete
    searchInput.addEventListener('input', handleSearchInput);
    
    // Form submission
    searchForm.addEventListener('submit', handleSearchSubmit);
    
    // Focus events
    searchInput.addEventListener('focus', handleSearchFocus);
    searchInput.addEventListener('blur', handleSearchBlur);
    
    // Keyboard navigation
    searchInput.addEventListener('keydown', handleSearchKeydown);
    
    // Click outside to close suggestions
    document.addEventListener('click', handleClickOutside);
    
    console.log('🔍 Search functionality initialized');
}

/**
 * Handle search input
 */
function handleSearchInput(e) {
    const query = e.target.value.trim();
    searchState.currentQuery = query;
    
    // Clear previous timer
    if (searchState.debounceTimer) {
        clearTimeout(searchState.debounceTimer);
    }
    
    // Debounce search requests
    searchState.debounceTimer = setTimeout(() => {
        if (query.length >= 2) {
            fetchSuggestions(query);
        } else {
            hideSuggestions();
        }
    }, 300);
}

/**
 * Handle search form submission
 */
function handleSearchSubmit(e) {
    e.preventDefault();
    
    const query = searchState.currentQuery.trim();
    if (!query) return;
    
    // Hide suggestions
    hideSuggestions();
    
    // Perform search
    performSearch(query);
}

/**
 * Handle search input focus
 */
function handleSearchFocus(e) {
    const suggestionsContainer = document.querySelector('.search-suggestions');
    if (suggestionsContainer && suggestionsContainer.children.length > 0) {
        showSuggestions();
    }
}

/**
 * Handle search input blur
 */
function handleSearchBlur(e) {
    // Delay hiding to allow clicking on suggestions
    setTimeout(() => {
        hideSuggestions();
    }, 200);
}

/**
 * Handle keyboard navigation in search
 */
function handleSearchKeydown(e) {
    const suggestionsContainer = document.querySelector('.search-suggestions');
    const suggestions = suggestionsContainer?.querySelectorAll('.suggestion-item');
    
    if (!suggestions || suggestions.length === 0) return;
    
    const currentIndex = Array.from(suggestions).findIndex(item => 
        item.classList.contains('active')
    );
    
    switch (e.key) {
        case 'ArrowDown':
            e.preventDefault();
            navigateSuggestions(suggestions, currentIndex + 1);
            break;
            
        case 'ArrowUp':
            e.preventDefault();
            navigateSuggestions(suggestions, currentIndex - 1);
            break;
            
        case 'Enter':
            e.preventDefault();
            if (currentIndex >= 0) {
                selectSuggestion(suggestions[currentIndex]);
            } else {
                // Submit form if no suggestion is selected
                const searchForm = document.querySelector('.search-form');
                searchForm.dispatchEvent(new Event('submit'));
            }
            break;
            
        case 'Escape':
            hideSuggestions();
            break;
    }
}

/**
 * Navigate through suggestions
 */
function navigateSuggestions(suggestions, newIndex) {
    // Remove active class from all suggestions
    suggestions.forEach(item => item.classList.remove('active'));
    
    // Handle bounds
    if (newIndex < 0) {
        newIndex = suggestions.length - 1;
    } else if (newIndex >= suggestions.length) {
        newIndex = 0;
    }
    
    // Add active class to current suggestion
    if (suggestions[newIndex]) {
        suggestions[newIndex].classList.add('active');
        suggestions[newIndex].scrollIntoView({ block: 'nearest' });
    }
}

/**
 * Select a suggestion
 */
function selectSuggestion(suggestionItem) {
    const query = suggestionItem.textContent.trim();
    const searchInput = document.querySelector('.search-input');
    
    if (searchInput) {
        searchInput.value = query;
        searchState.currentQuery = query;
    }
    
    hideSuggestions();
    performSearch(query);
}

/**
 * Handle clicks outside search
 */
function handleClickOutside(e) {
    const searchContainer = document.querySelector('.search-container');
    if (searchContainer && !searchContainer.contains(e.target)) {
        hideSuggestions();
    }
}

/**
 * Fetch search suggestions
 */
async function fetchSuggestions(query) {
    if (searchState.isSearching) return;
    
    try {
        searchState.isSearching = true;
        
        const response = await fetch(`/search/autocomplete?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.suggestions) {
            searchState.suggestions = data.suggestions;
            displaySuggestions(data.suggestions);
        }
        
    } catch (error) {
        console.error('Error fetching suggestions:', error);
        hideSuggestions();
    } finally {
        searchState.isSearching = false;
    }
}

/**
 * Display search suggestions
 */
function displaySuggestions(suggestions) {
    const suggestionsContainer = document.querySelector('.search-suggestions');
    if (!suggestionsContainer) return;
    
    // Clear existing suggestions
    suggestionsContainer.innerHTML = '';
    
    if (suggestions.length === 0) {
        hideSuggestions();
        return;
    }
    
    // Create suggestion items
    suggestions.forEach((suggestion, index) => {
        const item = document.createElement('div');
        item.className = 'suggestion-item';
        item.textContent = suggestion;
        item.setAttribute('role', 'option');
        item.setAttribute('tabindex', '-1');
        
        // Add click handler
        item.addEventListener('click', () => selectSuggestion(item));
        
        // Add hover handler
        item.addEventListener('mouseenter', () => {
            // Remove active from all items
            suggestionsContainer.querySelectorAll('.suggestion-item').forEach(i => 
                i.classList.remove('active')
            );
            // Add active to current item
            item.classList.add('active');
        });
        
        suggestionsContainer.appendChild(item);
    });
    
    showSuggestions();
}

/**
 * Show suggestions container
 */
function showSuggestions() {
    const suggestionsContainer = document.querySelector('.search-suggestions');
    if (suggestionsContainer) {
        suggestionsContainer.classList.add('show');
        suggestionsContainer.setAttribute('aria-expanded', 'true');
    }
}

/**
 * Hide suggestions container
 */
function hideSuggestions() {
    const suggestionsContainer = document.querySelector('.search-suggestions');
    if (suggestionsContainer) {
        suggestionsContainer.classList.remove('show');
        suggestionsContainer.setAttribute('aria-expanded', 'false');
        
        // Remove active class from all items
        suggestionsContainer.querySelectorAll('.suggestion-item').forEach(item => 
            item.classList.remove('active')
        );
    }
}

/**
 * Perform search
 */
async function performSearch(query) {
    if (!query.trim()) return;
    
    try {
        // Show loading state
        showSearchLoading();
        
        const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.results) {
            searchState.results = data.results;
            displaySearchResults(data.results, query);
        }
        
    } catch (error) {
        console.error('Error performing search:', error);
        showSearchError('Failed to perform search. Please try again.');
    } finally {
        hideSearchLoading();
    }
}

/**
 * Display search results
 */
function displaySearchResults(results, query) {
    // This would typically navigate to a search results page
    // For now, we'll just log the results
    console.log('Search results for:', query, results);
    
    // If we're on a search results page, update the content
    const resultsContainer = document.querySelector('.search-results');
    if (resultsContainer) {
        updateSearchResultsPage(results, query);
    } else {
        // Navigate to search results page
        window.location.href = `/search?q=${encodeURIComponent(query)}`;
    }
}

/**
 * Update search results page
 */
function updateSearchResultsPage(results, query) {
    const resultsContainer = document.querySelector('.search-results');
    const queryDisplay = document.querySelector('.search-query');
    const resultsCount = document.querySelector('.results-count');
    
    if (!resultsContainer) return;
    
    // Update query display
    if (queryDisplay) {
        queryDisplay.textContent = query;
    }
    
    // Update results count
    if (resultsCount) {
        resultsCount.textContent = `${results.length} result${results.length !== 1 ? 's' : ''} found`;
    }
    
    // Clear existing results
    resultsContainer.innerHTML = '';
    
    if (results.length === 0) {
        showNoResults(query);
        return;
    }
    
    // Create result items
    results.forEach(result => {
        const resultItem = createResultItem(result);
        resultsContainer.appendChild(resultItem);
    });
}

/**
 * Create a search result item
 */
function createResultItem(result) {
    const item = document.createElement('div');
    item.className = 'search-result-item';
    
    const typeIcon = getTypeIcon(result.type);
    const typeLabel = getTypeLabel(result.type);
    
    item.innerHTML = `
        <div class="result-header">
            <div class="result-type">
                <i class="${typeIcon}"></i>
                <span>${typeLabel}</span>
            </div>
            <div class="result-meta">
                ${result.age_group ? `<span class="age-group">${result.age_group}</span>` : ''}
                ${result.difficulty ? `<span class="difficulty difficulty-${result.difficulty}">${result.difficulty}</span>` : ''}
            </div>
        </div>
        <h3 class="result-title">
            <a href="${result.url}">${highlightQuery(result.title, searchState.currentQuery)}</a>
        </h3>
        <p class="result-description">
            ${highlightQuery(result.description || '', searchState.currentQuery)}
        </p>
        <div class="result-footer">
            ${result.topic ? `<span class="topic">${result.topic}</span>` : ''}
            ${result.subject ? `<span class="subject">${result.subject}</span>` : ''}
            ${result.duration ? `<span class="duration">${result.duration} min</span>` : ''}
        </div>
    `;
    
    return item;
}

/**
 * Get icon for content type
 */
function getTypeIcon(type) {
    const icons = {
        lesson: 'fas fa-book-open',
        flashcard: 'fas fa-cards-blank',
        question: 'fas fa-question-circle',
        resource: 'fas fa-external-link-alt'
    };
    return icons[type] || 'fas fa-file';
}

/**
 * Get label for content type
 */
function getTypeLabel(type) {
    const labels = {
        lesson: 'Lesson',
        flashcard: 'Flashcard',
        question: 'Question',
        resource: 'Resource'
    };
    return labels[type] || 'Content';
}

/**
 * Highlight search query in text
 */
function highlightQuery(text, query) {
    if (!query || !text) return text;
    
    const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

/**
 * Escape special regex characters
 */
function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Show no results message
 */
function showNoResults(query) {
    const resultsContainer = document.querySelector('.search-results');
    if (!resultsContainer) return;
    
    resultsContainer.innerHTML = `
        <div class="no-results">
            <i class="fas fa-search"></i>
            <h3>No results found for "${query}"</h3>
            <p>Try different keywords or check your spelling.</p>
            <div class="search-tips">
                <h4>Search Tips:</h4>
                <ul>
                    <li>Try more general terms</li>
                    <li>Check your spelling</li>
                    <li>Use different keywords</li>
                    <li>Browse by subject or age group</li>
                </ul>
            </div>
        </div>
    `;
}

/**
 * Show search loading state
 */
function showSearchLoading() {
    const searchButton = document.querySelector('.search-button');
    if (searchButton) {
        searchButton.classList.add('loading');
        searchButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    }
}

/**
 * Hide search loading state
 */
function hideSearchLoading() {
    const searchButton = document.querySelector('.search-button');
    if (searchButton) {
        searchButton.classList.remove('loading');
        searchButton.innerHTML = '<i class="fas fa-search"></i>';
    }
}

/**
 * Show search error
 */
function showSearchError(message) {
    const searchContainer = document.querySelector('.search-container');
    if (!searchContainer) return;
    
    // Remove existing error
    const existingError = searchContainer.querySelector('.search-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Create error message
    const error = document.createElement('div');
    error.className = 'search-error';
    error.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <span>${message}</span>
    `;
    
    searchContainer.appendChild(error);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        error.remove();
    }, 5000);
}

/**
 * Voice search functionality
 */
function initializeVoiceSearch() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        return; // Voice search not supported
    }
    
    const searchInput = document.querySelector('.search-input');
    const searchButton = document.querySelector('.search-button');
    
    if (!searchInput || !searchButton) return;
    
    // Add voice search button
    const voiceButton = document.createElement('button');
    voiceButton.type = 'button';
    voiceButton.className = 'voice-search-button';
    voiceButton.innerHTML = '<i class="fas fa-microphone"></i>';
    voiceButton.setAttribute('aria-label', 'Voice search');
    voiceButton.setAttribute('title', 'Voice search');
    
    // Insert before search button
    searchButton.parentNode.insertBefore(voiceButton, searchButton);
    
    // Voice search functionality
    voiceButton.addEventListener('click', startVoiceSearch);
}

/**
 * Start voice search
 */
function startVoiceSearch() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    const searchInput = document.querySelector('.search-input');
    const voiceButton = document.querySelector('.voice-search-button');
    
    if (!searchInput || !voiceButton) return;
    
    // Update button state
    voiceButton.classList.add('listening');
    voiceButton.innerHTML = '<i class="fas fa-stop"></i>';
    voiceButton.setAttribute('aria-label', 'Stop listening');
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        searchInput.value = transcript;
        searchState.currentQuery = transcript;
        
        // Perform search
        performSearch(transcript);
    };
    
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        showSearchError('Voice search failed. Please try again.');
    };
    
    recognition.onend = function() {
        voiceButton.classList.remove('listening');
        voiceButton.innerHTML = '<i class="fas fa-microphone"></i>';
        voiceButton.setAttribute('aria-label', 'Voice search');
    };
    
    recognition.start();
}

// Initialize voice search when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeVoiceSearch();
});

// Export search functions
window.EduMorphSearch = {
    performSearch,
    fetchSuggestions,
    highlightQuery
};
