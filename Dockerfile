# Stage 1: Build the React app
FROM node:22-alpine as react-build

# Set the working directory for React
WORKDIR /frontend/book-recommender-frontend

# Copy package.json and package-lock.json
COPY ./App/book-recommender-frontend/package*.json ./


# Install dependencies
RUN npm install

# Copy the rest of the frontend source code
COPY ./App /frontend/
COPY ./API /frontend/

# Build the React app
RUN npm run build

# Stage 2: Set up FastAPI (Python environment)
FROM python:3.10-bullseye as backend

# Set the working directory for FastAPI
WORKDIR /backend

# Copy the backend dependencies
COPY ./requirements.txt ./



# Install FastAPI and other Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI source code
COPY ./ /backend

# Stage 3: Combine React and FastAPI into one container
FROM python:3.10-bullseye


# Install required system dependencies for both React and FastAPI
RUN apt-get update && apt-get install -y nginx curl

# Set the working directory for the combined app
WORKDIR /app

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the React build and FastAPI app files from previous stages
COPY --from=react-build /frontend/book-recommender-frontend/build /usr/share/nginx/html
COPY --from=backend /backend /app

# Install dependencies for FastAPI
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt



# Expose the ports for FastAPI (8000) and React (80)
EXPOSE 8000
EXPOSE 80

# Set up the command to run FastAPI and Nginx
CMD ["sh", "-c", "uvicorn Api.endpoints:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'"]
