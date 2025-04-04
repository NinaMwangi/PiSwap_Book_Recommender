# Stage 1: Build React App
FROM node:18 AS build

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first (for caching dependencies)
COPY book-recommender-frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY ./book-recommender-frontend .

# Build the React app
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy the built React files from the previous stage to Nginx's web root
COPY --from=build /app/book-recommender-frontend-build /usr/share/nginx/html

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
