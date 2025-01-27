# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables
ENV AZURE_OPENAI_ENDPOINT="your-azure-openai-endpoint"
ENV AZURE_OPENAI_API_KEY="your-azure-openai-key"

# Expose the port that Streamlit will run on
EXPOSE 8501

# Run Streamlit when the container launches
CMD ["streamlit", "run", "streamlitapp.py", "--server.port=8501", "--server.address=0.0.0.0"]