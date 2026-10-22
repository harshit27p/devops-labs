# Layer 1: Base image using minimal Alpine Linux with Nginx
FROM nginx:alpine

# Layer 2: Metadata labels
LABEL maintainer="student@cdac.in"
LABEL application="static-website"

# Layer 3: Remove default Nginx placeholder website
RUN rm -rf /usr/share/nginx/html/*

# Layer 4: Copy custom web assets into Nginx web root
COPY index.html /usr/share/nginx/html/index.html
COPY style.css /usr/share/nginx/html/style.css

# Layer 5: Document the exposed port
EXPOSE 80

# Layer 6: Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
