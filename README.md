# Example CanvasXpress for Python Shiny App
An example project featuring CX-P, Shiny-P, and custom event support to trigger backend events.

To configure the project run:

    chmod +x ./setup.sh
    ./setup.sh

Some IDEs will auto-select the virtual environment, labelled `venv` in the project root directory, but if your IDE
does not then you can activate the vietual environment manually.  Open a new terminal window and change directories
to the project root directory if needed; then type:

    source venv/bin/activate

The virtual environment should become active, and your terminal prompt should change to show `(venv)` or similar.

Then run the app:

    shiny run --reload --launch-browser app.py

Or for the chart-only example:

    shiny run --reload --launch-browser app_chart_only.py
