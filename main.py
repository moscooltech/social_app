"""
AI Content Generator - Mobile App
A productivity app for generating AI-powered social media content
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.clock import Clock
import threading

from api_client import APIClient
from storage import StorageManager

# Set window background color
Window.clearcolor = get_color_from_hex('#0A0E27')


class ModernButton(Button):
    """Custom button with modern styling"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = get_color_from_hex('#6366F1')
        self.color = get_color_from_hex('#FFFFFF')
        self.size_hint_y = None
        self.height = 50
        self.bold = True
        
        with self.canvas.before:
            Color(rgba=self.background_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class HomeScreen(Screen):
    """Main content generation screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = APIClient()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        header = Label(
            text='✨ AI Content Generator',
            font_size='28sp',
            size_hint_y=None,
            height=60,
            bold=True,
            color=get_color_from_hex('#A5B4FC')
        )
        layout.add_widget(header)
        
        # Prompt input
        prompt_label = Label(
            text='What do you want to create?',
            font_size='16sp',
            size_hint_y=None,
            height=30,
            color=get_color_from_hex('#E0E7FF')
        )
        layout.add_widget(prompt_label)
        
        self.prompt_input = TextInput(
            hint_text='e.g., "A motivational post about productivity"',
            multiline=True,
            size_hint_y=None,
            height=120,
            background_color=get_color_from_hex('#1E293B'),
            foreground_color=get_color_from_hex('#F1F5F9'),
            cursor_color=get_color_from_hex('#6366F1'),
            font_size='14sp',
            padding=[15, 15]
        )
        layout.add_widget(self.prompt_input)
        
        # Platform selector
        platform_label = Label(
            text='Platform',
            font_size='16sp',
            size_hint_y=None,
            height=30,
            color=get_color_from_hex('#E0E7FF')
        )
        layout.add_widget(platform_label)
        
        self.platform_spinner = Spinner(
            text='Twitter',
            values=('Twitter', 'LinkedIn', 'Instagram', 'Facebook', 'General'),
            size_hint_y=None,
            height=44,
            background_color=get_color_from_hex('#1E293B'),
            color=get_color_from_hex('#F1F5F9')
        )
        layout.add_widget(self.platform_spinner)
        
        # Tone selector
        tone_label = Label(
            text='Tone',
            font_size='16sp',
            size_hint_y=None,
            height=30,
            color=get_color_from_hex('#E0E7FF')
        )
        layout.add_widget(tone_label)
        
        self.tone_spinner = Spinner(
            text='Professional',
            values=('Professional', 'Casual', 'Enthusiastic', 'Formal', 'Funny', 'Inspirational'),
            size_hint_y=None,
            height=44,
            background_color=get_color_from_hex('#1E293B'),
            color=get_color_from_hex('#F1F5F9')
        )
        layout.add_widget(self.tone_spinner)
        
        # Generate buttons
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=50)
        
        self.generate_text_btn = ModernButton(text='Generate Text')
        self.generate_text_btn.bind(on_press=self.generate_text)
        btn_layout.add_widget(self.generate_text_btn)
        
        self.generate_image_btn = ModernButton(text='Generate Image')
        self.generate_image_btn.background_color = get_color_from_hex('#8B5CF6')
        self.generate_image_btn.bind(on_press=self.generate_image)
        btn_layout.add_widget(self.generate_image_btn)
        
        layout.add_widget(btn_layout)
        
        # Result display
        result_label = Label(
            text='Result',
            font_size='16sp',
            size_hint_y=None,
            height=30,
            color=get_color_from_hex('#E0E7FF')
        )
        layout.add_widget(result_label)
        
        scroll = ScrollView(size_hint=(1, 1))
        self.result_text = TextInput(
            text='Your generated content will appear here...',
            multiline=True,
            readonly=True,
            background_color=get_color_from_hex('#1E293B'),
            foreground_color=get_color_from_hex('#F1F5F9'),
            font_size='14sp',
            padding=[15, 15]
        )
        scroll.add_widget(self.result_text)
        layout.add_widget(scroll)
        
        # Bottom buttons
        bottom_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=50)
        
        settings_btn = ModernButton(text='⚙️ Settings')
        settings_btn.background_color = get_color_from_hex('#475569')
        settings_btn.bind(on_press=self.go_to_settings)
        bottom_layout.add_widget(settings_btn)
        
        history_btn = ModernButton(text='📚 History')
        history_btn.background_color = get_color_from_hex('#475569')
        history_btn.bind(on_press=self.go_to_history)
        bottom_layout.add_widget(history_btn)
        
        layout.add_widget(bottom_layout)
        
        self.add_widget(layout)
    
    def generate_text(self, instance):
        """Generate text content using AI"""
        prompt = self.prompt_input.text.strip()
        if not prompt:
            self.result_text.text = '❌ Please enter a prompt'
            return
        
        self.result_text.text = '⏳ Generating amazing content...'
        self.generate_text_btn.disabled = True
        
        def generate():
            try:
                content = self.api_client.generate_text(
                    prompt=prompt,
                    platform=self.platform_spinner.text,
                    tone=self.tone_spinner.text
                )
                Clock.schedule_once(lambda dt: self.show_result(content))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_error(str(e)))
            finally:
                Clock.schedule_once(lambda dt: setattr(self.generate_text_btn, 'disabled', False))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def generate_image(self, instance):
        """Generate image using AI"""
        prompt = self.prompt_input.text.strip()
        if not prompt:
            self.result_text.text = '❌ Please enter a prompt'
            return
        
        self.result_text.text = '🎨 Creating your image...'
        self.generate_image_btn.disabled = True
        
        def generate():
            try:
                image_url = self.api_client.generate_image(prompt)
                Clock.schedule_once(lambda dt: self.show_result(f'✅ Image generated!\n\n🔗 {image_url}\n\n(Image URL - long press to copy)'))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_error(str(e)))
            finally:
                Clock.schedule_once(lambda dt: setattr(self.generate_image_btn, 'disabled', False))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def show_result(self, content):
        """Display generated content"""
        self.result_text.text = content
        # Save to history
        storage = StorageManager()
        storage.save_post(
            prompt=self.prompt_input.text,
            content=content,
            platform=self.platform_spinner.text,
            tone=self.tone_spinner.text
        )
    
    def show_error(self, error):
        """Display error message"""
        self.result_text.text = f'❌ Error: {error}\n\nPlease check your API keys in Settings.'
    
    def go_to_settings(self, instance):
        self.manager.current = 'settings'
    
    def go_to_history(self, instance):
        self.manager.current = 'history'


class SettingsScreen(Screen):
    """Settings screen for API keys"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = StorageManager()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        header = Label(
            text='⚙️ Settings',
            font_size='28sp',
            size_hint_y=None,
            height=60,
            bold=True,
            color=get_color_from_hex('#A5B4FC')
        )
        layout.add_widget(header)
        
        # API Keys section
        scroll = ScrollView(size_hint=(1, 1))
        api_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        api_layout.bind(minimum_height=api_layout.setter('height'))
        
        # Gemini API Key
        api_layout.add_widget(Label(
            text='Gemini API Key (Google AI Studio)',
            font_size='14sp',
            size_hint_y=None,
            height=30,
            color=get_color_from_hex('#E0E7FF')
        ))
        self.gemini_key = TextInput(
            hint_text='Enter your Gemini API key',
            multiline=False,
            size_hint_y=None,
            height=44,
            background_color=get_color_from_hex('#1E293B'),
            foreground_color=get_color_from_hex('#F1F5F9'),
            password=True
        )
        api_layout.add_widget(self.gemini_key)
        
        # Groq API Key
        api_layout.add_widget(Label(
            text='Groq API Key',
            font_size='14sp',
            size_hint_y=None,
            height=30,
            color=get_color_from_hex('#E0E7FF')
        ))
        self.groq_key = TextInput(
            hint_text='Enter your Groq API key',
            multiline=False,
            size_hint_y=None,
            height=44,
            background_color=get_color_from_hex('#1E293B'),
            foreground_color=get_color_from_hex('#F1F5F9'),
            password=True
        )
        api_layout.add_widget(self.groq_key)
        
        # OpenRouter API Key
        api_layout.add_widget(Label(
            text='OpenRouter API Key',
            font_size='14sp',
            size_hint_y=None,
            height=30,
            color=get_color_from_hex('#E0E7FF')
        ))
        self.openrouter_key = TextInput(
            hint_text='Enter your OpenRouter API key',
            multiline=False,
            size_hint_y=None,
            height=44,
            background_color=get_color_from_hex('#1E293B'),
            foreground_color=get_color_from_hex('#F1F5F9'),
            password=True
        )
        api_layout.add_widget(self.openrouter_key)
        
        # Bytez API Key
        api_layout.add_widget(Label(
            text='Bytez API Key (for images)',
            font_size='14sp',
            size_hint_y=None,
            height=30,
            color=get_color_from_hex('#E0E7FF')
        ))
        self.bytez_key = TextInput(
            hint_text='Enter your Bytez API key',
            multiline=False,
            size_hint_y=None,
            height=44,
            background_color=get_color_from_hex('#1E293B'),
            foreground_color=get_color_from_hex('#F1F5F9'),
            password=True
        )
        api_layout.add_widget(self.bytez_key)
        
        scroll.add_widget(api_layout)
        layout.add_widget(scroll)
        
        # Buttons
        btn_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=50)
        
        save_btn = ModernButton(text='💾 Save')
        save_btn.bind(on_press=self.save_settings)
        btn_layout.add_widget(save_btn)
        
        back_btn = ModernButton(text='← Back')
        back_btn.background_color = get_color_from_hex('#475569')
        back_btn.bind(on_press=self.go_back)
        btn_layout.add_widget(back_btn)
        
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
        
        # Load saved keys
        self.load_settings()
    
    def load_settings(self):
        """Load saved API keys"""
        keys = self.storage.get_api_keys()
        self.gemini_key.text = keys.get('gemini', '')
        self.groq_key.text = keys.get('groq', '')
        self.openrouter_key.text = keys.get('openrouter', '')
        self.bytez_key.text = keys.get('bytez', '')
    
    def save_settings(self, instance):
        """Save API keys"""
        self.storage.save_api_keys({
            'gemini': self.gemini_key.text,
            'groq': self.groq_key.text,
            'openrouter': self.openrouter_key.text,
            'bytez': self.bytez_key.text
        })
        # Show feedback
        instance.text = '✅ Saved!'
        Clock.schedule_once(lambda dt: setattr(instance, 'text', '💾 Save'), 2)
    
    def go_back(self, instance):
        self.manager.current = 'home'


