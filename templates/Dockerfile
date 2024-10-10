# Use the official Nginx image as a parent image
FROM nginx:alpine

COPY . /flask_app/templates

EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]