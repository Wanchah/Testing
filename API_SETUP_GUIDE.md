# EduMorph API Setup Guide

## Required API Keys for Full Functionality

To enable all AI features in EduMorph, you need to obtain API keys from the following services:

### 1. OpenAI API (Primary AI Service)
- **Purpose**: Document processing, content generation, summaries, flashcards, quiz questions
- **How to get**: 
  1. Visit [OpenAI Platform](https://platform.openai.com/)
  2. Sign up or log in
  3. Go to API Keys section
  4. Create a new API key
  5. Copy the key (starts with `sk-`)

### 2. Hugging Face API (Alternative AI Service)
- **Purpose**: Alternative AI models for content processing
- **How to get**:
  1. Visit [Hugging Face](https://huggingface.co/)
  2. Sign up or log in
  3. Go to Settings > Access Tokens
  4. Create a new token
  5. Copy the token

### 3. Anthropic API (Claude AI)
- **Purpose**: Advanced AI reasoning and content analysis
- **How to get**:
  1. Visit [Anthropic Console](https://console.anthropic.com/)
  2. Sign up or log in
  3. Go to API Keys
  4. Create a new API key
  5. Copy the key

## Configuration Steps

### Step 1: Update Environment Variables
Edit the `.env` file in your project root and add your API keys:

```env
# AI Services Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
HUGGINGFACE_API_KEY=your-huggingface-token-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### Step 2: Test API Integration
Run the test script to verify API connectivity:

```bash
python test_app_simple.py
```

### Step 3: Test AI Features
1. Go to `/ai/upload-document`
2. Upload a test document
3. Check if AI content is generated

## Fallback Behavior

If API keys are not provided, EduMorph will:
- Use enhanced basic content generation
- Still process documents and create structured content
- Generate flashcards and questions using text analysis
- Provide a fully functional experience without AI APIs

## Cost Considerations

### OpenAI API Pricing (as of 2024)
- GPT-3.5-turbo: ~$0.002 per 1K tokens
- Typical document processing: $0.01-0.05 per document
- Monthly usage for 100 documents: ~$1-5

### Hugging Face
- Free tier available for most models
- Pay-per-use for premium models

### Anthropic
- Claude API: ~$0.008 per 1K tokens
- Similar pricing to OpenAI

## Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables only**
3. **Rotate API keys regularly**
4. **Monitor API usage and costs**
5. **Set usage limits in your API accounts**

## Troubleshooting

### Common Issues

1. **"API key not found" error**
   - Check if `.env` file exists
   - Verify API key format
   - Ensure no extra spaces in the key

2. **"Rate limit exceeded" error**
   - Wait a few minutes and try again
   - Consider upgrading your API plan
   - Implement request throttling

3. **"Invalid API key" error**
   - Verify the key is correct
   - Check if the key has expired
   - Ensure the key has proper permissions

### Testing Without API Keys

The application works fully without API keys using enhanced basic content generation. This includes:
- Document text extraction
- Structured note generation
- Basic flashcard creation
- Simple quiz question generation
- All UI and navigation features

## Support

For API-related issues:
1. Check the respective API documentation
2. Verify your account status and billing
3. Test with a simple document first
4. Check the application logs for detailed error messages
