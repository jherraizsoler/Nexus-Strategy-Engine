# Usamos Node 22 que es compatible con las últimas versiones de Angular
FROM node:22

WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalamos Angular CLI globalmente
RUN npm install -g @angular/cli

# Instalamos dependencias con legacy-peer-deps por el conflicto de FontAwesome
RUN npm install --legacy-peer-deps

# Copiar el código del front
COPY . .

EXPOSE 4200

# Comando estándar de arranque
CMD ["ng", "serve", "--host", "0.0.0.0","--poll", "2000"]