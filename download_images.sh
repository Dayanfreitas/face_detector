#!/bin/bash

# Criar diretório fotos se não existir
mkdir -p fotos

# Função para baixar uma imagem
download_image() {
    local url=$1
    local filename=$(basename "$url")
    
    # Verificar se a URL é válida
    if curl --output /dev/null --silent --head --fail "$url"; then
        echo "Baixando: $url"
        curl -L "$url" -o "fotos/$filename"
        echo "Imagem salva como: fotos/$filename"
    else
        echo "Erro: URL inválida - $url"
    fi
}

# Verificar se foram fornecidos argumentos
if [ $# -eq 0 ]; then
    echo "Uso: $0 URL1 [URL2 URL3 ...]"
    echo "Exemplo: $0 https://exemplo.com/imagem1.jpg https://exemplo.com/imagem2.jpg"
    exit 1
fi

# Baixar cada URL fornecida
for url in "$@"; do
    download_image "$url"
done

echo "Download concluído!" 