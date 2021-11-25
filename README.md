# Dashboard Analítico Twitter
## TCC - Dashboard Analítico usando Twitter API

Para instalação das bibliotecas é necessário a instalação do package installer pip, conforme documentação em: https://pypi.org/project/pip/

Alguns pacotes não são nativos do Python e logo precisam ser instalados também:
* Pip install pandas
* Pip install textblob
* Pip install squarify
* Pip install nltk
* Pip install tweepy
* Pip install PySimpleGUI

Os módulos abaixo pertencentes a biblioteca NLTK também precisam ser baixados para funcionamento:
* nltk.download('vader_lexicon')
* nltk.download('vader_lexicon')
 
Se faz necessário criar uma conta de desenvolvedor na para utilizar a API do Twitter (https://developer.twitter.com/en/docs/twitter-api) para que seja possível utilizar as Keys e Tokens. <b>As chaves podem demorar de 5 a 15 dias para serem aprovadas.</b>

 
Observações:
* Devido a problemas de latência, é possível que a ferramenta sinalize o alerta de “Não está respondendo”, porém, isso não implica na conclusão do dashboard que irá ser gerado normalmente.
* O caminho sinalizado para o armazenamento do dashboard deve ser o mais preciso possível por padrão ele virá sem nenhum e com isso irá armazenar a imagem do dashboard gerado na pasta do projeto ou  na pasta do usuário dentro do disco C.
 
 
