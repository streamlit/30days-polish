# Zbuduj pulpit z możliwością przeciągania i zmiany rozmiaru za pomocą Streamlit Elements

Streamlit Elements jest zewnętrznym komponentem stworzononym przez [okld](https://github.com/okld), który dostarcza narzędzi do budowania pięknych aplikacji i pulpitów z wykorzystaniem widżetów Material UI, edytora Monaco (Visual Studio Code), wykresów Nivo i więcej.

## Sposób użycia

### Instalacja

Pierwszym krokiem będzie zainstalowanie biblioteki Streamlit Elements w Twoim środowisku:

```bash
pip install streamlit-elements==0.1.*
```

Zalecamy przypiąć wersję do `0.1.*` ponieważ nowe wersje biblioteki mogą wprowadzić zmiany niekompatybilne z tym przykładem.

### Użycie

Może zajrzeć do pliku [Streamlit Elements README](https://github.com/okld/streamlit-elements#getting-started) aby uzyskać szczegółowe iformacje na temat biblioteki.

## Co będziemy budować?

Celem dzisiejszej lekcji będzie stworzenie pulpitu złożonego z trzech komponentów Material UI:

- Pierwszy komponent będzie zawierał edytor kodu Monaco aby móc wprowadzać dane ;
- Drugi komponent będzie wyświetlał dane w postaci wykresu Nivo Bump ;
- Trzeci komponent wyświetli wideo z portalu YouTube na podstawie adresu przekazanego poprzez `st.text_input`.

Możesz użyć danych wygenerowanych z demo Nivo Bump, w zakładce „dane”: https://nivo.rocks/bump/.

## Przykładowa aplikacja

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/okld/streamlit-elements-demo/main)

## Wyjaśnienie działania, linijka po linijce

```python
# Na początku musimy zaimportować kilka bibliotek.

import json
import streamlit as st
from pathlib import Path

# Jeśli chodzi o Streamlit Elements, to będziemy potrzebowali wszystkich elementów zaimportowanych poniżej
# Wszystkie dostępne elementy wraz z opisem użycia są udokumentowane tutaj: https://github.com/okld/streamlit-elements#getting-started

from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo

# Zmieńmy układ strony tak aby nasz pulpit wypełniał całą jej szerokość.

st.set_page_config(layout="wide")

with st.sidebar:
    st.title("🗓️ #30DaysOfStreamlit")
    st.header("Dzień 27 - Streamlit Elements")
    st.write("Zbuduj pulpit z możliwością przeciągania i zmiany rozmiaru za pomocą Streamlit Elements.")
    st.write("---")

    # Zdefiniujmy adres URL dla odtwarzacza wideo.
    media_url = st.text_input("Media URL", value="https://www.youtube.com/watch?v=vIQQR_yq-8I")

# Zainicjalizujmy edytor kodu i wykres domyślymi wartościami.
#
# Na potrzeby tej lekcji, będziemy używali danych z przykładowej aplikacji dla wykresu Nivo Bump.
# Możesz pobrać dane z zakładki 'data': https://nivo.rocks/bump/
#
# Jak zobaczymy poniżej, klucz 'data' w stanie sesji zostanie zaktualizowany kiedy zmieni się kod w edytorze.
# Nowe dane zostaną odczytane przez wykres Nivo Bum, który się odświeży. 

if "data" not in st.session_state:
    st.session_state.data = Path("data.json").read_text()

# Zdefiniujmy domyślne rozmieszczenie elementów na stronie
# Domyślnie siatka pulpitu będzie się składać z 12 kolumn.
#
# Więcej informacji na temat dostępnych parametrów konfiguracji znajdziesz pod adresem:
# https://github.com/react-grid-layout/react-grid-layout#grid-item-props

layout = [
    
    # Komponent edytora jest umieszczony na współrzędnych x=0 i y=0, zajmuje 6/12 kolumn i ma wysokość 3 jednostek.
    dashboard.Item("edytor", 0, 0, 6, 3),
    # Komponent wykresu jest umieszczony na współrzędnych x=6 i y=0, zajmuje 6/12 kolumn i ma wysokość 3 jednostek.
    dashboard.Item("wykres", 6, 0, 6, 3),
    # Komponent wideo jest umieszczony na współrzędnych x=0 i y=3, zajmuje 6/12 kolumn i ma wysokość 4 jednostek.
    dashboard.Item("wideo", 0, 2, 12, 4),
]

# Tworzenie ramki do wyświetalnia elementów

with elements("przykład"):

    # Stwórzmy nowy pulpit z elementami rozmieszczonymi według układu zdefiniowanego powyżej.
    #
    # draggableHandle jest zmienną definiującą które części aplikacji mogą być przeciągane.
    # W naszym przypadku wszystkie elementy posiadające klasę CSS o nawie 'draggable' będą mogły zmieniać pozycję.
    #
    # Po więcej informacji na temat dostępnych parametrów siatki pulpitu zajrzyj pod następujące adresy:
    # https://github.com/react-grid-layout/react-grid-layout#grid-layout-props
    # https://github.com/react-grid-layout/react-grid-layout#responsive-grid-layout-props

    with dashboard.Grid(layout, draggableHandle=".draggable"):

        # Pierwszy komponent, edytor kodu
        #
        # Uzywamy parametru 'key' aby móc odwołać się do właściwego elementu pulpitu.
        #
        # Aby treść komponentu automatycznie dostosowywała swoją wysokość, użyjemy modelu flexbox.
        # sx jest parametrem dostępnym dla każdego widżetu Material UI i służy do dodania atrybutów CSS.
        #
        # Po więcej infromacji na temat komponentów, flexboxs oraz parametru sx, zajrzyj tutaj:
        # https://mui.com/components/cards/
        # https://mui.com/system/flexbox/
        # https://mui.com/system/the-sx-prop/

        with mui.Card(key="editor", sx={"display": "flex", "flexDirection": "column"}):

            # Aby sprawić, że nagłówek również jest przeciągalny, należy dodać do niego klasę  'draggable',
            # podobnie jak to robiliśmy dla innych komponentów przy pomocy zmiennej draggableHandle.

            mui.CardHeader(title="Editor", className="draggable")

            # Chcemy aby zawartość komponentu zajmowała całą dostępną wysokość dlatego ustawiamy parametr flex na 1
            # Ponadto chcemy aby zawartość komponentu miminalizowła się kiedy komponent jest zmniejszany ustawiając parametr minHeight to 0.

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # Tutaj definiujemy nasz edytor kodu Monaco.
                #
                # First, we set the default value to st.session_state.data that we initialized above.
                # Second, we define the language to use, JSON here.
                #
                # Then, we want to retrieve changes made to editor's content.
                # By checking Monaco documentation, there is an onChange property that takes a function.
                # This function is called everytime a change is made, and the updated content value is passed in
                # the first parameter (cf. onChange: https://github.com/suren-atoyan/monaco-react#props)
                #
                # Streamlit Elements provide a special sync() function. This function creates a callback that will
                # automatically forward its parameters to Streamlit's session state items.
                #
                # Examples
                # --------
                # Create a callback that forwards its first parameter to a session state item called "data":
                # >>> editor.Monaco(onChange=sync("data"))
                # >>> print(st.session_state.data)
                #
                # Create a callback that forwards its second parameter to a session state item called "ev":
                # >>> editor.Monaco(onChange=sync(None, "ev"))
                # >>> print(st.session_state.ev)
                #
                # Create a callback that forwards both of its parameters to session state:
                # >>> editor.Monaco(onChange=sync("data", "ev"))
                # >>> print(st.session_state.data)
                # >>> print(st.session_state.ev)
                #
                # Now, there is an issue: onChange is called everytime a change is made, which means everytime
                # you type a single character, your entire Streamlit app will rerun.
                #
                # To avoid this issue, you can tell Streamlit Elements to wait for another event to occur
                # (like a button click) to send the updated data, by wrapping your callback with lazy().
                #
                # For more information on available parameters for Monaco:
                # https://github.com/suren-atoyan/monaco-react
                # https://microsoft.github.io/monaco-editor/api/interfaces/monaco.editor.IStandaloneEditorConstructionOptions.html

                editor.Monaco(
                    defaultValue=st.session_state.data,
                    language="json",
                    onChange=lazy(sync("data"))
                )

            with mui.CardActions:

                # Monaco editor has a lazy callback bound to onChange, which means that even if you change
                # Monaco's content, Streamlit won't be notified directly, thus won't reload everytime.
                # So we need another non-lazy event to trigger an update.
                #
                # The solution is to create a button that fires a callback on click.
                # Our callback doesn't need to do anything in particular. You can either create an empty
                # Python function, or use sync() with no argument.
                #
                # Now, everytime you will click that button, onClick callback will be fired, but every other
                # lazy callbacks that changed in the meantime will also be called.

                mui.Button("Apply changes", onClick=sync())

        # Second card, the Nivo Bump chart.
        # We will use the same flexbox configuration as the first card to auto adjust the content height.

        with mui.Card(key="chart", sx={"display": "flex", "flexDirection": "column"}):

            # To make this header draggable, we just need to set its classname to 'draggable',
            # as defined above in dashboard.Grid's draggableHandle.

            mui.CardHeader(title="Chart", className="draggable")

            # Like above, we want to make our content grow and shrink as the user resizes the card,
            # by setting flex to 1 and minHeight to 0.

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # This is where we will draw our Bump chart.
                #
                # For this exercise, we can just adapt Nivo's example and make it work with Streamlit Elements.
                # Nivo's example is available in the 'code' tab there: https://nivo.rocks/bump/
                #
                # Data takes a dictionary as parameter, so we need to convert our JSON data from a string to
                # a Python dictionary first, with `json.loads()`.
                #
                # For more information regarding other available Nivo charts:
                # https://nivo.rocks/

                nivo.Bump(
                    data=json.loads(st.session_state.data),
                    colors={ "scheme": "spectral" },
                    lineWidth=3,
                    activeLineWidth=6,
                    inactiveLineWidth=3,
                    inactiveOpacity=0.15,
                    pointSize=10,
                    activePointSize=16,
                    inactivePointSize=0,
                    pointColor={ "theme": "background" },
                    pointBorderWidth=3,
                    activePointBorderWidth=3,
                    pointBorderColor={ "from": "serie.color" },
                    axisTop={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "",
                        "legendPosition": "middle",
                        "legendOffset": -36
                    },
                    axisBottom={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "",
                        "legendPosition": "middle",
                        "legendOffset": 32
                    },
                    axisLeft={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "ranking",
                        "legendPosition": "middle",
                        "legendOffset": -40
                    },
                    margin={ "top": 40, "right": 100, "bottom": 40, "left": 60 },
                    axisRight=None,
                )

        # Third element of the dashboard, the Media player.

        with mui.Card(key="media", sx={"display": "flex", "flexDirection": "column"}):
            mui.CardHeader(title="Media Player", className="draggable")
            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # This element is powered by ReactPlayer, it supports many more players other
                # than YouTube. You can check it out there: https://github.com/cookpete/react-player#props

                media.Player(url=media_url, width="100%", height="100%", controls=True)

```

## Any question?

Feel free to ask any question regarding Streamlit Elements or this challenge there: [Streamlit Elements Topic](https://discuss.streamlit.io/t/streamlit-elements-build-draggable-and-resizable-dashboards-with-material-ui-nivo-charts-and-more/24616)
