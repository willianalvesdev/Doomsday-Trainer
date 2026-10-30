# Doomsday Trainer — web local

Versão web recuperada do pacote Android 6.1.5 fornecido pelo usuário. O aplicativo usa React dentro de Capacitor; a pasta `dist` preserva sua interface, lógica de treino, áudio e recursos gráficos.

## Abrir

Nesta pasta, execute `python -m http.server 4174 --bind 127.0.0.1 --directory dist` e abra http://127.0.0.1:4174. Não abra o HTML diretamente via `file://`.

Os recordes e preferências ficam no armazenamento do navegador. Limpar os dados do navegador remove esses registros. Outra origem/porta usa armazenamento separado.

## Escopo

Mantidos: jogo de datas, treino guiado, drills, tutorial, treino personalizado, recordes locais, configurações de cores/design/texto/data e áudio.

Battle e ranking global ficam desativados: seus serviços PlayFab não fazem parte do APK. A autenticação automática e a inicialização de analytics foram removidas. Uma política `connect-src 'self'` impede chamadas de dados a servidores externos. A fonte opcional Space Grotesk ainda vem do Google Fonts; a fonte retro VT323 está no pacote.

A música usa um caminho relativo para funcionar também em subpastas. Zoom do navegador foi habilitado. Os botões de download da App Store e Google Play foram removidos da tela inicial. Compartilhamento depende do suporte do navegador à Web Share API. A interface continua em inglês, como o pacote original.

## Proveniência e reconstrução

`prepare.py <caminho-do-apks>` extrai somente `assets/public` do `base.apk` e aplica as adaptações documentadas. `evidence/extraction.json` guarda hashes SHA-256 do pacote e dos arquivos originais. O bundle é compilado/minificado; os fontes React originais não estavam incluídos.

REA: `evidence/javascript.json`, Evidence `ev_4a57bc21eb1fa8c19a759f25adb765926c277da2cafc8735a2fe4cbabc429fb6`, contém a análise estática da aplicação extraída antes das adaptações. A inspeção nativa do APKS não foi suportada pelo provedor disponível; o inventário ZIP foi feito com Python. A análise JavaScript REA concluiu normalmente.

Testes no navegador são da versão web recuperada, não da execução do Android. Não foi feita publicação nem alteração do Roll/Joll.

## Ícone e atalho no celular

O favicon e os ícones de atalho usam a arte Doomsday fornecida pelo usuário. No celular, abra o site pelo navegador e use “Adicionar à Tela de Início”. Os PNGs de 180, 192 e 512 pixels derivam do SVG em `favicon.svg`; o manifesto define o nome e o ícone do atalho.
