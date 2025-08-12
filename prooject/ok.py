import google.generativeai as genai

# Replace YOUR_API_KEY with your actual Gemini API key
genai.configure(api_key="AIzaSyCOYJIhNLGDZ5WHKyydveQ2UU0__SC92eM")

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Generate a simple response
response = model.generate_content("Hello! Are you working?")
print(response.text)