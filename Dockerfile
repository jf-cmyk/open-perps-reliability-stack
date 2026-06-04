FROM nginx:1.27-alpine

WORKDIR /usr/share/nginx/html

COPY deploy/railway/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY index.html README.md LICENSE ./
COPY apps ./apps
COPY datasets ./datasets
COPY docs ./docs
COPY examples ./examples
COPY schemas ./schemas
COPY deliverables ./deliverables

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
