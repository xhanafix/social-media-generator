# AI Social Media Post Generator

A powerful tool that generates engaging social media posts using AI. Supports multiple platforms, languages, and tones. Built with a strong focus on factual accuracy and verified information.

## Features

- Generate posts for multiple platforms (Facebook, Instagram, LinkedIn, Twitter, TikTok)
- Support for multiple languages:
  - English (EN)
  - Bahasa Malaysia (BM) with casual language style (aku/kau)
- Various post lengths (short, medium, long)
- Different emotional tones
- Automatic hashtag generation
- Image suggestions
- Post history tracking
- Modern web interface
- **Factual Accuracy System**
  - Verified information only
  - No unsubstantiated claims
  - Reliable source citations
  - Clear fact/opinion distinction
  - Built-in fact-checking guidelines

## Language Support

The generator supports two languages with specific features:

1. **English (EN)**
   - Professional and engaging tone
   - Natural conversational style
   - Platform-specific formatting

2. **Bahasa Malaysia (BM)**
   - Casual and friendly language style
   - Uses "aku" and "kau" for personal connection
   - Localized expressions and slang
   - Platform-specific formatting

## Factual Accuracy Guidelines

The generator follows strict guidelines to ensure all content is factual and verified:

1. ✅ **Verified Information Only**
   - All content is based on verified facts
   - No unsubstantiated claims or rumors
   - Clear distinction between facts and opinions

2. ✅ **Source Reliability**
   - Statistics and facts are from reliable sources
   - Citations are included when necessary
   - Focus on well-established information

3. ✅ **Content Quality**
   - No misleading or false content
   - Clear and accurate information
   - Balanced and objective presentation

4. ✅ **User Transparency**
   - Clear indication of factual content
   - Disclosure of opinion-based content
   - Transparent about information sources

## Installation

1. Clone the repository:
```bash
git clone https://github.com/xhanafix/social-media-generator.git
cd social-media-generator
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Copy `env.sample.txt` to `.env`
   - Get your API key from [OpenRouter](https://openrouter.ai/)
   - Add your API key to the `.env` file:
     ```
     OPENROUTER_API_KEY=your-api-key-here
     ```

## Usage

### Web Interface
Run the Streamlit app:
```bash
python -m streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Command Line Interface
You can also use the generator from the command line:
```bash
python social_media_generator.py
```

## Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)

## Changing the AI Model

The generator uses OpenRouter's API to access various AI models. By default, it uses `deepseek/deepseek-chat-v3-0324:free`, but you can change it to any model supported by OpenRouter.

### Available Models
Some popular models you can use:
- `anthropic/claude-3-opus:beta` - Most capable model, best for complex content and factual accuracy
- `anthropic/claude-3-sonnet:beta` - Good balance of capability, speed, and accuracy
- `google/gemini-pro` - Strong performance for creative content with factual verification
- `meta-llama/llama-2-70b-chat` - Good for general purpose content with fact-checking
- `mistralai/mistral-7b-instruct` - Fast and efficient with basic fact verification
- `deepseek/deepseek-chat-v3-0324:free` - Free tier model (default)

### How to Change the Model
1. Open `social_media_generator.py`
2. Find the `__init__` method in the `SocialMediaPostGenerator` class
3. Locate the line: `self.default_model = "deepseek/deepseek-chat-v3-0324:free"`
4. Replace it with your preferred model, for example:
   ```python
   self.default_model = "anthropic/claude-3-opus:beta"
   ```

### Model Considerations
- Different models have different pricing tiers
- Some models may have different response times
- Model capabilities vary in terms of:
  - Content quality
  - Language support
  - Context length
  - Response speed
  - Factual accuracy
- Free tier models may have rate limits
- Fact-checking capabilities vary by model

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Powered by OpenRouter AI
- Built with Streamlit
- Fact-checking guidelines based on industry best practices
