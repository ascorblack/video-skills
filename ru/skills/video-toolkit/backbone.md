# Основа рендера [Стек]

Основа управляет таймлайном, кадровыми часами, захватом и кодированием. Всё остальное (библиотеки анимации, canvas, 3D, физика, звук) подключается к ней. В источнике названы две основы; это альтернативы, а не слои одного стека.

## Что выбрать

| | Remotion | HyperFrames |
|---|---|---|
| Что такое сцена | React-компоненты; время — `useCurrentFrame()` | композиции HTML/CSS/JS; время задаётся приостановленным таймлайном GSAP (и другими зарегистрированными анимациями), который перематывает среда выполнения |
| Когда выбирать | проект на React/TypeScript, много параметризованных вариантов, видео из данных, команда уже пишет на React | видео пишет агент; полезен каталог готовых блоков (заголовки, субтитры, графики, переходы, 3D); обычный HTML легче читать и править, чем дерево React |
| Перематывает сам | всё, что управляется через `useCurrentFrame()`; интеграции `@remotion/three`, `@remotion/gsap`, `@remotion/lottie`, `@remotion/gif`, `@remotion/rive`, `@remotion/skia`; CSS-анимации через `animation-play-state` + отрицательный `animation-delay` | GSAP, CSS-анимации, Anime.js v4 (экземпляры, добавленные в `window.__hfAnime`), Lottie, Three.js и TypeGPU (через событие `hf-seek`), Web Animations |
| Не перематывает | `react-spring`, Framer Motion, всё на `requestAnimationFrame` | незарегистрированную библиотеку со своим тикером; незарегистрированные экземпляры Anime.js не перематываются никогда |
| Переходы | `@remotion/transitions` (`TransitionSeries`) | `@hyperframes/shader-transitions` (14 WebGL-шейдеров на таймлайне GSAP) и блоки реестра |
| Воспроизводимый рендер | та же функция кадра; Chrome и шрифты фиксируйте сами | `npx hyperframes render --docker` фиксирует Chromium, шрифты и FFmpeg |
| Лицензия | бесплатно для частных лиц, коммерческих компаний численностью до 3 сотрудников и некоммерческих организаций; для компаний крупнее нужна корпоративная лицензия | Apache 2.0 |

В обоих случаях «как выглядит кадр N» должно зависеть только от N. К тому же правилу уроки пришли на собственных ошибках [Визуал] [3D] — см. навык `video-render`, `seek-render.md`.

## Установка

Перед установкой проверьте актуальные требования: команды меняются от версии к версии.

**Remotion.**

```bash
npx create-video@latest
npx remotion studio                          # preview
npx remotion compositions                    # list composition ids
npx remotion render <CompositionId> out/video.mp4
```

Схема: `Composition` → `Sequence` → компоненты, которые читают `useCurrentFrame()` и вычисляют стили через `interpolate()` и `spring()`. Прежде чем подключать другую библиотеку анимации, прочитайте https://www.remotion.dev/docs/third-party.

**HyperFrames** (Node.js 22+ и FFmpeg).

```bash
npx hyperframes skills update                # agents: installs exactly the core skill set from main
npx hyperframes init my-video
cd my-video
npx hyperframes preview
npx hyperframes render                       # add --docker for a byte-reproducible render
```

Интерактивный выбор `npx skills add heygen-com/hyperframes` открывается без выбранных пунктов и отстаёт от `main`; неинтерактивный запуск без `--skill` устанавливает все семь скиллов. Для агента документированный путь — `npx hyperframes skills update`. Основные скиллы, которые нужно прочитать до написания кода HyperFrames:

- `/hyperframes` — контракт рендера и рабочий цикл; читать первым.
- `/hyperframes-cli` — создание каркаса проекта, линтинг, просмотр кадров, предпросмотр, рендер, восстановление после сбоев.
- `/hyperframes-registry` — около 450 редактируемых блоков: переходы, заголовки, кинетическая типографика, субтитры, графики, карты, 3D, движения камеры. Загляните сюда, прежде чем собирать конкретный визуальный приём вручную.
- `/media-use` — музыка, звуковые эффекты, изображения, озвучка, расшифровки, вырезанные объекты, цветовые стили.

Не считайте HyperFrames обёрткой над Remotion: у него собственный формат композиций, среда выполнения и CLI. Для переноса есть `/remotion-to-hyperframes`.

**OBS Studio** — не основа рендера, а рекордер. Его запись поступает в основу рендера как видеофайл. Когда и как его использовать — в `effects-map.md` и навыке `video-ui-capture`.

## Структура проекта

Подстраивайте её под основу рендера; не навязывайте HyperFrames пути Remotion.

```text
video-project/
  README.md            # what it is, render command, asset list with licenses
  package.json         # pinned versions
  src/ or compositions/
    scenes/            # one module per shot
    components/        # reusable titles, cards, diagrams, transitions
    theme/             # colors, fonts, motion tokens, output size and fps — in one place
    timeline/          # the shot table as data; baked simulations (JSON)
  assets/
    audio/ images/ video/
    fonts/             # only licensed fonts, as files, Cyrillic included [Popsci] [3D]
  scripts/
    bake-*.mjs         # simulations baked into per-frame tables
    render.sh
  out/
    v001.mp4 …         # every version a new file [Video] [Audio]
    qa/                # output of qa.sh
```

## Порядок работы

1. **План.** Сообщение, аудитория, длина, площадка, соотношение сторон, fps, язык, бренд, доступные ассеты. Недостающие параметры — выберите разумные значения и назовите их. Таблица шотов: `start`, `end`, картинка, переход, дикторский текст, звук, библиотека, ассеты. Кадры — `round(seconds × fps)`. Отметьте, что снято, а что сгенерировано. Длину не задают до подсчёта текста [Визуал].
2. **Один показательный шот.** 3–8 секунд в конечном разрешении и fps, с самой требовательной библиотекой ролика. Прежде чем делать остальное, проверьте типографику, движение, стык и то, что библиотека выдерживает перемотку (два рендера, сравнение).
3. **Все сцены.** Если ролик строится вокруг голоса, сначала дикторская дорожка: её тайминги задают картинку [Видео]. Библиотеки — только там, где они заметно выигрывают у основы рендера.
4. **Рендер и проверка.** `scripts/qa.sh`, полноразмерные кадры вокруг каждого стыка и в каждом моменте действия [Визуал] [3D], затем просмотр всего ролика.
5. **Итоговая проверка.** Кодек, размер, fps, длительность, звуковая дорожка нужной длины, отсутствие чёрных и прозрачных кадров в начале и конце, громкость и истинный пик закодированного файла [Звук]. Сдавайте MP4 вместе с редактируемым проектом, таблицей шотов, списком ассетов и заметками о проверке.
