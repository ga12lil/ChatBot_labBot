# ChatBot_labBot
 
Репозиторий содержит скрипт для запуска телеграм бота

**t.me/ChatBot_labBot**

## Функциональность бота
* команды: 
   - /start (выводится приветствие и список доступных команд)
   - /model (выводит название используемой LLM)
   - /clear (очистка контекста)
* запросы пользователя пересылаются LLM, запущеной на этом компьютере, и потом пересылаются пользователю

## Особенности бота
Контекст переписки сохраняется, LLM отвечает на текущий запрос с учетом контекста всего диалога.


