# Dr. Balduino Andrade

Portfólio médico institucional em Flask para o Dr. Balduino Andrade, nefrologista. O site reúne apresentação profissional, áreas de atuação, jornada de cuidado, informações da clínica, contato e artigos educativos com área administrativa.

## Execução local

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
flask --app 'app:create_app()' init-db
flask --app 'app:create_app()' seed
flask --app 'app:create_app()' run --debug
```

Acesse `http://127.0.0.1:5000`. A área administrativa fica em `/admin/login`.

O comando `seed` cria dados demonstrativos e o usuário `admin` com senha `admin123` somente quando ainda não há artigos. Altere a senha antes de usar em produção. As configurações podem ser definidas no arquivo `.env`; use `.env.example` como referência.

## Hospedagem recomendada

O GitHub é excelente para armazenar o código e controlar versões, mas o GitHub Pages não executa Flask, não mantém sessões de login e não oferece banco de dados ou armazenamento persistente para o painel administrativo. A Vercel consegue executar Python em funções serverless, porém este projeto usa SQLite e uploads locais; sem uma adaptação para banco e armazenamento externos, artigos, sessões ou imagens podem deixar de ser persistentes.

Para manter o projeto integralmente funcional, prefira um serviço de aplicação como Render, Railway, Fly.io ou um servidor próprio, executando `gunicorn 'app:create_app()'`, com volume persistente para `instance/` e `static/uploads/`. Para produção profissional, use PostgreSQL e armazenamento de imagens compatível com S3. O repositório pode continuar hospedado no GitHub e ser conectado ao serviço de aplicação para deploy automático.

## Acesso administrativo e publicação

Para controlar os artigos, acesse `http://127.0.0.1:5000/admin/login`. No primeiro ambiente demonstrativo criado pelo comando `seed`, o acesso é `admin` com a senha `admin123`; altere essa credencial imediatamente antes de qualquer uso real. Depois do login, o painel permite criar artigos, salvar rascunhos, publicar, despublicar, editar capas e acompanhar visualizações. Um artigo só aparece no site quando está com o status `publicado`.

## Personalização institucional

Os dados da clínica e do médico são lidos por variáveis de ambiente para que o conteúdo possa ser atualizado sem alterar os templates. Antes da publicação, preencha pelo menos `CLINIC_NAME`, `CLINIC_ADDRESS`, `CLINIC_CITY`, `CLINIC_HOURS`, `CLINIC_MAP_URL`, `WHATSAPP_NUMBER`, `DOCTOR_CRM` e `DOCTOR_RQE` com informações confirmadas pela equipe responsável. `CLINIC_PHONE`, `CLINIC_EMAIL` e `CLINIC_INSTAGRAM` são opcionais. O botão “Como chegar” abre o Google Maps por meio de `CLINIC_MAP_URL`.

## Conteúdo ampliado

Além da home, perfil, áreas de atuação, contato e artigos, o site inclui páginas próprias para: quando procurar um nefrologista; doença renal crônica; hipertensão e rins; diabetes e rins; glomerulopatias; cálculo renal; medicamentos e rins; hemodiálise; prevenção; exames dos rins; perguntas frequentes; diferença entre nefrologista e urologista; e como funciona a consulta. Os dados de endereço, telefone, WhatsApp, Doctoralia e DaVita foram aproveitados das informações públicas disponíveis em `balduinoandrade.med.br` e devem ser confirmados pela equipe antes da publicação definitiva.

A identidade visual utiliza a paleta `#033651`, `#ddcdba4`, `#08abb2` e `#ffffff`. Como `#ddcdba4` é uma cor hexadecimal de oito dígitos, o CSS também mantém sua leitura opaca `#ddcdba` para superfícies e a variação alfa equivalente para detalhes. O corpo do site usa Kanit e os títulos usam `Quebec` quando a fonte estiver disponível, com fallback para Kanit. Como o arquivo original de Quebec não foi enviado, a aplicação mantém esse fallback até que a fonte licenciada seja adicionada ao projeto.

## Comandos úteis

- `flask --app 'app:create_app()' init-db`: cria as tabelas.
- `flask --app 'app:create_app()' seed`: insere artigos demonstrativos uma única vez.
- `flask --app 'app:create_app()' create-admin --username admin`: cria um administrador.
- `gunicorn 'app:create_app()'`: executa com Gunicorn.

O conteúdo dos artigos é sanitizado antes de ser salvo. A aplicação cria automaticamente as pastas de banco e uploads necessárias. As imagens remotas usadas como apoio editorial devem ser substituídas por fotos autorizadas da clínica e do médico antes da publicação definitiva.
