# Use the official Node.js image with a tag specifying the Node version
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application's source code
COPY . .

# Build the application
RUN npm run build

# Install a simple server for serving static content
RUN npm install -g serve

# Serve the static files from the build directory
CMD ["serve", "-s", "build"]