class HistoryScreen(Screen):
    """History of generated content"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = StorageManager()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        header_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        header = Label(
            text='📚 History',
            font_size='28sp',
            bold=True,
            color=get_color_from_hex('#A5B4FC')
        )
        header_layout.add_widget(header)
        
        refresh_btn = Button(
            text='🔄',
            size_hint_x=None,
            width=50,
            background_color=get_color_from_hex('#6366F1')
        )
        refresh_btn.bind(on_press=self.load_history)
        header_layout.add_widget(refresh_btn)
        
        layout.add_widget(header_layout)
        
        # History list
        scroll = ScrollView(size_hint=(1, 1))
        self.history_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll.add_widget(self.history_layout)
        layout.add_widget(scroll)
        
        # Back button
        back_btn = ModernButton(text='← Back')
        back_btn.background_color = get_color_from_hex('#475569')
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def on_enter(self):
        """Load history when screen is entered"""
        self.load_history()
    
    def load_history(self, instance=None):
        """Load and display history"""
        self.history_layout.clear_widgets()
        posts = self.storage.get_history()
        
        if not posts:
            self.history_layout.add_widget(Label(
                text='No history yet.\nGenerate some content to see it here!',
                font_size='14sp',
                color=get_color_from_hex('#94A3B8'),
                size_hint_y=None,
                height=100
            ))
            return
        
        for post in posts:
            item = BoxLayout(orientation='vertical', size_hint_y=None, height=120, padding=10, spacing=5)
            
            with item.canvas.before:
                Color(rgba=get_color_from_hex('#1E293B'))
                item.rect = RoundedRectangle(pos=item.pos, size=item.size, radius=[10])
            item.bind(pos=lambda i, p: setattr(i.rect, 'pos', p), size=lambda i, s: setattr(i.rect, 'size', s))
            
            # Metadata
            meta = Label(
                text=f"{post['platform']} • {post['tone']} • {post['created_at'][:16]}",
                font_size='11sp',
                size_hint_y=None,
                height=20,
                color=get_color_from_hex('#94A3B8')
            )
            item.add_widget(meta)
            
            # Content preview
            content_preview = post['content'][:100] + ('...' if len(post['content']) > 100 else '')
            content = Label(
                text=content_preview,
                font_size='12sp',
                size_hint_y=None,
                height=60,
                color=get_color_from_hex('#E0E7FF'),
                text_size=(Window.width - 60, None)
            )
            item.add_widget(content)
            
            self.history_layout.add_widget(item)
    
    def go_back(self, instance):
        self.manager.current = 'home'


class AIContentGeneratorApp(App):
    """Main application class"""
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(HistoryScreen(name='history'))
        return sm


if __name__ == '__main__':
    AIContentGeneratorApp().run()
