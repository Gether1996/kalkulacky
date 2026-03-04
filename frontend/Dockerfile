# Angular Frontend Dockerfile - Development Mode
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Expose port
EXPOSE 4200

# Start Angular dev server using npm script
# This uses the locally installed Angular CLI from node_modules
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--poll", "2000"]
