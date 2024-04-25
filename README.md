# ivo_ia

![Static Badge](https://img.shields.io/badge/Python-3.10-1?style=for-the-badge&logo=python&logoColor=yellow&color=blue)
![Static Badge](https://img.shields.io/badge/Rasa-3-1?style=for-the-badge&logo=rasa&logoColor=yellow&color=purple)


Para treinar o modelo :

    rasa train

Para testar o modelo no terminal (depende do passo 1) :

    rasa shell 

Para iniciar o servidor (depende do passo 1) :

    rasa run actions
    
    // em outro shell:
    
    rasa run --enable-api --cors "*" --debug
    
