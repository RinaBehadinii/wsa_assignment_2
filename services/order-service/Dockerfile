FROM php:8.0-apache

WORKDIR /var/www/html

COPY index.php .
COPY .htaccess /var/www/html/.htaccess
COPY db-init /docker-entrypoint-initdb.d/

RUN docker-php-ext-install mysqli

RUN a2enmod rewrite && \
    service apache2 restart

RUN echo "<IfModule mod_dir.c>\n    DirectoryIndex index.php\n</IfModule>" >> /etc/apache2/apache2.conf
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

RUN sed -i '/<Directory \/var\/www\/>/,/<\/Directory>/d' /etc/apache2/apache2.conf && \
    echo "<Directory /var/www/>\n\
    Options Indexes FollowSymLinks\n\
    AllowOverride All\n\
    Require all granted\n\
</Directory>" >> /etc/apache2/apache2.conf

EXPOSE 80
CMD ["apache2-foreground"]
