# AI Social Media Post Generator

A powerful tool that generates engaging social media posts using AI. Supports multiple platforms, languages, and tones.

## Features

- Generate posts for multiple platforms (Facebook, Instagram, LinkedIn, Twitter, TikTok)
- Support for multiple languages (English, Bahasa Malaysia)
- Various post lengths (short, medium, long)
- Different emotional tones
- Automatic hashtag generation
- Image suggestions
- Post history tracking
- Modern web interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/social-media-generator.git
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