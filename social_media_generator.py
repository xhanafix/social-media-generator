import random
import os
import requests
import json
from typing import Dict, List, Optional
from dotenv import load_dotenv
from datetime import datetime

# Add debugging information
print("Current working directory:", os.getcwd())
print("Files in directory:", os.listdir())
load_dotenv()
print("Environment variables after load_dotenv:", os.environ.get('OPENROUTER_API_KEY'))

class SocialMediaPostGenerator:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # OpenRouter configuration
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        print("API Key found:", bool(self.api_key))  # Debug print
        self.api_base = "https://openrouter.ai/api/v1"
        self.default_model = "deepseek/deepseek-chat-v3-0324:free"  # You can change this to any model supported by OpenRouter
        
        # Timeout settings (in seconds) - increased for better handling of longer content
        self.timeouts = {
            'short': 30,    # Increased for more content
            'medium': 60,   # Increased for longer content
            'long': 90      # Increased for longest content
        }
        
        # Token limits for different lengths
        self.token_limits = {
            'short': 400,   # Approximately 300 words
            'medium': 1200, # Approximately 900 words
            'long': 2000    # Approximately 1500 words
        }
        
        # History file path
        self.history_file = "post_history.json"
        self.history = self._load_history()
        
        self.emojis = {
            'inspirational': ['✨', '🌟', '💫', '💪', '🔥'],
            'urgent': ['⚡', '⏰', '🚨', '💥', '❗'],
            'emotional': ['❤️', '😊', '🥺', '😌', '🙏'],
            'empathetic': ['🤗', '💝', '💕', '🤝', '💫'],
            'professional': ['💼', '📊', '📈', '🎯', '💡'],
            'friendly': ['😊', '👋', '💫', '✨', '💕'],
            'casual': ['😎', '👍', '💯', '🔥', '✨']
        }
        
        # Language-specific CTAs
        self.cta_templates = {
            'EN': {
                'Facebook': [
                    "💬 What's your take on this?",
                    "Share this if you agree!",
                    "Tag someone who needs to see this!",
                    "Drop a ❤️ if this resonates with you!"
                ],
                'Instagram': [
                    "Double tap if you agree!",
                    "Tag a friend who needs this!",
                    "Save this for later!",
                    "Follow for more content like this!"
                ],
                'LinkedIn': [
                    "What are your thoughts on this?",
                    "Share your experience in the comments!",
                    "Connect if this resonates with you!",
                    "Follow for more professional insights!"
                ],
                'Twitter': [
                    "RT if you agree!",
                    "Like & follow for more!",
                    "What's your take?",
                    "Share your thoughts below!"
                ],
                'TikTok': [
                    "Follow for more! 🎵",
                    "Drop a ❤️ if you agree!",
                    "Save this for later! 📱",
                    "Comment your thoughts below! 💭",
                    "Share with someone who needs this! 🔄",
                    "Double tap if you relate! 👆"
                ]
            },
            'BM': {
                'Facebook': [
                    "💬 Apa pendapat kau?",
                    "Kongsi kalau kau setuju!",
                    "Tag kawan yang perlu tengok ni!",
                    "Tekan ❤️ kalau kau rasa sama!"
                ],
                'Instagram': [
                    "Double tap kalau kau setuju!",
                    "Tag kawan yang perlukan ni!",
                    "Simpan untuk tengok balik!",
                    "Follow untuk lebih banyak content!"
                ],
                'LinkedIn': [
                    "Apa pendapat kau?",
                    "Kongsi pengalaman kau dalam komen!",
                    "Connect kalau kau rasa sama!",
                    "Follow untuk lebih banyak insight!"
                ],
                'Twitter': [
                    "RT kalau kau setuju!",
                    "Like & follow untuk lebih banyak!",
                    "Apa pendapat kau?",
                    "Kongsi pendapat kau kat bawah!"
                ],
                'TikTok': [
                    "Follow untuk lebih banyak! 🎵",
                    "Tekan ❤️ kalau kau setuju!",
                    "Simpan untuk tengok balik! 📱",
                    "Komen pendapat kau kat bawah! 💭",
                    "Kongsi dengan kawan yang perlukan! 🔄",
                    "Double tap kalau kau rasa sama! 👆"
                ]
            }
        }

        # Platform-specific formatting
        self.platform_formats = {
            'TikTok': {
                'max_length': 150,  # TikTok caption character limit
                'hashtag_style': True,
                'emojis_per_line': 2,
                'line_breaks': True
            }
        }

    def _load_history(self) -> List[Dict]:
        """Load post history from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading history: {e}")
            return []

    def _save_history(self):
        """Save post history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

    def _format_for_platform(self, content: str, platform: str) -> str:
        """Format content according to platform-specific rules."""
        if platform not in self.platform_formats:
            return content

        format_rules = self.platform_formats[platform]
        
        # Add line breaks for TikTok
        if format_rules.get('line_breaks'):
            # Split into sentences and add line breaks
            sentences = content.split('. ')
            content = '.\n\n'.join(sentences)
        
        # Add hashtags for TikTok
        if format_rules.get('hashtag_style'):
            # Extract key words and add hashtags
            words = content.split()
            hashtags = [f"#{word.lower()}" for word in words if len(word) > 3][:5]
            if hashtags:
                content += "\n\n" + " ".join(hashtags)
        
        return content

    def _generate_ai_content(self, topic: str, length: str, platform: str, tone: str, language: str = 'EN') -> str:
        """Generate content using OpenRouter API with timeout."""
        language_instruction = "Write in English" if language == 'EN' else "Write in Bahasa Malaysia"
        
        # Add word count instructions based on length
        word_count_instruction = {
            'short': "Write approximately 300 words",
            'medium': "Write approximately 900 words",
            'long': "Write approximately 1500 words"
        }.get(length.lower(), "Write appropriate length")
        
        prompt = f"""Create a {tone.lower()} social media post about {topic} for {platform}.
        {language_instruction}.
        {word_count_instruction}.
        Write in second-person perspective (using 'you' and 'your').
        
        IMPORTANT GUIDELINES:
        1. Only include verified, factual information
        2. Avoid making unsubstantiated claims
        3. If citing statistics or facts, ensure they are from reliable sources
        4. Do not generate content that could be misleading or false
        5. Focus on well-established, widely accepted information
        6. If uncertain about a fact, either omit it or clearly indicate it's an opinion
        
        Make it engaging, emotional, and authentic while maintaining accuracy.
        Include relevant emojis naturally in the text.
        Focus on storytelling and relatability.
        For long posts, ensure the content is well-structured with clear paragraphs.
        Format: Return only the post content, no additional text."""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "https://github.com/yourusername/social-media-generator",
                "X-Title": "Social Media Post Generator"
            }

            # Get token limit based on length
            max_tokens = self.token_limits.get(length.lower(), 400)

            data = {
                "model": self.default_model,
                "messages": [
                    {"role": "system", "content": f"""You are a creative social media copywriter who specializes in writing engaging, emotionally resonant posts in {language}. 
                    Your primary responsibility is to ensure all information is factual and verified.
                    For Bahasa Malaysia posts, use casual language with 'aku' and 'kau' instead of formal 'saya' and 'kamu'.
                    Use 'you' and 'your' to create a personal connection with the reader.
                    For long posts, ensure proper paragraph breaks and structure.
                    Never generate content that could be misleading or false.
                    If you're unsure about a fact, either omit it or clearly mark it as an opinion.
                    Always prioritize accuracy over engagement."""},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.5,  # Reduced temperature for more factual output
                "presence_penalty": 0.6,
                "frequency_penalty": 0.3
            }

            # Set timeout based on length
            timeout = self.timeouts.get(length.lower(), 30)
            
            print(f"Generating {length} post in {language} with {max_tokens} tokens and {timeout}s timeout")
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=timeout
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content'].strip()
                # Ensure proper paragraph breaks for long content
                if length.lower() == 'long':
                    content = self._format_long_content(content)
                return self._format_for_platform(content, platform)
            else:
                print(f"Error from OpenRouter API: {response.status_code} - {response.text}")
                return self._generate_fallback_content(topic, length, tone, language)
                
        except requests.Timeout:
            print(f"Request timed out after {timeout} seconds")
            return self._generate_fallback_content(topic, length, tone, language)
        except Exception as e:
            print(f"Error generating AI content: {e}")
            return self._generate_fallback_content(topic, length, tone, language)

    def _format_long_content(self, content: str) -> str:
        """Format long content with proper paragraph breaks and structure."""
        # Split into sentences
        sentences = content.split('. ')
        
        # Group sentences into paragraphs (3-4 sentences per paragraph)
        paragraphs = []
        current_paragraph = []
        
        for sentence in sentences:
            current_paragraph.append(sentence)
            if len(current_paragraph) >= 3:
                paragraphs.append('. '.join(current_paragraph) + '.')
                current_paragraph = []
        
        # Add any remaining sentences
        if current_paragraph:
            paragraphs.append('. '.join(current_paragraph) + '.')
        
        # Join paragraphs with double line breaks
        return '\n\n'.join(paragraphs)

    def _generate_fallback_content(self, topic: str, length: str, tone: str, language: str = 'EN') -> str:
        """Generate fallback content if AI generation fails."""
        if length.lower() == 'short':
            return self._generate_short_post(topic, tone, language)
        elif length.lower() == 'medium':
            return self._generate_medium_post(topic, tone, language)
        else:
            # For long posts, combine multiple medium posts with proper formatting
            content = self._generate_medium_post(topic, tone, language)
            content += "\n\n" + self._generate_medium_post(topic, tone, language)
            return self._format_long_content(content)

    def generate_post(self, topic: str, length: str, platform: str, tone: str, language: str = 'EN') -> Dict[str, str]:
        """Generate a social media post and save to history."""
        # Generate AI content
        content = self._generate_ai_content(topic, length, platform, tone, language)
            
        # Add CTA
        cta = random.choice(self.cta_templates[language].get(platform, self.cta_templates[language]['Facebook']))
        content += f"\n\n{cta}"
        
        # Generate image suggestions
        image_suggestions = self._generate_image_suggestions(topic, tone)
        
        # Create result
        result = {
            'content': content,
            'image_suggestions': image_suggestions,
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                'topic': topic,
                'length': length,
                'platform': platform,
                'tone': tone,
                'language': language
            }
        }
        
        # Save to history
        self.history.append(result)
        self._save_history()
        
        return result

    def get_history(self, limit: int = 10) -> List[Dict]:
        """Get recent post history."""
        return self.history[-limit:]

    def clear_history(self):
        """Clear post history."""
        self.history = []
        self._save_history()

    def _generate_short_post(self, topic: str, tone: str, language: str = 'EN') -> str:
        """Generate a short post (suitable for Twitter)."""
        templates = {
            'EN': [
                f"✨ Struggling with {topic}? Here's what you need to know...",
                f"💡 Want to master {topic}? Start with this...",
                f"🚀 Your journey to {topic} begins here:",
                f"💪 Transform your {topic} with this simple tip:"
            ],
            'BM': [
                f"✨ Bermasalah dengan {topic}? Ini yang kau perlu tahu...",
                f"💡 Mahu kuasai {topic}? Mulakan dengan ni...",
                f"🚀 Perjalanan kau ke arah {topic} bermula kat sini:",
                f"💪 Ubah {topic} kau dengan tip mudah ni:"
            ]
        }
        return random.choice(templates[language])
    
    def _generate_medium_post(self, topic: str, tone: str, language: str = 'EN') -> str:
        """Generate a medium-length post (suitable for Facebook/Instagram)."""
        templates = {
            'EN': [
                f"✨ Struggling with {topic}?\n\nYou're not alone. Here's what changed everything for me...",
                f"💡 The truth about {topic} that nobody tells you:\n\n",
                f"🚀 Want to transform your {topic}?\n\nHere's how I did it:",
                f"💪 Your {topic} doesn't have to be complicated.\n\nHere's why:"
            ],
            'BM': [
                f"✨ Bermasalah dengan {topic}?\n\nKau tak keseorangan. Ini yang mengubah segalanya untuk aku...",
                f"💡 Kebenaran tentang {topic} yang tiada siapa beritahu kau:\n\n",
                f"🚀 Mahu ubah {topic} kau?\n\nIni cara aku lakukannya:",
                f"💪 {topic} kau tak perlu rumit.\n\nIni sebabnya:"
            ]
        }
        return random.choice(templates[language])
    
    def _generate_long_post(self, topic: str, tone: str, language: str = 'EN') -> str:
        """Generate a long post (suitable for LinkedIn/Facebook)."""
        templates = {
            'EN': [
                f"✨ Your complete guide to {topic}:\n\nHere's everything you need to know...",
                f"💡 Your journey with {topic} and what you'll learn:\n\n",
                f"🚀 Transform your {topic} with these proven strategies:\n\n",
                f"💪 Master your {topic} with these expert tips:\n\n"
            ],
            'BM': [
                f"✨ Panduan lengkap kau untuk {topic}:\n\nIni semua yang kau perlu tahu...",
                f"💡 Perjalanan kau dengan {topic} dan apa yang kau akan pelajari:\n\n",
                f"🚀 Ubah {topic} kau dengan strategi yang terbukti ini:\n\n",
                f"💪 Kuasai {topic} kau dengan tip pakar ini:\n\n"
            ]
        }
        return random.choice(templates[language])
    
    def _generate_image_suggestions(self, topic: str, tone: str) -> List[str]:
        """Generate relevant image suggestions based on topic and tone."""
        try:
            headers = {
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "anthropic/claude-3-opus-20240229",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a creative social media expert. Generate 2 specific and relevant image suggestions that would perfectly complement a social media post about the given topic and tone. Make the suggestions detailed and specific to the content."
                    },
                    {
                        "role": "user",
                        "content": f"Generate 2 specific image suggestions for a social media post about {topic} with a {tone} tone. The suggestions should be detailed and directly relevant to the content."
                    }
                ]
            }
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content'].strip()
                # Split the response into individual suggestions
                suggestions = [s.strip() for s in content.split('\n') if s.strip()]
                # Take the first 2 suggestions
                return suggestions[:2]
            else:
                # Fallback to generic suggestions if API call fails
                return [
                    f"A person looking determined while working on {topic}",
                    f"A split image showing before/after of {topic}"
                ]
                
        except Exception as e:
            print(f"Error generating image suggestions: {e}")
            # Fallback to generic suggestions
            return [
                f"A person looking determined while working on {topic}",
                f"A split image showing before/after of {topic}"
            ]

def main():
    # Check for API key
    if not os.getenv('OPENROUTER_API_KEY'):
        print("Warning: OPENROUTER_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenRouter API key.")
        print("Example .env file content:")
        print("OPENROUTER_API_KEY=your-api-key-here")
        return

    generator = SocialMediaPostGenerator()
    
    # Example usage
    topic = input("Enter your topic: ")
    length = input("Enter length (short/medium/long): ")
    platform = input("Enter platform (Facebook/Instagram/LinkedIn/Twitter/TikTok): ")
    tone = input("Enter tone (Inspirational/Urgent/Emotional/Empathetic/Professional/Friendly/Casual): ")
    language = input("Enter language (EN/BM): ")
    
    result = generator.generate_post(topic, length, platform, tone, language)
    
    print("\nGenerated Post:")
    print("=" * 50)
    print(result['content'])
    print("\nImage Suggestions:")
    print("=" * 50)
    for i, suggestion in enumerate(result['image_suggestions'], 1):
        print(f"{i}. {suggestion}")

if __name__ == "__main__":
    main() 