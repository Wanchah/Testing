"""
EduMorph Settings Blueprint
Handles user preferences, theme customization, and layout settings.

This module provides:
- Theme customization (colors, fonts, backgrounds)
- Layout preferences
- Accessibility settings
- User profile customization
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from database.models import db, User
import json

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/')
@login_required
def index():
    """Main settings page with all customization options."""
    return render_template('settings/index.html')

@settings_bp.route('/themes')
@login_required
def themes():
    """Theme customization page."""
    return render_template('settings/themes.html')

@settings_bp.route('/layout')
@login_required
def layout():
    """Layout customization page."""
    return render_template('settings/layout.html')

@settings_bp.route('/accessibility')
@login_required
def accessibility():
    """Accessibility settings page."""
    return render_template('settings/accessibility.html')

@settings_bp.route('/api/update-theme', methods=['POST'])
@login_required
def update_theme():
    """Update user's theme preferences."""
    try:
        data = request.get_json()
        
        # Update theme preferences
        if 'theme_preference' in data:
            current_user.theme_preference = data['theme_preference']
        
        if 'color_scheme' in data:
            current_user.color_scheme = data['color_scheme']
        
        if 'font_size' in data:
            current_user.font_size = data['font_size']
        
        if 'font_family' in data:
            current_user.font_family = data['font_family']
        
        if 'background_color' in data:
            current_user.background_color = data['background_color']
        
        if 'accent_color' in data:
            current_user.accent_color = data['accent_color']
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Theme updated successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@settings_bp.route('/api/update-layout', methods=['POST'])
@login_required
def update_layout():
    """Update user's layout preferences."""
    try:
        data = request.get_json()
        
        # Update layout preferences
        if 'sidebar_position' in data:
            current_user.sidebar_position = data['sidebar_position']
        
        if 'content_width' in data:
            current_user.content_width = data['content_width']
        
        if 'navigation_style' in data:
            current_user.navigation_style = data['navigation_style']
        
        if 'card_layout' in data:
            current_user.card_layout = data['card_layout']
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Layout updated successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@settings_bp.route('/api/update-accessibility', methods=['POST'])
@login_required
def update_accessibility():
    """Update user's accessibility preferences."""
    try:
        data = request.get_json()
        
        # Update accessibility preferences
        if 'high_contrast' in data:
            current_user.high_contrast = data['high_contrast']
        
        if 'reduced_motion' in data:
            current_user.reduced_motion = data['reduced_motion']
        
        if 'screen_reader_support' in data:
            current_user.screen_reader_support = data['screen_reader_support']
        
        if 'focus_indicators' in data:
            current_user.focus_indicators = data['focus_indicators']
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Accessibility settings updated successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@settings_bp.route('/api/get-preferences')
@login_required
def get_preferences():
    """Get current user's preferences."""
    try:
        preferences = {
            'theme_preference': current_user.theme_preference,
            'color_scheme': current_user.color_scheme,
            'font_size': current_user.font_size,
            'font_family': current_user.font_family,
            'background_color': current_user.background_color,
            'accent_color': current_user.accent_color,
            'sidebar_position': current_user.sidebar_position,
            'content_width': current_user.content_width,
            'navigation_style': current_user.navigation_style,
            'card_layout': current_user.card_layout,
            'high_contrast': current_user.high_contrast,
            'reduced_motion': current_user.reduced_motion,
            'screen_reader_support': current_user.screen_reader_support,
            'focus_indicators': current_user.focus_indicators
        }
        
        return jsonify({'success': True, 'preferences': preferences})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@settings_bp.route('/api/reset-preferences', methods=['POST'])
@login_required
def reset_preferences():
    """Reset user's preferences to defaults."""
    try:
        # Reset to default values
        current_user.theme_preference = 'modern'
        current_user.color_scheme = 'default'
        current_user.font_size = 'medium'
        current_user.font_family = 'system'
        current_user.background_color = '#ffffff'
        current_user.accent_color = '#4f46e5'
        current_user.sidebar_position = 'left'
        current_user.content_width = 'standard'
        current_user.navigation_style = 'standard'
        current_user.card_layout = 'grid'
        current_user.high_contrast = False
        current_user.reduced_motion = False
        current_user.screen_reader_support = False
        current_user.focus_indicators = True
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Preferences reset to defaults'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
